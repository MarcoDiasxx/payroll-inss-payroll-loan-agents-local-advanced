# Comparativo de atividades e fluxos: esteiras 5003 e 6014

Data da analise: 26/10/2026.

## 1. Resumo do cenario

Objetivo: identificar qual esteira apresenta melhor estrutura de execucao e medir a similaridade entre suas atividades e seus fluxos, desconsiderando mudancas de nomes e numeros.

Foram analisados integralmente, por parser XML, somente os dois anexos fornecidos:

| Identificacao | Arquivo de entrada | DataHora declarada no XML |
| --- | --- | --- |
| 5003 | Esteira5003(1).xml | 2026-10-23T14:19:00 |
| 6014 | Esteira6014.xml | 2023-03-10T13:30:00 |

Diretorio dos anexos: /Users/idd_mdias/Downloads.

Contexto funcional declarado nos anexos: INSS, canal App, refinanciamento relacionado a portabilidade. A classificacao funcional nao foi inferida exclusivamente dos codigos das esteiras. A data declarada no XML nao comprova vigencia, homologacao ou implantacao.

Nao foram usados outros XMLs como modelo para a comparacao. Diferencas de nomenclatura, faixas de numeracao ou codigo da esteira nao receberam pontuacao positiva ou negativa. Os numeros aparecem neste documento apenas para localizar evidencias.

## 2. Conclusao executiva

**A 5003 e a melhor base quanto a integridade das referencias internas, mas nao foi demonstrado que seja a melhor esteira para executar a operacao completa.**

Ela nao possui destinos inexistentes e tem menos atividades nao alcancaveis desde a entrada. Entretanto, sua atividade explicita de liberacao de credito nao recebe nenhuma rota, e nao existe processo RECALCREFIN declarado.

**A 6014 preserva processos explicitos e alcancaveis de recalculo de refinanciamento e liberacao de credito, mas possui quatro referencias a destinos inexistentes.**

Recomendacao: utilizar a 5003 como candidata a base de evolucao somente depois de esclarecer o recalculo e corrigir ou justificar o percurso de pagamento. Preservar a 6014 como referencia comparativa desses processos nao significa copiar suas rotas nem considera-la homologada.

Nenhuma das duas deve ser considerada pronta para implantacao a partir desta analise.

## 3. Estado da validacao

**CUIDADO**.

Motivos: referencias quebradas na 6014, liberacao de credito desconectada na 5003 e equivalencia funcional do recalculo nao demonstrada.

A analise e estatica. Nao houve importacao, execucao de procedures, teste funcional, homologacao ou alteracao dos XMLs.

## 4. Similaridade e metodo

| Dimensao | Elementos na 5003 | Elementos na 6014 | Correspondencias | Similaridade |
| --- | ---: | ---: | ---: | ---: |
| Atividades por processo e condicao | 124 | 110 | 85 | **72,6%** |
| Transicoes de aprovacao verdadeira/falsa | 151 | 149 | 44 | **29,3%** |
| Todas as transicoes declaradas | 504 | 459 | 249 | **51,7%** |

**Para a pergunta sobre similaridade do fluxo, o indicador principal e 29,3%.** Os 72,6% expressam semelhanca dos componentes, nao da ordem em que sao executados. As rotas genericas de pendencia, reprovacao e cancelamento contribuem para elevar o indicador de todas as transicoes a 51,7%.

Foi usado o coeficiente Dice:

```text
Similaridade (%) = 100 x (2 x correspondencias) / (total da 5003 + total da 6014)

Atividades:           100 x 170 / 234 = 72,6496%
Aprovacoes:           100 x  88 / 300 = 29,3333%
Todas as transicoes:  100 x 498 / 963 = 51,7134%
```

### Normalizacao

- A assinatura de uma atividade considera Processo e CondicaoAprovada.
- Descricoes e numeros identificadores nao compoem a assinatura.
- Espacos consecutivos e diferencas entre maiusculas e minusculas foram normalizados para a comparacao textual.
- Referencias numericas em predicados EPNRDECI de igualdade ou IN foram substituidas por um marcador, evitando penalizar renumeracoes nesses trechos.
- Parametros numericos de negocio, limites financeiros e limites de tentativas nao foram descartados.
- Cada transicao considera assinatura da origem, tipo da rota e assinatura do destino.
- Destinos separados por ponto e virgula foram contados individualmente.
- As cinco rotas examinadas foram AprovadoVerdadeiro, AprovadoFalso, Reprovado, Pendente e Cancelado.
- As correspondencias foram contadas por multiconjuntos: a quantidade comum de cada assinatura e o menor numero de ocorrencias entre os arquivos.

### Limites da medida

Os percentuais abrangem todas as atividades e transicoes declaradas, inclusive trechos nao alcancaveis desde a entrada. A alcancabilidade foi avaliada separadamente.

Atividades diferentes podem compartilhar Processo e CondicaoAprovada, especialmente AUTAPR com VERDADEIRO. Portanto, a medida agrupa assinaturas semelhantes e nao estabelece um de-para individual e inequivoco entre todas as atividades. Tambem nao comprova isomorfismo dos grafos ou equivalencia das regras executadas.

A normalizacao textual do SQL nao e uma prova de equivalencia semantica. O calculo nao inclui alcadas, fases, TipoAcao, parametros e configuracoes de processo, telas, efeitos externos ou configuracoes de push. Esses elementos podem alterar a execucao real, mesmo quando as assinaturas coincidem.

O percentual mede semelhanca estrutural local, nao cobertura de testes nem probabilidade de funcionamento.

## 5. Itens validados

| Item | Encontrado: 5003 | Encontrado: 6014 | Esperado / criterio | Status e recomendacao |
| --- | --- | --- | --- | --- |
| XML bem-formado | Sim | Sim | Leitura integral pelo parser | ATENDIDO; nao equivale a validacao XSD |
| NumeroDecisao duplicado | 0 | 0 | Nenhuma duplicidade | ATENDIDO |
| Destinos inexistentes | 0 | 4 referencias | Nenhuma referencia quebrada | ATENDIDO na 5003; NAO ATENDIDO na 6014 |
| Configuracoes de processo referenciadas | Nenhuma referencia ausente | Nenhuma referencia ausente | Codigo nao zero presente na secao de configuracoes | ATENDIDO apenas quanto a existencia local |
| Atividades alcancaveis desde a entrada | 101 de 124 | 79 de 110 | Avaliar cada trecho no contexto de execucao | Verificar os trechos nao alcancaveis e entradas externas |
| Atividades nao alcancaveis desde a entrada | 23 | 31 | Ausencias de percurso justificadas | NAO VALIDADO funcionalmente; nao excluir automaticamente |
| Processo LBATBKTES | Presente, sem rota de entrada | Presente e alcancavel | Pagamento no percurso aplicavel | NAO ATENDIDO no grafo interno da 5003; execucao real nao testada |
| Processo RECALCREFIN | Nao declarado | Declarado e alcancavel | Confirmar o recalculo aplicavel a operacao | NAO VALIDADO quanto a equivalencia na 5003 |

Evidencias: elementos Decisoes/DecisaoExportacao, seus processos e rotas, e codigos da secao ConfiguracaoProcessoExportacao dos anexos.

Alcancabilidade: busca a partir da decisao 0, seguindo as cinco classes de rota, sem executar condicoes. Uma atividade alcancavel no grafo pode depender de um resultado ou evento que nunca ocorra em ambiente. Uma atividade nao alcancavel pode ser acionada externamente, mas isso nao foi comprovado.

## 6. Divergencias encontradas

### 6.1. CRITICA: liberacao de credito desconectada na 5003

- Evidencia: a decisao 700 usa LBATBKTES e nao e destino de nenhuma das cinco classes de rota examinadas.
- A decisao 224 executa BRK_VALIDA_LIBERACAO_AUTBANK e envia tanto AprovadoVerdadeiro quanto AprovadoFalso diretamente a 800.
- A decisao 800 usa REMESSSPROCCOMP, correspondente a integracao backoffice.
- Impacto: o grafo interno permite chegar ao backoffice sem passar pela atividade explicita de liberacao de credito.
- Limite da conclusao: nao foi verificado se alguma procedure ou integracao realiza o pagamento fora dessa atividade. Nao e possivel afirmar que nenhum pagamento ocorre em ambiente.
- Recomendacao: confirmar o contrato da procedure e o percurso de liberacao antes de definir qualquer nova rota.

### 6.2. CRITICA: destinos inexistentes na 6014

| Origem | Processo da origem | Campo | Destino ausente |
| --- | --- | --- | --- |
| 4 | CNANMT | Reprovado | 966 |
| 5 | CONSMARG | AprovadoFalso | 8 |
| 9 | AVERBPROPOSTA | AprovadoFalso | 8 |
| 11 | RETAVERBPROP | AprovadoFalso | 16 |

Sao quatro referencias quebradas para tres numeros de destino distintos. Nao foram descartadas porque um campo CondicaoAprovada contem VERDADEIRO: a semantica de cada processo precisa ser considerada antes de declarar uma rota inexecutavel.

Impacto: as rotas nao podem ser resolvidas internamente para atividades existentes. A origem 4 tambem nao e alcancavel desde 0 pelas rotas declaradas, mas a referencia permanece estruturalmente quebrada.

Recomendacao: recuperar os destinos corretos ou justificar formalmente a retirada de cada rota. Nao inferir destinos pela proximidade numerica.

### 6.3. CUIDADO: recalculo nao demonstrado como equivalente

- Na 6014, a decisao 310 usa RECALCREFIN e e alcancavel desde a entrada.
- Na 5003, nao existe atividade com Processo igual a RECALCREFIN. Existem atividades RECALCVCTO.
- Impacto potencial: uma funcao explicita da 6014 pode nao ter equivalente comprovado na 5003.
- Nao foi presumido que RECALCVCTO substitui RECALCREFIN nem que sua ausencia isolada viola uma regra universal para toda operacao.
- Recomendacao: confirmar aplicabilidade, momento e implementacao do recalculo antes de concluir equivalencia.

### 6.4. CUIDADO: atividades nao alcancaveis nas duas esteiras

A 5003 possui 23 e a 6014 possui 31 atividades nao alcancaveis desde 0 no grafo declarado. Esse resultado nao identifica, por si so, atividades dispensaveis.

Recomendacao: confrontar cada trecho com acionamentos externos, eventos de assinatura, robos e integracoes antes de remover ou reconectar atividades.

## 7. Qual esta melhor

| Criterio | Resultado | Justificativa |
| --- | --- | --- |
| Integridade das referencias de rota | 5003 | Zero destinos inexistentes, contra quatro referencias quebradas |
| Menor quantidade de atividades nao alcancaveis | 5003 | 23 contra 31, sem considerar acionamentos externos |
| Presenca de recalculo explicito RECALCREFIN | 6014 | Processo declarado e alcancavel; equivalencia na 5003 nao comprovada |
| Conexao da atividade explicita de liberacao | 6014 | LBATBKTES alcancavel; na 5003 nao recebe rotas |
| Execucao ponta a ponta comprovada | Nenhuma | Nao houve teste em ambiente |

**Parecer:** a 5003 apresenta melhor integridade local para servir de base de evolucao. A 6014 preserva melhor os processos explicitos de recalculo e liberacao. Nao ha evidencia suficiente para declarar uma vencedora irrestrita em execucao funcional completa.

As diferencas sao de comportamento e conexao, nao apenas de novos numeros e nomes.

## 8. Alteracoes recomendadas

| Situacao atual | Resultado a buscar | Condicao para alterar |
| --- | --- | --- |
| 5003: validacao encaminha diretamente ao backoffice e LBATBKTES esta isolado | Percurso de pagamento confirmado e coerente com a integracao | Confirmar implementacao externa e roteamento oficial; nao inserir destino por suposicao |
| 5003: ausencia de RECALCREFIN explicito | Equivalencia do recalculo demonstrada ou fluxo ajustado | Confirmar a regra aplicavel e os efeitos dos processos existentes |
| 6014: quatro referencias quebradas | Destinos existentes e funcionalmente corretos | Recuperar evidencia do roteamento esperado |
| Ambas: atividades nao alcancaveis desde 0 | Trechos justificados, conectados ou removidos conforme evidencia | Identificar acionamentos externos e comportamento esperado |

Este documento nao aplica essas alteracoes. Os XMLs de entrada permanecem preservados.

## 9. Referencias consultadas

### Evidencias diretas da comparacao

- Os dois XMLs anexados, lidos integralmente por parser durante esta sessao.
- [Politica core](../core/esteiras-core-policy.md), lida integralmente e relida na geracao deste documento.

### Referencias oficiais recuperadas na etapa anterior desta mesma sessao

- Jira [BRGN-3563](https://jiraps.atlassian.net/browse/BRGN-3563): [FUNCAO-INSS] Padronizacao, Higienizacao e Evolucao das Esteiras de INSS; atualizado em 26/10/2026, 10:01:44 -0300.
- Confluence [Esteiras Funcao, ID 77048086725](https://jiraps.atlassian.net/wiki/spaces/BRGN/pages/77048086725): versao 2. A data da versao nao foi registrada no resumo recuperado.
- [Planilha oficial local](../reference/Esteiras_Funcao-Grupos_de_Atividades-Alcadas_e_Fases.xlsx): aba GrpAtvds+FasesAlcadas-Esteiras, linha 11; aba Atividades-Esteiras, linhas 87, 88, 89 e 96, na consulta por Delphos. Essas linhas nao constituem auditoria de todas as atividades.
- get_core_references retornou complete=true na etapa anterior. As referencias remotas nao foram novamente consultadas apenas para redigir este documento.

As referencias oficiais foram recuperadas para contexto e governanca. Os percentuais e achados estruturais foram calculados exclusivamente sobre os dois anexos; nao representam declaracao de aderencia integral as fontes oficiais.

### Pesquisas complementares realizadas na etapa anterior

- discover_domain_knowledge para refin_de_portabilidade.
- search_jira_esteiras com os termos refin de portabilidade, refin port e refin da port.
- search_confluence_esteiras por refin de portabilidade.
- lookup_official_activity por Delphos.

Nao foi registrada indisponibilidade de fonte core no retorno resumido. Nao foram consultados catalogo vigente de Message Center, ambiente de execucao ou corpo das procedures. Nenhum dos anexos foi tratado como XML homologado, pois essa condicao nao foi comprovada.

## 10. Impactos externos

| Componente | Limite / impacto a verificar |
| --- | --- |
| Procedures | Confirmar efeitos de recalculo, validacao de liberacao e eventuais pagamentos fora do grafo |
| AutBank / pagamento | Confirmar liberacao efetiva, retorno e conta de destino |
| Backoffice | Confirmar integracao somente no momento correto do fluxo de credito |
| Message Center / pushes | Rotas no XML nao comprovam template, evento, envio ou configuracao vigente |
| Produtos, convenios e anuencia | Parametrizacao e aplicabilidade nao verificadas |
| Tracking, CRM, robos e plugins | Confirmar acionamentos externos e efeitos nos trechos nao alcancaveis |
| Assinatura e demais integracoes | Confirmar pontos de entrada e eventos que nao aparecem como rotas internas |

Nenhuma parametrizacao externa foi alterada ou declarada aplicada.

## 11. Pendencias bloqueantes

Bloqueiam validacao final ou implantacao, nao a entrega deste comparativo:

1. Resolver ou justificar formalmente as quatro referencias quebradas da 6014.
2. Confirmar e ajustar, quando necessario, o percurso de pagamento da 5003.
3. Demonstrar equivalencia ou aplicabilidade distinta do recalculo entre os fluxos.
4. Validar entradas externas e atividades nao alcancaveis antes de higienizacao.
5. Executar testes dos caminhos aplicaveis, incluindo aprovacoes, reprovacoes, pendencias, cancelamentos, recalculo, pagamento e backoffice.
6. Confirmar ambiente alvo, responsaveis, configuracoes externas e aprovacoes necessarias para eventual implantacao.

## 12. Artefatos gerados

- Este documento comparativo.
- Nenhum XML, SQL, setup de push ou configuracao externa foi criado ou modificado.
- Nao foram gerados XML final, backup, plano de rollback ou de-para individual, pois nao houve solicitacao de alteracao ou implantacao. As referencias numericas dos achados nao constituem um de-para completo.

## 13. Checklist DoR e DoD

| Item | Estado |
| --- | --- |
| Dois anexos identificados e analisados integralmente por parser | ATENDIDO |
| Nomes e numeros excluidos das assinaturas comparativas | ATENDIDO |
| Percentuais, formulas e limitacoes documentados | ATENDIDO |
| Duplicidades e destinos inexistentes verificados | ATENDIDO |
| Alcancabilidade estatica desde a entrada verificada | ATENDIDO |
| Referencias locais de configuracao de processo verificadas | ATENDIDO |
| Execucao real e equivalencia semantica das atividades | NAO VALIDADO |
| Validacao por XSD e auditoria integral de alcadas, fases e protecoes | NAO VALIDADO |
| Loops sem saida e finalizacao de todos os caminhos funcionais | NAO VALIDADO |
| Procedures, Message Center, produtos, convenios e tracking | NAO VALIDADO |
| CRM, robos, plugins e integracoes externas | NAO VALIDADO |
| Recalculo, pagamento e conta beneficio confirmados em ambiente | NAO VALIDADO |
| Testes funcionais e importacao no ambiente alvo | NAO VALIDADO |
| Resolucao das divergencias criticas identificadas | NAO ATENDIDO |
| Geracao ou alteracao de XML, SQL, setup e rollback nesta entrega | NAO APLICAVEL |
| Condicoes para considerar qualquer esteira pronta para implantacao | NAO ATENDIDO |