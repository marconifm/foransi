# Mapa preliminar de migração — matriz v0.2 para v0.3

## 1. Estratégia

- A v0.2 permanece inalterada.
- A v0.3 será criada vazia a partir do modelo lógico aprovado.
- Como a v0.2 ainda não está populada, a migração principal é de estrutura, não de dados.
- Se surgirem linhas preenchidas antes da conversão, elas serão transformadas por script e registradas em relatório de migração.
- A v0.3 passa a ser alimentada por JSONL validado; a ODS resultante será uma projeção gerada, não a fonte primária operacional.

## 2. Mapeamento de abas

| v0.2 | v0.3 | Operação |
|---|---|---|
| `experimentos` | `experimentos` + `transicoes_experimento` | ampliar rastreabilidade e ciclo de vida |
| `ambiente` | `ambientes` | renomear e tipar campos |
| inexistente | `identidades_atores` | carregar identidades autorizadas a partir de referências Kerberos/OpenLDAP/SSH |
| `execucoes` | `execucoes` + `eventos_execucao` | separar granularidades |
| inexistente | `streams_eventos` | registrar cadeias dos emissores do contrato JSONL |
| inexistente | `ledger_eventos` | registrar ordem de aceitação pelo agregador |
| inexistente | `correcoes_registro` | preservar correções sem sobrescrita |
| `validacao` | `validacoes_execucao` | normalizar FK e nomes; criar separadamente `validacoes_modelo` |
| `idempotencia` | `idempotencia` | adicionar PK e normalizar FK |
| `reproducao` | `reproducao` | adicionar PK e normalizar FKs |
| `divergencias` | `testes_deteccao` | preservar a semântica de alteração introduzida; criar nova `divergencias` |
| `evidencias` | `evidencias` | manter `exp`, trocar ordinal por `execucao_id` opcional e tipar coleta |
| `anomalias` | `anomalias` | normalizar FK, domínio e vínculo opcional com evento |
| `metricas` | `metricas` + `medicoes` | separar definição de observação |
| `resultados` | `resultados` | adicionar PK, versão e timestamp de cálculo |
| inexistente | `custodia_eventos` | nova entidade |
| inexistente | `manifestos` | nova entidade |
| inexistente | `manifesto_evidencias` | nova entidade associativa |
| `dicionario` | `dicionario` | reconstruir a partir da especificação v0.3 |

## 3. Transformações críticas

### 3.1 `execucoes`

Cada combinação distinta de `Execução_ID` da v0.2 gera uma linha em `execucoes`. Cada linha original da aba gera uma linha em `eventos_execucao`.

| Campo v0.2 | Destino v0.3 | Regra |
|---|---|---|
| `Execução_ID` | `execucoes.execucao_id` | preservar valor |
| `EXP` | `execucoes.exp` | preservar valor |
| ausente | `execucoes.numero_execucao` | extrair de convenção ou atribuir sequencialmente com relatório |
| `Etapa` | `eventos_execucao.etapa` | preservar |
| `Timestamp` | `eventos_execucao.timestamp_inicio_utc` | normalizar UTC |
| `Fase` | `eventos_execucao.fase` | mapear domínio |
| `Ação` | `eventos_execucao.acao` | preservar |
| `Resultado` | `eventos_execucao.resultado` | mapear domínio |
| `Duração` | `eventos_execucao.duracao_ms` | converter unidade; marcar como legado se não houver timestamp final |
| `Intervenção` | `eventos_execucao.intervencao` e descrição | decompor booleano e texto |
| `Observação` | `eventos_execucao.observacao` | preservar |

### 3.2 FKs compostas legadas

Nas abas `validacao`, `idempotencia`, `divergencias`, `evidencias` e `anomalias`, a combinação (`EXP`, `Execução`) será resolvida para um único `execucao_id`. Registros sem correspondência única serão rejeitados e enviados a relatório de pendências; nunca haverá escolha silenciosa.

### 3.3 Evidências

| Campo v0.2 | Campo v0.3 |
|---|---|
| `Evidência_ID` | `evidencia_id` |
| `EXP` | `exp` |
| `Execução` | resolver para `execucao_id`; opcional se vazio |
| `Timestamp` | `coletada_em_utc` |
| `Tipo` | `tipo` |
| `Origem` | `origem` |
| `Caminho` | `caminho` |
| `Formato` | `formato` |
| `Tamanho` | `tamanho_bytes` |
| `Hash` | `hash` |
| `Algoritmo` | `algoritmo_hash` |
| `Integridade` | `estado_integridade` |

`metodo_coleta` não possui equivalente seguro na v0.2 e deverá ser informado ou marcado como pendência; não será inferido apenas pelo formato do arquivo.

Os campos `fase_iso_27037`, `procedimento`, `versao_ferramenta`, `hash_antes` e `hash_depois` também não possuem equivalentes seguros e não serão inferidos retroativamente sem evidência.

### 3.4 Divergências

As linhas da antiga aba `divergencias` irão para `testes_deteccao`, porque contêm `Alteração introduzida`. Nenhuma linha será convertida automaticamente para a nova entidade `divergencias` de drift.

### 3.5 Métricas

Para cada definição conceitualmente distinta será criada uma linha em `metricas`. Os valores observados, numerador e denominador irão para `medicoes`. Ambiguidades de definição ou versão serão listadas para revisão.

## 4. Campos que exigem preenchimento novo

- `experimentos.estado_atual`
- `experimentos.doml_hash`
- `experimentos.responsavel_id`
- `identidades_atores` e referências `ator_id`
- `execucoes.numero_execucao`
- timestamps de início/fim da execução, quando inexistentes
- `evidencias.metodo_coleta`
- versões de cálculo de resultados
- atores e ações da trilha de custódia
- fases ISO/IEC 27037 aplicáveis aos eventos de custódia
- referências de autenticação e fingerprints, sem copiar segredos
- identidades, sequências e hashes terminais de cada stream
- referências do ledger e eventos de correção
- campos de proveniência dos eventos e versão do mapa de projeção

## 5. Regras contra perda silenciosa

1. Toda coluna v0.2 deve possuir destino, justificativa de descarte ou registro de pendência.
2. Valores não reconhecidos em domínio não serão corrigidos automaticamente.
3. Datas sem fuso não serão presumidas como UTC sem registrar a convenção usada.
4. Duração legada permanecerá identificada como observada quando não puder ser recalculada.
5. A migração produzirá contagens de entrada, saída, rejeição e pendência por aba.
6. Texto legado de ator não será convertido automaticamente em identidade autenticada; exigirá resolução explícita.
7. Tempos legados sem contador monotônico serão marcados como duração observada não verificável pelo novo método.

## 6. Condição atual

A matriz v0.2 inspecionada contém cabeçalhos e dicionário, mas não contém dados experimentais nas abas. Portanto, a criação da v0.3 pode ocorrer sem transformação de registros neste momento. Este mapa permanece necessário para rastreabilidade estrutural e para eventual importação futura.
