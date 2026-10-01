# Rastreabilidade das divergências — matriz v0.3

| Divergência | Tratamento aprovado na proposta | Artefatos afetados | Verificação prevista | Estado |
|---|---|---|---|---|
| DIV-01 | `execucao_id` torna-se FK operacional; evidências mantêm `exp` por pertencimento forense e `execucao_id` opcional | matriz, dicionário, validador | Toda FK resolve; coerência `evidencia.exp = execucao.exp` | resolvida no modelo |
| DIV-02 | Inclusão de `idempotencia_id` e `reproducao_id` como PKs | abas e dicionário | PK obrigatória, única e não vazia | resolvida no modelo |
| DIV-03 | Criação de `custodia_eventos`, `manifestos` e `manifesto_evidencias`, com fase ISO/IEC 27037 explícita | matriz, dicionário, protocolo | Toda evidência selada possui manifesto e eventos de identificação/coleta/aquisição/preservação aplicáveis | resolvida no escopo experimental |
| DIV-04 | Substituição de `Divergẽncia_ID` por `divergencia_id` | cabeçalhos e dicionário | correspondência exata de nomes | resolvida no modelo |
| DIV-05 | Nomes técnicos sem acentos; `execucoes` usado de forma uniforme | todas as abas | conjunto de nomes permitido por regex | resolvida no modelo |
| DIV-06 | Inclusão condicional de `scenario_id`, `attack_id`, `baseline_id` e hash da DOML | `experimentos` e protocolo | regras condicionais por tipo de experimento | resolvida no modelo |
| DIV-07 | Adicionar `secret_ref` à especificação executável/JSON Schema | DOML-F schema, especificação e testes | exemplo válido e casos negativos sem segredo em claro | pendente fora da matriz |
| DIV-08 | `ansible_versao` e `criticidade` deixam de ser FKs | dicionário | alvos de FK pertencem a PK/UK declarada | resolvida no modelo |
| DIV-09 | Domínios iniciais e regras derivados definidos na especificação | dicionário e validação de dados | nenhum campo do tipo domínio sem conjunto ou referência | parcialmente resolvida; detalhar na geração |
| DIV-10 | Uso uniforme de `resultado_consolidado` | `resultados` e dicionário | correspondência exata | resolvida no modelo |
| DIV-11 | Preservar v0.2, criar v0.3 e versionar artefatos/diretórios | repositório | estado Git limpo e diretórios operacionais rastreados | pendente no repositório |

## Divergências adicionais reveladas pela normalização

| ID | Problema | Correção proposta | Estado |
|---|---|---|---|
| DIV-12 | `execucoes` mistura uma execução com seus eventos | criar `eventos_execucao` | resolvida no modelo |
| DIV-13 | Validação pré-voo e validação experimental compartilham uma única semântica implícita | separar `validacoes_modelo` e `validacoes_execucao` | resolvida no modelo |
| DIV-14 | A antiga aba `divergencias` representa alteração deliberada | renomear semântica para `testes_deteccao` e criar drift real | resolvida no modelo |
| DIV-15 | `metricas` mistura definição e observação | separar `metricas`, `medicoes` e `resultados` | resolvida no modelo |
| DIV-16 | Campos booleano/texto não possuem tipo determinístico | dividir valor booleano e descrição | resolvida no modelo |
| DIV-17 | Durações digitadas podem divergir dos timestamps | derivar em milissegundos | resolvida no modelo |
| DIV-18 | ODS manual não preserva precisão e consistência durante a execução | JSONL validado torna-se fonte primária; ODS passa a ser exportação | resolvida no modelo; implementação pendente |
| DIV-19 | Atores registrados como strings não resolvem para identidade AAA | criar `identidades_atores` e FKs `ator_id` | resolvida no modelo; integração pendente |
| DIV-20 | UTC isolado pode gerar duração incorreta após ajuste de relógio | capturar relógio monotônico e derivar durações | resolvida no modelo; implementação pendente |
| DIV-21 | Ausência de plano amostral permite `N` arbitrário e pseudorreplicação | piloto, regra de precisão, piso/teto e desenho pareado | resolvida no modelo; protocolo pendente |
| DIV-22 | Stream único exige sequenciador central e cria ponto único de falha | streams independentes por instância/boot e ledger separado | resolvida no modelo; implementação pendente |
| DIV-23 | Nanossegundos podem exceder inteiros exatos de I-JSON | representar contadores como strings decimais | resolvida no contrato |
| DIV-24 | Correções posteriores poderiam sobrescrever o registro original | criar `record.corrected` e projeção `correcoes_registro` | resolvida no modelo; implementação pendente |
| DIV-25 | Linhas ODS não indicariam exatamente qual evento as originou | mapa normativo e campos técnicos de proveniência | resolvida no modelo; dicionário pendente |

## Critério de encerramento

Uma divergência somente será marcada como encerrada após:

1. alteração aplicada ao artefato correspondente;
2. regra correspondente incluída no dicionário ou schema;
3. teste automático implementado quando tecnicamente verificável;
4. resultado do teste registrado sem erro.

Para DIV-18 a DIV-25, o encerramento também exige teste integrado do pipeline, resolução das identidades contra AAA, validação JCS/hash, teste de falha/reinício de streams, projeção reproduzível e execução do piloto estatístico.

Assim, “resolvida no modelo” significa que a decisão foi definida, mas ainda depende de implementação na matriz v0.3.
