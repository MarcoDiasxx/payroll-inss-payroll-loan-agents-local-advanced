# Payroll INSS Payroll Loan Agents

Agente **Esteiras Analista** para criar, revisar e validar esteiras de decisão Payroll/INSS. Ele consulta Jira, Confluence, a planilha oficial de atividades e os XMLs de referência antes de responder, por meio de um servidor MCP **somente leitura**.

Para o guia completo de instalação e solução de problemas, veja [`README-MCP.md`](README-MCP.md).

## O que você consegue fazer

- **Validar uma esteira nova ou migrada:** o agente avalia o DoR e o DoD item a item, com base nas páginas vigentes do Confluence, e lista os cards relacionados.
- **Analisar ou ajustar um XML:** estrutura, atividades protegidas, alçadas, fases, rotas, pushes e comparação com as esteiras de referência.
- **Criar uma esteira nova:** XML, comparativo antes e depois, de-para, checklist de testes e rollback.
- **Consultar as regras oficiais:** número de decisão, processo, alçada e fase de uma atividade.

O agente nunca altera cards, páginas ou o conteúdo de `docs/reference/xml/`.

## Como as peças se encaixam

```text
Chat do VS Code
   └── agente "Esteiras Analista"        .github/agents/esteiras-analista.agent.md
          │   (regras de negócio)        docs/core/esteiras-core-policy.md
          ▼
       servidor MCP "esteiras-atlassian"  src/esteiras_mcp/server.py
          │   (processo Python local, lê o .env, somente leitura)
          ├── Jira e Confluence           com o seu e-mail e o seu token
          ├── Planilha oficial            docs/reference/*.xlsx
          └── XMLs de referência          docs/reference/xml/
```

O **agente** é quem conversa com você. O **MCP** é um programa Python local que dá ao agente as ferramentas para buscar nas fontes. Você **não precisa rodar o MCP manualmente**: o VS Code o inicia como subprocesso a partir de `.vscode/mcp.json`.

## Antes de começar

- macOS, Linux ou Windows com Python 3.11 ou superior (3.12 recomendado).
- VS Code atualizado, com GitHub Copilot com suporte a agentes e MCP.
- Acesso ao Jira e ao Confluence da empresa.
- Um **token de API Atlassian seu**, gerado em <https://id.atlassian.com/manage-profile/security/api-tokens>.

## Instalação (uma única vez)

Na raiz do repositório:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

No Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Abra o `.env` e preencha **somente**:

```dotenv
ATLASSIAN_EMAIL=seu-email-corporativo@empresa.com
ATLASSIAN_API_TOKEN=cole-seu-token-aqui
```

As demais variáveis já vêm com os valores do projeto. O `.env` está no `.gitignore`: nunca o versione nem compartilhe o token.

A planilha oficial (`docs/reference/Esteiras_Funcao-Grupos_de_Atividades-Alcadas_e_Fases.xlsx`) já está no repositório. Substitua o arquivo somente se tiver uma versão mais nova.

## Como iniciar o MCP

1. Abra a **pasta do repositório** no VS Code.
2. Abra a paleta (`Cmd/Ctrl + Shift + P`) e execute **`MCP: List Servers`**.
3. Selecione **`esteiras-atlassian`** e escolha **`Start Server`**. Na primeira vez, confirme a confiança no servidor local.
4. Abra o Chat e selecione o agente **`Esteiras Analista`**.
5. Teste com: `Valide o acesso às fontes core e informe quais estão disponíveis.`

O servidor está funcionando quando aparece como **Running** em `MCP: List Servers` e as ferramentas de `esteiras-atlassian` aparecem na lista de ferramentas do Chat.

**Reinicie o servidor** (`MCP: List Servers` → `esteiras-atlassian` → `Restart Server`) sempre que mudar o `.env`, o código em `src/` ou o arquivo `.vscode/mcp.json`. O `.env` só é lido na inicialização.

**No Windows**, se `${workspaceFolder}/.venv/bin/python` não existir, troque o `command` em `.vscode/mcp.json` por `${workspaceFolder}\\.venv\\Scripts\\python.exe`.

### Rodar manualmente (só para diagnóstico)

```bash
source .venv/bin/activate
PYTHONPATH=src python -m esteiras_mcp.server
```

O terminal fica parado, aguardando um cliente: isso é o esperado. Encerre com `Ctrl+C`. Sempre inicie como módulo (`-m esteiras_mcp.server`), nunca com `python src/esteiras_mcp/server.py`.

## Como usar o agente

Exemplos de pedidos no Chat:

| Objetivo | Exemplo |
| --- | --- |
| Conferir se as fontes estão acessíveis | `Valide o acesso às fontes core e informe quais estão disponíveis.` |
| Validar uma esteira nova | `Valide a esteira 5011 (XML anexo) contra o DoR e o DoD e traga os cards relacionados. Card: BRGN-XXXX.` |
| Analisar um ajuste em XML | `Analise o ajuste de recálculo neste XML e compare com a referência.` |
| Criar uma esteira | `Crie a esteira 5013 - INSS - Refin com Port [CorBan] a partir da referência equivalente.` |
| Consultar uma atividade | `Qual é a alçada e a fase da decisão 225?` |

Na **validação de esteira nova**, o agente:

1. abre o DoR, o DoD, o processo de entrega, as padronizações e o card `BRGN-3563`, lidos na hora;
2. abre também as páginas filhas de critério de "Esteiras Função" (critérios INSS, modelo de decisão, setup de pushes);
3. valida o XML e confere as atividades na planilha oficial;
4. avalia cada item do DoR e do DoD como `ATENDIDO`, `NAO ATENDIDO`, `NAO APLICAVEL` ou `NAO VALIDADO`;
5. procura cards e páginas relacionados e diz qual o efeito de cada um na validação;
6. entrega um veredito e um checklist para você confirmar.

Para ajudar o agente, informe **o código da esteira, o XML e a chave do card Jira**. Itens que dependem de ação fora do repositório (backup, RFC, revisão por par, Message Center, anuência, teste) só ficam como atendidos se você informar a evidência. Sem ela, o agente pergunta.

Estados possíveis do resultado: `RASCUNHO`, `VALIDADO ESTRUTURALMENTE`, `VALIDADO CONTRA REFERENCIAS`, `PRONTO PARA DEV`, `PRONTO PARA HML`, `ELEGIVEL PARA PRD` e `CUIDADO` (divergência crítica ou fonte obrigatória ausente).

> [!NOTE]
> O MCP lê somente o **texto** das páginas. Imagens, vídeos e arquivos `.drawio.xml` anexados são apenas listados, e o agente pede o conteúdo a você quando ele for necessário.

## Ferramentas MCP

| Ferramenta | Para que serve |
| --- | --- |
| `test_atlassian_access` | Confirma a identidade Atlassian configurada, sem expor o token. |
| `get_core_references` | Carrega as referências core (Jira, Confluence, política e planilha) e informa o que não estiver disponível. |
| `get_jira_issue` | Abre um card pela chave, com descrição, comentários e anexos listados. |
| `search_jira_esteiras` | Busca cards por termos de negócio, siglas e sinônimos. |
| `get_confluence_page` | Abre uma página pelo ID, com texto, versão, URL e lista de anexos. |
| `get_confluence_children` | Lista as páginas filhas e os anexos de uma página. |
| `search_confluence_esteiras` | Busca páginas por termos de negócio. |
| `discover_domain_knowledge` | Busca ampla em Jira e Confluence para um domínio (INSS, refin, portabilidade, novas esteiras etc.). |
| `lookup_official_activity` | Consulta a planilha oficial por número de decisão ou texto da atividade. |

## Fontes consultadas

As referências abaixo são **core** e nunca são substituídas em silêncio por resultados de busca. Os IDs ficam em `CONFLUENCE_CORE_PAGE_IDS` e `JIRA_CORE_ISSUES` no `.env`.

| Fonte | Identificador |
| --- | --- |
| Jira: padronização das esteiras INSS (DoR, DoD e critérios) | `BRGN-3563` |
| Confluence: Esteiras Função | `77048086725` |
| Confluence: DoR | `77048546241` |
| Confluence: DoD | `77048546248` |
| Confluence: processo para criar, alterar e entregar esteira | `77534004754` |
| Confluence: padronizações de códigos, atividades e esteiras | `77137215636` |
| Política do agente | `docs/core/esteiras-core-policy.md` |
| Planilha oficial | `docs/reference/Esteiras_Funcao-Grupos_de_Atividades-Alcadas_e_Fases.xlsx` |
| XMLs de referência | `docs/reference/xml/` |

Quando uma fonte não está acessível, o agente avisa com `BLOQUEIO DE FONTE` e marca o que depende dela como `NAO VALIDADO`.

## Identidade por usuário

A sessão do navegador no Jira **não** é reaproveitada pelo MCP local. Cada pessoa usa o próprio e-mail e token no `.env`, e a API respeita exatamente as permissões Jira e Confluence daquela conta. Para SSO real, sem token por pessoa, seria preciso publicar o MCP como serviço remoto com OAuth 2.0/3LO. Mais detalhes em [`SECURITY.md`](SECURITY.md).

## Problemas comuns

| Sintoma | O que fazer |
| --- | --- |
| `401` | E-mail ou token inválido. Gere um token novo e atualize o `.env`. |
| `403` | A sua conta não tem permissão para o card ou a página. |
| `404` | O recurso não existe ou não está visível para a sua conta. |
| O servidor não aparece como **Running** | Confirme que a `.venv` existe e que as dependências estão instaladas. Veja o `command` em `.vscode/mcp.json`. |
| `No module named ...` | Ative a `.venv` e rode `python -m pip install -r requirements.txt`. |
| Ferramentas novas ou mudanças no `.env` não aparecem | Reinicie o servidor: `MCP: List Servers` → `Restart Server`. |
| O agente não usa as ferramentas do MCP | Veja a seção 19 do [`README-MCP.md`](README-MCP.md) (frontmatter do agente) e recarregue a janela. |
| `CERTIFICATE_VERIFY_FAILED` | Veja a seção 15 do [`README-MCP.md`](README-MCP.md). Não use `VERIFY_SSL=false` como solução permanente. |

## Estrutura do repositório

| Caminho | Conteúdo |
| --- | --- |
| `.github/agents/` | Definição do agente `Esteiras Analista`. |
| `.vscode/mcp.json` | Como o VS Code inicia o MCP. |
| `docs/core/` | Política de negócio obrigatória do agente. |
| `docs/reference/` | Planilha oficial e XMLs de referência (somente leitura). |
| `docs/analysis/` | Análises geradas, como o comparativo das esteiras 5003 e 6014. |
| `config/` | Ordem de prioridade das fontes e sinônimos dos domínios de busca. |
| `src/esteiras_mcp/` | Código do servidor MCP. |
| `tests/` | Testes do pacote (`python -m pytest -q`). |
