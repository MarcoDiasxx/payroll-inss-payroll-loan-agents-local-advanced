# Seguranca

- Revogue qualquer token exposto em conversa, log ou commit.
- Use token individual, com menor escopo e validade possiveis.
- Nunca versione `.env`.
- O servidor implementa apenas metodos GET.
- O token herda as permissoes da identidade Atlassian.
- Para uso organizacional centralizado, prefira OAuth 2.0/3LO ou conta de servico com governanca.
- Revise dependencias e o codigo MCP antes de autorizar sua execucao no VS Code.
