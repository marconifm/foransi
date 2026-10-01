# Contrato de eventos DOML-F v0.1

**Estado:** proposta para revisão  
**Formato:** JSON Lines (`.jsonl`)  
**Schema:** JSON Schema Draft 2020-12  
**Relação com DOML-F:** contrato observacional independente; não altera o estado desejado

## 1. Objetivo

O contrato define como orquestrador, callback Ansible, coletores, validadores e selador registram fatos ocorridos durante um experimento. Cada linha contém exatamente um objeto JSON completo, sem arrays externos e sem formatação multilinha.

A DOML-F declara o que deve existir e ocorrer. O JSONL registra o que efetivamente existiu e ocorreu. A ODS v0.3 e um futuro banco SQL são projeções derivadas desses eventos.

## 2. Princípios

1. **Imutabilidade:** evento aceito não é sobrescrito; correções geram novo evento.
2. **Validação prévia:** cada linha deve validar contra `doml-f-event.schema.json` antes de entrar no fluxo oficial.
3. **Identidade:** todo evento possui UUID e contexto de experimento.
4. **Ordenação local:** `stream_sequence` é estritamente crescente dentro de cada stream emissor.
5. **Tempo duplo:** UTC serve à correlação; relógio monotônico serve a durações dentro da mesma origem.
6. **Autoria autenticada:** todo emissor usa `actor_id` resolvível em `identidades_atores`.
7. **Encadeamento:** cada evento registra o hash do anterior no mesmo stream; streams diferentes nunca compartilham cadeia.
8. **Minimização:** tickets, chaves privadas, senhas, tokens e segredos nunca aparecem no evento.
9. **Reprodutibilidade:** versões do contrato, DOML-F, software emissor e commit acompanham o registro.
10. **Separação:** políticas permanecem na DOML-F; resultados observados permanecem no fluxo de eventos.

## 3. Unidade de armazenamento

Exemplo físico:

```jsonl
{"schema_version":"0.1.0","event_id":"018f0000-0000-7000-8000-000000000001","event_type":"execution.started","stream":{"stream_id":"STR-ORCH-01","emitter_type":"orchestrator","emitter_instance_id":"orchestrator-controller-01","host":"controller-01","boot_id":"boot-a"},"stream_sequence":1,"emitted_at_utc":"2026-09-20T12:00:00.000Z","monotonic_ns":"1000000000","source":{"emitter":"orchestrator","host":"controller-01","process_id":4200,"software_version":"0.1.0"},"context":{"exp":"EXP-001","execucao_id":"EXEC-001","doml_model_id":"lab-forense-01","doml_version":"0.1.0","doml_hash":"sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","commit":"0123456789abcdef0123456789abcdef01234567"},"actor":{"ator_id":"ACT-SVC-ORCH","principal":"forensic-orchestrator@LAB.LOCAL","authentication_method":"KERBEROS_SSH","ssh_key_fingerprint":"SHA256:example"},"integrity":{"algorithm":"SHA-256","previous_event_hash":null,"event_hash":"bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},"payload":{"numero_execucao":1,"status":"EM_EXECUCAO","inicio_monotonico_ns":"1000000000"}}
```

Os hashes do arquivo de exemplo são valores didáticos com formato válido e encadeamento consistente; não representam o resultado real da canonicalização. Para manter o exemplo legível, o ledger demonstra somente duas aceitações. O arquivo é um exemplo estrutural, não uma fixture criptográfica ou uma execução integralmente ledgerizada. Os testes definitivos serão realizados pelo gerador/validador do contrato.

## 4. Envelope comum

| Campo | Obrigatório | Semântica |
|---|---:|---|
| `schema_version` | sim | versão do contrato de eventos |
| `event_id` | sim | UUID do evento |
| `event_type` | sim | tipo normativo do evento |
| `stream` | sim | identidade estruturada da instância emissora |
| `stream_sequence` | sim | número local crescente, iniciado em 1 |
| `emitted_at_utc` | sim | instante UTC ISO 8601 |
| `monotonic_ns` | sim | leitura monotônica como string decimal |
| `source` | sim | componente que materializou o evento |
| `context` | sim | referências ao experimento e modelo |
| `actor` | sim | identidade autenticada responsável |
| `integrity` | sim | hash atual e hash anterior |
| `correlation_id` | não | correlação entre eventos distribuídos |
| `causation_id` | não | `event_id` que causou diretamente este evento |
| `payload` | sim | dados específicos do tipo |

### 4.1 `source`

```json
{
  "emitter": "ansible_callback",
  "host": "controller-01",
  "process_id": 4200,
  "software_version": "0.1.0"
}
```

`monotonic_ns` somente pode ser comparado quando `source.host` e o processo/boot de referência forem compatíveis. Durações distribuídas não devem ser calculadas pela subtração de relógios monotônicos de hosts diferentes.

### 4.2 `stream`

Cada instância emissora possui cadeia própria. A identidade contém `stream_id`, `emitter_type`, `emitter_instance_id`, `host` e `boot_id`. Reinício do host/processo, perda do último hash ou perda do contador de sequência exige novo `stream_id`; nunca se reinicia a sequência de um stream existente.

### 4.3 `context`

Campos obrigatórios: `exp`, `doml_model_id`, `doml_version`, `doml_hash`, `commit`. `execucao_id` é obrigatório nos eventos pertencentes a uma execução. `evento_id` é usado quando houver correspondência direta com `eventos_execucao`.

### 4.4 `actor`

Campos obrigatórios: `ator_id`, `principal`, `authentication_method`. Fingerprints são incluídos quando o método utilizar chave SSH ou certificado. O contrato não armazena material secreto.

### 4.5 `integrity`

`event_hash` é calculado sobre a representação canônica do evento com `integrity.event_hash` e `integrity.signature` removidos. O algoritmo inicial é SHA-256. `previous_event_hash` é `null` somente no primeiro evento do stream.

A implementação adota JSON Canonicalization Scheme (JCS/RFC 8785). O parser deve rejeitar chaves duplicadas, números não finitos, `-0` e inteiros fora do intervalo seguro de I-JSON. Contadores em nanossegundos são strings decimais para evitar perda acima de `2^53-1`. O texto é UTF-8 e não recebe normalização Unicode adicional fora das regras do JCS.

## 5. Ledger da execução

Streams emissores preservam a ordem local, mas não criam ordem física total entre hosts. O agregador mantém um stream próprio de ledger com eventos `ledger.event.accepted`. Cada entrada registra `ledger_sequence`, instante de recebimento, stream/posição de origem, `event_id` e `event_hash` aceitos.

O ledger prova a ordem de aceitação, não uma ordem física absoluta. A reconstrução utiliza, nesta ordem: cadeia local do stream, `causation_id`, ledger de ingestão e timestamps UTC como correlação auxiliar.

## 6. Tipos de evento v0.1

| Tipo | Emissor típico | Projeção principal |
|---|---|---|
| `experiment.transitioned` | orquestrador | `transicoes_experimento` |
| `execution.started` | orquestrador | `execucoes` |
| `execution.step.started` | callback Ansible | `eventos_execucao` |
| `execution.step.finished` | callback Ansible | `eventos_execucao` |
| `evidence.registered` | coletor | `evidencias` |
| `custody.recorded` | coletor/selador | `custodia_eventos` |
| `measurement.recorded` | medidor/orquestrador | `medicoes` |
| `validation.completed` | validador | `validacoes_modelo` ou `validacoes_execucao` |
| `anomaly.recorded` | orquestrador/analista | `anomalias` |
| `divergence.detected` | comparador | `divergencias` |
| `detection_test.completed` | orquestrador | `testes_deteccao` |
| `manifest.sealed` | selador | `manifestos` e `manifesto_evidencias` |
| `execution.completed` | orquestrador | `execucoes` |
| `ledger.event.accepted` | agregador | `ledger_eventos` |
| `record.corrected` | emissor autorizado/analista | `correcoes_registro` |

## 7. Payloads mínimos

### `experiment.transitioned`

`transicao_id`, `estado_anterior`, `estado_novo`, `motivo` opcional e `evidencia_id` opcional.

### `execution.started`

`numero_execucao`, `status=EM_EXECUCAO`, `inicio_monotonico_ns` como string decimal e referências opcionais `scenario_id`, `attack_id`, `baseline_id`.

### `execution.step.started`

`evento_id`, `etapa`, `fase`, `acao`, `inicio_monotonico_ns` como string decimal e `relogio_origem`.

### `execution.step.finished`

`evento_id`, `resultado`, `fim_monotonico_ns` como string decimal, `duracao_ms`, `intervencao` e descrição condicional.

### `evidence.registered`

`evidencia_id`, `metodo_coleta`, `tipo`, `descricao`, `origem`, `caminho`, `formato`, `tamanho_bytes`, `hash`, `algoritmo_hash` e `estado_integridade`.

### `custody.recorded`

`evento_custodia_id`, `evidencia_id`, `fase_iso_27037`, `acao`, `procedimento`, `ferramenta`, `versao_ferramenta`, hashes anterior/posterior e resultado de integridade.

### `measurement.recorded`

`medicao_id`, `metrica_id`, `valor`, `unidade`, `fonte`; numerador e denominador são opcionais.

### `validation.completed`

`validation_scope` (`MODELO` ou `EXECUCAO`), identificador da validação, tipo, resultado, contagens e evidência opcional.

### `manifest.sealed`

`manifesto_id`, `versao`, `algoritmo_hash`, `hash_manifesto`, `metodo_assinatura`, `assinatura`, `chave_assinatura_fingerprint` e lista ordenada de evidências com seus hashes.

### `execution.completed`

`status`, `resultado`, `fim_monotonico_ns`, `duracao_ms` e contagens consolidadas.

### `ledger.event.accepted`

`ledger_sequence`, `received_at_utc`, `source_stream_id`, `source_stream_sequence`, `source_event_id` e `source_event_hash`.

### `record.corrected`

`target_event_id`, `target_event_hash`, `correction_reason` e `corrected_fields`. A correção não altera evento, hash, sequência ou evidência anteriores. Correção de conteúdo de evidência exige nova evidência derivada.

## 8. Regras temporais

- `emitted_at_utc` sempre contém `Z` e precisão mínima de milissegundos.
- Durações locais derivam de contadores monotônicos do mesmo relógio.
- O emissor registra o host e sua versão.
- A sincronização de tempo do ambiente será documentada como evidência de configuração.
- Ordem de `stream_sequence` prevalece sobre UTC em eventos do mesmo stream.

## 9. Regras de identidade

- `actor.ator_id` deve resolver para `identidades_atores.ator_id`.
- O principal observado deve coincidir com a identidade autorizada.
- Contas compartilhadas são proibidas nas execuções principais.
- `LOCAL_CONTROLADO` exige justificativa e evento de anomalia ou exceção.
- Alteração de principal, chave ou certificado exige nova versão da identidade ou novo `ator_id`, conforme a política de identidade.

## 10. Regras de validação e rejeição

Um evento é rejeitado quando:

- não valida contra o schema;
- repete `event_id` com conteúdo diferente;
- quebra a sequência ou o encadeamento do stream;
- referencia experimento, execução, ator ou evidência inexistente quando exigidos;
- apresenta hash incompatível;
- contém campo desconhecido no envelope ou payload normativo;
- mistura clocks monotônicos incompatíveis para calcular duração;
- inclui segredo conhecido ou material de credencial proibido.
- reutiliza `stream_id` após reinício/perda de estado;
- usa inteiro JSON inseguro em campo que exija precisão exata.

O rejeitado deve ser preservado em área de quarentena, acompanhado do motivo, sem entrar na projeção oficial.

## 11. Idempotência de ingestão

- Mesmo `event_id` e mesmos bytes canônicos: reentrega idempotente.
- Mesmo `event_id` e conteúdo diferente: conflito crítico.
- Novo `event_id` corrigindo evento anterior: usar `record.corrected`, `causation_id` e referência ao hash original.

## 12. Selamento e manifesto

O manifesto final contém, para cada stream: `stream_id`, primeira/última sequência, quantidade, primeiro/último hash e indicador de completude. Também registra `ledger_hash`, lacunas detectadas, streams interrompidos e a lista ordenada de evidências. A assinatura cobre o manifesto canonicalizado por JCS sem o próprio campo de assinatura.

## 13. Impacto na futura matriz ODS v0.3

A projeção ODS deverá acrescentar três entidades antes de ser congelada:

- `streams_eventos`: identidade, origem, boot, primeiro/último hash, contagem e completude;
- `ledger_eventos`: ordem de ingestão e referência imutável ao evento de origem;
- `correcoes_registro`: evento original, hash original, motivo, autor e campos corrigidos.

A matriz v0.2 permanece histórica e não deve ser adotada para a coleta. A v0.3 somente será gerada após o mapeamento desses três conjuntos no dicionário.

## 14. Versionamento

- Compatibilidade retroativa: incremento de patch ou minor conforme regra documentada.
- Quebra de campos obrigatórios, semântica ou canonicalização: incremento major.
- `schema_version` pertence ao contrato de eventos e não deve ser confundida com `doml_version`.

## 15. Impacto esperado na DOML-F

O contrato exige somente pontos de integração:

- identidade, versão e hash estáveis do modelo;
- referências a políticas de coleta, custódia e manifesto;
- identificação dos emissores necessários;
- `secret_ref` para impedir segredos incorporados;
- distinção normativa entre política declarada e instância observada.

Nenhuma dessas exigências autoriza armazenar resultados operacionais dentro do modelo declarativo.
