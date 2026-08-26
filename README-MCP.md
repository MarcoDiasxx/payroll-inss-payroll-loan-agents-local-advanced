# Esteiras Analista MCP

Este repositório contém o agente **Esteiras Analista** e um servidor MCP local, em modo somente leitura, para consultar Jira, Confluence, a política core, a planilha oficial e XMLs de referência antes de criar ou alterar esteiras Payroll/INSS.

O MCP utiliza Python 3.12, FastMCP e autenticação Atlassian carregada a partir do arquivo `.env` local.

> [!IMPORTANT]
> Nunca versione o arquivo `.env`, nunca compartilhe tokens e nunca utilize `VERIFY_SSL=false` como solução permanente.

---

## 1. Estrutura atual do projeto

A estrutura esperada é:

```text
payroll-inss-payroll-loan-agents-local-advanced/
├── .github/
│   └── agents/
│       └── esteiras-analista.agent.md
│
├── .venv/
│   ├── bin/
│   ├── include/
│   ├── lib/
│   └── pyvenv.cfg
│
├── .vscode/
│   └── mcp.json
│
├── config/
│   ├── core-references.json
│   └── domain-taxonomy.json
│
├── docs/
│   ├── core/
│   │   └── esteiras-core-policy.md
│   └── reference/
│       ├── xml/
│       │   ├── Esteira5000.xml
│       │   ├── Esteira5001.xml
│       │   ├── Esteira5010.xml
│       │   └── Esteira5021.xml
│       └── Esteiras_Funcao-Grupos_de_Atividades-Alcadas_e_Fases.xlsx
│
├── src/
│   ├── esteiras_mcp/
│   │   ├── __init__.py
│   │   ├── atlassian.py
│   │   └── server.py
│   └── esteiras_mcp.egg-info/
│
├── tests/
│   └── test_text_extract.py
│
├── .env
├── .gitignore
├── pyproject.toml
├── README.md
├── requirements.txt
└── SECURITY.md
```

### Função de cada diretório

- `.github/agents/`: definição do agente customizado.
- `.vscode/mcp.json`: configuração usada pelo VS Code para iniciar o MCP.
- `config/`: prioridade das fontes core e sinônimos dos domínios funcionais.
- `docs/core/`: política de negócio obrigatória do agente.
- `docs/reference/xml/`: XMLs usados somente como referência técnica antes e depois das alterações.
- `docs/reference/*.xlsx`: planilha oficial de decisões, atividades, fases, alçadas e proteções.
- `src/esteiras_mcp/`: implementação Python do servidor MCP.
- `tests/`: testes locais do pacote.

> [!NOTE]
> Arquivos criados pelo agente, como `Esteira - 5003 - INSS - Refin com Port [APP].xml`, podem permanecer na raiz durante o trabalho, mas os XMLs oficiais de comparação devem ficar em `docs/reference/xml/`.

---

## 2. Requisitos

- macOS ou Linux;
- Python 3.11 ou superior;
- Python 3.12 recomendado;
- VS Code atualizado;
- GitHub Copilot com suporte a agentes e MCP;
- acesso corporativo ao Jira e Confluence;
- token de API Atlassian válido;
- planilha oficial presente no caminho configurado;
- XMLs de referência em `docs/reference/xml/`.

Confirme o Python:

```bash
python3.12 --version
```

Resultado esperado:

```text
Python 3.12.x
```

---

## 3. Configurar o `.env`

Se ainda não existir um `.env`, crie a partir do exemplo:

```bash
cp .env.example .env
```

Configuração recomendada:

```dotenv
ATLASSIAN_BASE_URL=https://jiraps.atlassian.net
ATLASSIAN_EMAIL=seu-email-corporativo@empresa.com
ATLASSIAN_API_TOKEN=COLE_UM_TOKEN_NOVO_AQUI

JIRA_CORE_ISSUES=BRGN-3563
CONFLUENCE_CORE_PAGE_IDS=77048086725
JIRA_PROJECT_KEYS=BRGN
CONFLUENCE_SPACE_KEYS=BRGN

OFFICIAL_WORKBOOK_LOCAL_PATH=./docs/reference/Esteiras_Funcao-Grupos_de_Atividades-Alcadas_e_Fases.xlsx
REFERENCE_XML_DIR=./docs/reference/xml
REFERENCE_XSD_DIR=./docs/reference/xsd

ATLASSIAN_READ_ONLY=true
VERIFY_SSL=true
REQUIRE_CORE_REFERENCES=true
BLOCK_FINAL_XML_WITHOUT_REFERENCE=true
HTTP_TIMEOUT_SECONDS=30
SEARCH_MAX_RESULTS=50
```

### Segurança

O `.gitignore` deve conter:

```gitignore
.env
.env.*
!.env.example
.venv/
__pycache__/
*.py[cod]
*.egg-info/
.pytest_cache/
```

Confirme que o segredo está ignorado:

```bash
git check-ignore -v .env
```

---

## 4. Instalação inicial

Execute sempre na raiz do projeto:

```bash
cd /Users/SEU_USUARIO/Downloads/payroll-inss-payroll-loan-agents-local-advanced

python3.12 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
python -m pip install -e .
```

Valide o ambiente:

```bash
python --version
command -v python
echo "$VIRTUAL_ENV"
```

O executável deve apontar para:

```text
.../payroll-inss-payroll-loan-agents-local-advanced/.venv/bin/python
```

---

## 5. Inicialização diária

Ao abrir o projeto novamente:

```bash
cd /Users/SEU_USUARIO/Downloads/payroll-inss-payroll-loan-agents-local-advanced
source .venv/bin/activate
python --version
python -m pip check
code .
```

Não é necessário recriar a `.venv` todos os dias.

---

## 6. Configuração do VS Code

O arquivo `.vscode/mcp.json` deve utilizar o Python da `.venv` atual:

```json
{
  "servers": {
    "esteiras-atlassian": {
      "type": "stdio",
      "command": "${workspaceFolder}/.venv/bin/python",
      "args": [
        "-m",
        "esteiras_mcp.server"
      ],
      "cwd": "${workspaceFolder}",
      "envFile": "${workspaceFolder}/.env",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/src"
      }
    }
  }
}
```

O VS Code inicia o servidor como subprocesso `stdio`. Portanto, o MCP normalmente é iniciado pelo próprio VS Code e não precisa ficar aberto manualmente em outro terminal.

### Reiniciar o MCP

1. Pressione `Command + Shift + P`.
2. Execute `MCP: List Servers`.
3. Selecione `esteiras-atlassian`.
4. Escolha `Restart Server`.
5. Se necessário, execute `Developer: Reload Window`.
6. Abra o Chat e selecione `Esteiras Analista`.

---

## 7. Testar o pacote localmente

### Validar imports

```bash
source .venv/bin/activate

python - <<'PY'
import sys
import dotenv
import requests
import fastmcp
import openpyxl
import esteiras_mcp

print("Python:", sys.version)
print("Executável:", sys.executable)
print("Pacote MCP:", esteiras_mcp.__file__)
print("Dependências: OK")
PY
```

### Executar os testes

```bash
python -m pytest -q
```

### Testar o servidor manualmente

```bash
python -m esteiras_mcp.server
```

O MCP FastMCP usa `stdio` por padrão. Se o terminal permanecer ocupado sem traceback, o servidor está aguardando comunicação do cliente. Finalize o teste com `Ctrl+C`.

Nunca inicie assim:

```bash
python src/esteiras_mcp/server.py
```

Sempre inicie como módulo:

```bash
python -m esteiras_mcp.server
```

---

## 8. Validar as fontes core pelo agente

No Chat do VS Code, selecione o agente `Esteiras Analista` e execute:

```text
Valide as fontes core sem alterar arquivos.

Consulte:
1. identidade Atlassian;
2. Jira BRGN-3563;
3. Confluence 77048086725;
4. docs/core/esteiras-core-policy.md;
5. docs/reference/Esteiras_Funcao-Grupos_de_Atividades-Alcadas_e_Fases.xlsx;
6. XMLs em docs/reference/xml/.

Informe disponibilidade, identificador, versão ou data, erro e estado final.
Não gere nem altere XML.
```

A validação completa deve mostrar:

```text
Identidade Atlassian: confirmada
Jira core: disponível
Confluence core: disponível
Política core: disponível
Planilha oficial: disponível
XMLs de referência: disponíveis
Modo: somente leitura
```

---

## 9. Uso correto dos XMLs de referência

Os arquivos abaixo são referências técnicas:

```text
docs/reference/xml/Esteira5000.xml
docs/reference/xml/Esteira5001.xml
docs/reference/xml/Esteira5010.xml
docs/reference/xml/Esteira5021.xml
```

Antes de criar ou alterar uma esteira, o agente deve:

1. listar os XMLs de `docs/reference/xml/`;
2. selecionar o XML funcionalmente mais próximo;
3. ler integralmente o XML selecionado;
4. comparar produto, canal e operação;
5. verificar estrutura, atividades, decisões, processos, fases, alçadas e roteamentos;
6. confrontar o XML com Jira, Confluence, política core e planilha oficial;
7. apresentar a análise prévia;
8. somente depois iniciar a alteração;
9. comparar novamente o resultado com a referência.

Os XMLs de exemplo não substituem as fontes normativas e nunca devem ser alterados automaticamente.

### Teste de leitura dos XMLs

```text
Liste e leia todos os XMLs existentes em docs/reference/xml/.

Para cada arquivo, informe:
- caminho;
- código de esteira;
- produto;
- canal;
- operação;
- atividade inicial;
- atividades finais;
- quantidade de atividades;
- decisões duplicadas;
- referências quebradas.

Não altere nenhum arquivo.
```

---

# Solução de problemas

## 10. `source: no such file or directory: .venv/bin/activate`

A `.venv` não existe na pasta atual.

```bash
cd /caminho/correto/do/projeto
python3.12 -m venv .venv
source .venv/bin/activate
```

---

## 11. `zsh: command not found: python`

A `.venv` não foi ativada ou foi criada incorretamente.

```bash
rm -rf .venv
python3.12 -m venv .venv
source .venv/bin/activate
python --version
command -v python
```

---

## 12. `No module named dotenv`

```bash
source .venv/bin/activate
python -m pip install python-dotenv
python -m pip install -r requirements.txt
```

Valide:

```bash
python -c "from dotenv import load_dotenv; print('dotenv OK')"
```

---

## 13. `No matching distribution found for fastmcp`

O Python da `.venv` é antigo.

```bash
deactivate 2>/dev/null || true
rm -rf .venv
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
python -m pip install -e .
```

---

## 14. `No module named esteiras_mcp`

Instale o projeto em modo editável:

```bash
source .venv/bin/activate
python -m pip install -e .
python -c "import esteiras_mcp; print(esteiras_mcp.__file__)"
python -m esteiras_mcp.server
```

Alternativa temporária:

```bash
PYTHONPATH="$PWD/src" python -m esteiras_mcp.server
```

---

## 15. `CERTIFICATE_VERIFY_FAILED`

O Python não confia na cadeia TLS apresentada ao acessar a Atlassian.

Primeiro instale `truststore`:

```bash
source .venv/bin/activate
python -m pip install "truststore>=0.10,<1"
```

O início de `src/esteiras_mcp/server.py` e `src/esteiras_mcp/atlassian.py` deve carregar o trust store antes de `requests`:

```python
import truststore
truststore.inject_into_ssl()
```

Mantenha:

```dotenv
VERIFY_SSL=true
```

Nunca use `VERIFY_SSL=false` como solução definitiva.

Teste:

```bash
python - <<'PY'
import truststore
truststore.inject_into_ssl()
import requests

response = requests.get("https://jiraps.atlassian.net", timeout=30)
print("Status HTTP:", response.status_code)
print("TLS: OK")
PY
```

Se o erro continuar, solicite à equipe responsável o bundle da CA corporativa e configure fora do Git:

```dotenv
REQUESTS_CA_BUNDLE=/Users/SEU_USUARIO/.certs/corporate-ca.pem
SSL_CERT_FILE=/Users/SEU_USUARIO/.certs/corporate-ca.pem
VERIFY_SSL=true
```

---

## 16. Erros HTTP Atlassian

### `401`

Token ou e-mail inválido. Gere um token novo e confira:

```dotenv
ATLASSIAN_EMAIL=seu-email-correto
ATLASSIAN_API_TOKEN=token-novo
```

### `403`

A autenticação funcionou, mas a identidade não possui permissão para o card, projeto, espaço ou página.

### `404`

O recurso não existe ou não está visível para a identidade. Confirme:

```dotenv
JIRA_CORE_ISSUES=BRGN-3563
CONFLUENCE_CORE_PAGE_IDS=77048086725
```

---

## 17. Planilha oficial não encontrada

Confirme o caminho real desta estrutura:

```dotenv
OFFICIAL_WORKBOOK_LOCAL_PATH=./docs/reference/Esteiras_Funcao-Grupos_de_Atividades-Alcadas_e_Fases.xlsx
```

Teste:

```bash
ls -lh docs/reference/Esteiras_Funcao-Grupos_de_Atividades-Alcadas_e_Fases.xlsx
```

---

## 18. XMLs não encontrados

Nesta estrutura, o caminho correto é:

```dotenv
REFERENCE_XML_DIR=./docs/reference/xml
```

Teste:

```bash
find docs/reference/xml -maxdepth 1 -type f -name '*.xml' -print
```

Não utilize no agente caminhos antigos como:

```text
.github/references/
```

O caminho atual é:

```text
docs/reference/xml/
```

---

## 19. O MCP inicia, mas o agente não usa as ferramentas

Verifique o frontmatter de `.github/agents/esteiras-analista.agent.md`:

```yaml
---
name: Esteiras Analista
description: Analisa, cria, revisa e audita esteiras Payroll/INSS com fontes oficiais e referências XML.
target: vscode
tools:
  - read
  - search
  - edit
  - execute
  - esteiras-atlassian/*
user-invocable: true
disable-model-invocation: false
---
```

Depois:

1. salve o arquivo;
2. execute `Developer: Reload Window`;
3. reinicie `esteiras-atlassian`;
4. selecione novamente `Esteiras Analista`;
5. confira as ferramentas habilitadas no Chat.

---

## 20. Recuperação completa do MCP

Quando vários erros ocorrerem ao mesmo tempo, execute:

```bash
cd /Users/SEU_USUARIO/Downloads/payroll-inss-payroll-loan-agents-local-advanced

deactivate 2>/dev/null || true
rm -rf .venv
rm -rf .pytest_cache
find . -type d -name '__pycache__' -prune -exec rm -rf {} +
find src -maxdepth 1 -type d -name '*.egg-info' -prune -exec rm -rf {} +

python3.12 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
python -m pip install -e .

python -m pip check
python -m pytest -q
python -c "from esteiras_mcp.server import mcp; print('MCP OK')"
python -m esteiras_mcp.server
```

Depois reinicie o servidor no VS Code.

---

## 21. Diagnóstico completo

```bash
echo '=== DIRETÓRIO ==='
pwd

echo '=== PYTHON ==='
python --version
command -v python

echo '=== VENV ==='
echo "$VIRTUAL_ENV"
ls -la .venv/bin/python*

echo '=== DEPENDÊNCIAS ==='
python -m pip check
python -m pip show fastmcp python-dotenv requests truststore openpyxl

echo '=== PACOTE ==='
python -c "import esteiras_mcp; from esteiras_mcp.server import mcp; print(esteiras_mcp.__file__); print('MCP OK')"

echo '=== CONFIGURAÇÃO ==='
test -f .env && echo '.env encontrado' || echo '.env ausente'
git check-ignore -v .env || true

echo '=== FONTES LOCAIS ==='
test -f docs/core/esteiras-core-policy.md && echo 'Política core encontrada' || echo 'Política core ausente'
test -f docs/reference/Esteiras_Funcao-Grupos_de_Atividades-Alcadas_e_Fases.xlsx && echo 'Planilha encontrada' || echo 'Planilha ausente'
find docs/reference/xml -maxdepth 1 -type f -name '*.xml' -print

echo '=== TESTES ==='
python -m pytest -q
```

Antes de compartilhar a saída, confirme que nenhum token ou segredo foi exibido.

---

## 22. Checklist de suporte

```text
[ ] O VS Code está aberto na raiz do projeto
[ ] Python 3.12 está instalado
[ ] .venv existe na raiz atual
[ ] python aponta para .venv/bin/python
[ ] requirements.txt foi instalado
[ ] pip install -e . foi executado
[ ] .env existe e está ignorado pelo Git
[ ] O token Atlassian é válido e não foi exposto
[ ] VERIFY_SSL=true
[ ] Jira abre para a identidade configurada
[ ] Confluence abre para a identidade configurada
[ ] A política existe em docs/core/
[ ] A planilha existe em docs/reference/
[ ] Os XMLs existem em docs/reference/xml/
[ ] .vscode/mcp.json aponta para .venv/bin/python
[ ] O MCP foi reiniciado no VS Code
[ ] O agente Esteiras Analista está selecionado
[ ] As ferramentas esteiras-atlassian estão habilitadas
```

---

## 23. Estado esperado para trabalhar

```text
Python: 3.12.x
Ambiente: .venv ativa
MCP: iniciado
Modo Atlassian: somente leitura
Identidade Atlassian: confirmada
Jira BRGN-3563: disponível
Confluence core: disponível
Política core local: disponível
Planilha oficial: disponível
XMLs em docs/reference/xml/: disponíveis
```

Se uma fonte obrigatória estiver indisponível, o agente deve classificar a análise como `RASCUNHO` ou `BLOQUEADO`, nunca como pronta para implantação.
