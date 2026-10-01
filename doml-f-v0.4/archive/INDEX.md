# Índice documental DOML-F / Matriz experimental

## 1. Normativos

Devem ser lidos antes de alterar schema, semântica ou cardinalidade.

| Documento | Função | Estado |
|---|---|---|
| `DOML-F-SPEC-v0.1.md` | linguagem declarativa | existente; correções pendentes |
| `DOML-F-EVENT-CONTRACT-v0.1.md` | contrato observacional JSONL | proposta consolidada |
| `doml-f-event.schema.json` | validação sintática dos eventos | proposta executável |
| `modelo-matriz-v0.3.md` | modelo relacional da projeção | proposta consolidada |
| `decisoes-metodologicas-v0.3.md` | decisões DM-001 a DM-029 | atualizado |

## 2. Executáveis

| Artefato | Função | Estado |
|---|---|---|
| `domlf_validator/` | validação por camadas | núcleo implementado |
| `event-projection-map-v0.1.yaml` | evento para entidade/aba | primeira versão |
| `pyproject.toml` | dependências e CLI | definido |
| `tests/` | regressão automatizada | núcleo estrutural coberto |

## 3. Exemplos

| Artefato | Função | Limite |
|---|---|---|
| `exemplo-execucao-v0.1.jsonl` | demonstra streams, ledger, correção e manifesto | hashes didáticos; ledger abreviado |
| `doml-f.example.yaml` | exemplo declarativo | precisa ampliar cobertura |

## 4. Auditoria e evolução

| Documento | Função |
|---|---|
| `rastreabilidade-divergencias-v0.3.md` | DIV → decisão → verificação |
| `migracao-v0.2-v0.3.md` | preservação e transformação estrutural |
| `relatorio_divergencias_forense.md` | diagnóstico de origem |

## 5. Históricos

- `matriz-experimental-v0.2.ods`: não utilizar para captura; preservar como referência histórica.
- Versões anteriores dos documentos v0.3: mantidas no histórico de versões.

## 6. Ordem de leitura para retomada

1. `docs/ROADMAP.md`;
2. `decisoes-metodologicas-v0.3.md`;
3. `DOML-F-EVENT-CONTRACT-v0.1.md`;
4. `modelo-matriz-v0.3.md`;
5. `event-projection-map-v0.1.yaml`;
6. `rastreabilidade-divergencias-v0.3.md`;
7. código e testes do validador.

