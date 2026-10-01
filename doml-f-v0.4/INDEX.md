# Índice documental DOML-F

## Entrada do projeto

| Documento | Função |
|---|---|
| `README.md` | visão geral, execução e estado do validador |
| `INDEX.md` | localização e autoridade dos artefatos |
| `ROADMAP.md` | decisões consolidadas, pendências e próximo marco |
| `DOCUMENTACAO_SISTEMA.md` | funções e características estruturadas do sistema e código |
| `CASOS_DE_USO_MUNDO_REAL.md` | casos de uso aplicados à prática pericial e segurança |
| `ARTIGO_CIENTIFICO_SBC.md` | proposta de artigo científico completo no formato SBC (v0.1 a v0.3) |
| `checklist.md` | checklist operacional de preflight, portões G01-G12 e execução do C01 |

## Documentos normativos e metodológicos

| Caminho | Função | Estado |
|---|---|---|
| `docs/requisitos/requisitos_refinados.md` | requisitos vigentes do MVP | atualizado para v0.3 |
| `docs/requisitos/requisitos_original.md` | escopo amplo original | histórico |
| `docs/especificacao/DOML-F-SPEC-v0.1.md` | linguagem declarativa | existente; revisão futura |
| `docs/especificacao/DOML-F-EVENT-CONTRACT-v0.1.md` | contrato observacional JSONL | proposta consolidada |
| `docs/especificacao/decisoes-metodologicas-v0.3.md` | decisões metodológicas | existente |
| `docs/protocolo/protocolo-experimental.md` | desenho do piloto | v0.3; C01 liberado para implementação |
| `docs/protocolo/cenarios.md` | procedimentos dos cenários | C01 determinístico; C02–C06 pendentes |
| `docs/protocolo/politica-evidencias.md` | retenção, custódia, NFS e capacidade | v0.3 consolidada |

## Contratos e modelos executáveis

| Caminho | Função | Estado |
|---|---|---|
| `schemas/doml-f.schema.json` | validação da descrição DOML-F | existente |
| `schemas/doml-f-event.schema.json` | validação sintática dos eventos | proposta executável |
| `models/modelo-matriz-v0.3.md` | modelo relacional da projeção | consolidado para geração |
| `models/event-projection-map-v0.1.yaml` | projeção evento → entidade | primeira versão preservada |
| `models/event-projection-map-v0.2.yaml` | extensão de projeção para C01/v0.3 | gerada; integrar ao motor |
| `models/matriz-experimental-v0.3.ods` | projeção humana com dicionário e pontos de coleta | gerada e validada estruturalmente |
| `src/domlf_validator/` | validação por camadas e projeção | implementação parcial |
| `pyproject.toml` | empacotamento, dependências e CLI | existente |

## Rastreabilidade e migração

| Caminho | Função |
|---|---|
| `docs/rastreabilidade/DOML-F-TRACEABILITY-v0.1.md` | rastreabilidade da especificação |
| `docs/rastreabilidade/rastreabilidade-divergencias-v0.3.md` | divergência → decisão → verificação |
| `docs/rastreabilidade/relatorio_divergencias_forense.md` | diagnóstico de origem |
| `docs/migracao/migracao-v0.2-v0.3.md` | transformação estrutural e preservação |

## Exemplos

| Caminho | Função | Limite |
|---|---|---|
| `examples/doml-f.example.yaml` | exemplo declarativo | ampliar cobertura |
| `examples/exemplo-execucao-v0.1.jsonl` | demonstra streams, ledger, correção e manifesto | hashes didáticos; ledger abreviado |

## Históricos

- `archive/modelo-v0.2.md`: modelo anterior; não editar como fonte vigente.
- `archive/matriz-experimental-v0.1.ods`: primeira matriz histórica.
- `archive/matriz-experimental-v0.2.ods`: não utilizar para nova captura.

## Estruturas ainda vazias ou incompletas

- `tests/unit/`, `tests/integration/`, `tests/fixtures/` e `tests/data/`: casos automatizados ainda não sincronizados.
- `ansible/`: inventários, playbooks, roles e variáveis ainda não implementados.
- `experiments/templates/` e `experiments/runs/`: aguardam templates e piloto.
- `analysis/`: scripts, notebooks e resultados ainda não produzidos.
- `LICENSE`: ausente; a licença do repositório ainda deve ser definida.

## Ordem de leitura para retomada

1. `README.md`;
2. `ROADMAP.md`;
3. `docs/requisitos/requisitos_refinados.md`;
4. `docs/especificacao/decisoes-metodologicas-v0.3.md`;
5. `docs/especificacao/DOML-F-EVENT-CONTRACT-v0.1.md`;
6. `models/modelo-matriz-v0.3.md`;
7. `models/event-projection-map-v0.1.yaml`;
8. `docs/protocolo/`;
9. código e testes do validador.
