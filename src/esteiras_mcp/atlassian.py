from __future__ import annotations

import os
import re
from typing import Any

import truststore

truststore.inject_into_ssl()

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()


def _need(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Variavel obrigatoria ausente: {name}")
    return value


def plain_adf(value: Any) -> str:
    """Extract readable text from Atlassian Document Format."""
    out: list[str] = []
    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("type") == "text" and node.get("text"):
                out.append(str(node["text"]))
            if node.get("type") in {"paragraph", "heading", "listItem"} and out and out[-1] != "\n":
                pass
            for child in node.get("content", []):
                walk(child)
            if node.get("type") in {"paragraph", "heading", "listItem", "blockquote"}:
                out.append("\n")
        elif isinstance(node, list):
            for item in node:
                walk(item)
        elif isinstance(node, str):
            out.append(node)
    walk(value)
    return re.sub(r"\n{3,}", "\n\n", "".join(out)).strip()


def plain_html(value: str | None) -> str:
    if not value:
        return ""
    return BeautifulSoup(value, "html.parser").get_text("\n", strip=True)


class AtlassianClient:
    def __init__(self) -> None:
        self.base = _need("ATLASSIAN_BASE_URL").rstrip("/")
        email = _need("ATLASSIAN_EMAIL")
        token = _need("ATLASSIAN_API_TOKEN")
        self.timeout = int(os.getenv("HTTP_TIMEOUT_SECONDS", "30"))
        self.verify = os.getenv("VERIFY_SSL", "true").lower() == "true"
        if os.getenv("ATLASSIAN_READ_ONLY", "true").lower() != "true":
            raise RuntimeError("ATLASSIAN_READ_ONLY deve permanecer true")
        self.http = requests.Session()
        self.http.auth = HTTPBasicAuth(email, token)
        self.http.headers.update({"Accept": "application/json"})

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        response = self.http.get(f"{self.base}{path}", params=params, timeout=self.timeout, verify=self.verify)
        if response.status_code == 401:
            raise RuntimeError("401: e-mail ou token invalido")
        if response.status_code == 403:
            raise RuntimeError("403: identidade sem permissao")
        if response.status_code == 404:
            raise RuntimeError("404: recurso ausente ou nao visivel")
        response.raise_for_status()
        return response.json()

    def myself(self) -> dict[str, Any]:
        data = self._get("/rest/api/3/myself")
        return {"accountId": data.get("accountId"), "displayName": data.get("displayName"), "active": data.get("active")}

    def issue(self, key: str) -> dict[str, Any]:
        data = self._get(f"/rest/api/3/issue/{key}", {"fields": "summary,description,status,updated,created,labels,comment,attachment,issuetype,project"})
        fields = data.get("fields", {})
        comments = []
        for c in (fields.get("comment") or {}).get("comments", []):
            comments.append({"author": (c.get("author") or {}).get("displayName"), "created": c.get("created"), "body": plain_adf(c.get("body"))})
        return {
            "key": data.get("key"), "url": f"{self.base}/browse/{data.get('key')}",
            "summary": fields.get("summary"), "description": plain_adf(fields.get("description")),
            "status": (fields.get("status") or {}).get("name"), "issueType": (fields.get("issuetype") or {}).get("name"),
            "created": fields.get("created"), "updated": fields.get("updated"), "labels": fields.get("labels") or [],
            "comments": comments,
            "attachments": [{"filename": a.get("filename"), "mimeType": a.get("mimeType"), "content": a.get("content")} for a in fields.get("attachment") or []]
        }

    def search_jira(self, text: str, max_results: int = 50, project_keys: list[str] | None = None) -> list[dict[str, Any]]:
        escaped = text.replace('"', '\\"')
        clauses = [f'text ~ "{escaped}"']
        if project_keys:
            quoted = ",".join(f'"{p}"' for p in project_keys)
            clauses.insert(0, f"project in ({quoted})")
        jql = " AND ".join(clauses) + " ORDER BY updated DESC"
        data = self._get("/rest/api/3/search", {"jql": jql, "maxResults": min(max_results, 100), "fields": "summary,status,updated,description,labels,issuetype"})
        results = []
        for item in data.get("issues", []):
            f = item.get("fields", {})
            results.append({
                "key": item.get("key"), "url": f"{self.base}/browse/{item.get('key')}", "summary": f.get("summary"),
                "status": (f.get("status") or {}).get("name"), "issueType": (f.get("issuetype") or {}).get("name"),
                "updated": f.get("updated"), "labels": f.get("labels") or [], "description": plain_adf(f.get("description"))[:4000]
            })
        return results

    def confluence_page(self, page_id: str) -> dict[str, Any]:
        data = self._get(f"/wiki/api/v2/pages/{page_id}", {"body-format": "storage"})
        body = ((data.get("body") or {}).get("storage") or {}).get("value")
        links = data.get("_links") or {}
        webui = links.get("webui") or ""
        return {
            "id": data.get("id"), "title": data.get("title"), "status": data.get("status"),
            "version": data.get("version"), "body": plain_html(body),
            "url": f"{self.base}{webui}" if webui else None
        }

    def search_confluence(self, text: str, max_results: int = 50, space_keys: list[str] | None = None) -> list[dict[str, Any]]:
        safe = text.replace('"', '\\"')
        cql = f'type=page AND text ~ "{safe}"'
        if space_keys:
            quoted = ",".join(f'"{s}"' for s in space_keys)
            cql += f" AND space in ({quoted})"
        data = self._get("/wiki/rest/api/content/search", {"cql": cql, "limit": min(max_results, 100), "expand": "body.storage,version,space"})
        results = []
        for item in data.get("results", []):
            webui = (item.get("_links") or {}).get("webui")
            results.append({
                "id": item.get("id"), "title": item.get("title"), "space": (item.get("space") or {}).get("key"),
                "version": item.get("version"), "url": f"{self.base}{webui}" if webui else None,
                "body": plain_html(((item.get("body") or {}).get("storage") or {}).get("value"))[:8000]
            })
        return results
