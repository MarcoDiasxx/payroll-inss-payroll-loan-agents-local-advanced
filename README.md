# Payroll INSS Payroll Loan Agents

Agente de esteiras com MCP somente leitura para Jira e Confluence, planilha oficial local e regras core preservadas.

## Como funciona

`.github/agents/esteiras-analista.agent.md` chama as ferramentas do servidor MCP definido em `.vscode/mcp.json`. O MCP lê `.env`, autentica na Atlassian com a identidade de cada desenvolvedor e pesquisa Jira e Confluence. A politica integral continua em `docs/core/esteiras-core-policy.md`.

## Instalacao

```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp /caminho/da/planilha.xlsx docs/reference/Esteiras_Funcao-Grupos_de_Atividades-Alcadas_e_Fases.xlsx
```

No Windows PowerShell:

```powershell
Copy-Item .env.example .env
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item C:\caminho\planilha.xlsx docs\reference\Esteiras_Funcao-Grupos_de_Atividades-Alcadas_e_Fases.xlsx
```

Preencha no `.env` apenas o e-mail e um token novo. O token nunca deve entrar no Git.

## VS Code

1. Abra a pasta do repositorio.
2. Abra `MCP: List Servers` e inicie `esteiras-atlassian`.
3. Confirme a confianca no servidor local.
4. Selecione o agente `Esteiras Analista` no Chat.
5. Teste: `Valide o acesso as fontes core e informe quais estao disponiveis.`

Em Windows, se `${workspaceFolder}/.venv/bin/python` nao existir, altere o `command` em `.vscode/mcp.json` para `${workspaceFolder}\\.venv\\Scripts\\python.exe`.

## Identidade por usuario

A autenticacao do navegador Jira nao e automaticamente reutilizada por um MCP local. Cada pessoa deve copiar `.env.example` para `.env` e usar seu proprio e-mail/token. Assim, a API respeita exatamente as permissoes Jira e Confluence daquela conta.

Para SSO real, sem token local por pessoa, publique o MCP como servico remoto com OAuth 2.0/3LO ou integracao Atlassian corporativa. O modo `.env` deste repositorio e adequado ao uso local e nao representa SSO por sessao do navegador.

## Ferramentas MCP

- `test_atlassian_access`
- `get_core_references`
- `get_jira_issue`
- `search_jira_esteiras`
- `get_confluence_page`
- `search_confluence_esteiras`
- `discover_domain_knowledge`
- `lookup_official_activity`

## Politica de fontes

As referencias core sao absolutas. Resultados complementares enriquecem a analise, mas nao substituem silenciosamente BRGN-3563, a pagina core do Confluence, a planilha oficial ou a politica do repositorio.
