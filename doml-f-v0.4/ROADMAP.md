# Roadmap técnico DOML-F

**Atualização:** 2026-09-26  
**Estado geral:** Preparação da execução exploratória C01 suspensa preventivamente pelo evento `PRE-C01-20260926-TIME` (falha de pré-condição no portão temporal G03; instabilidade de clocksource no controlador). C01 não iniciado. Investigação e resolução de hardware/NTP em andamento.

## Prioridades

- **P0 — bloqueador:** necessário antes do primeiro experimento válido.
- **P1 — necessário:** necessário antes da análise consolidada e do artigo.
- **P2 — evolução:** posterior ao MVP experimental.

## Fase A — contrato, integridade e rastreabilidade

| Item | Prioridade | Estado |
|---|---:|---|
| Contrato de eventos JSONL | P0 | definido em `docs/especificacao/DOML-F-EVENT-CONTRACT-v0.1.md` |
| JSON Schema de eventos | P0 | definido em `schemas/doml-f-event.schema.json` |
| JCS/RFC 8785 e SHA-256 | P0 | implementados no validador; integração ponta a ponta pendente |
| Streams locais e ledger de ingestão | P0 | definidos; validação básica implementada |
| Correções imutáveis | P0 | definidas; projeção completa pendente |
| Mapa evento → matriz | P0 | v0.1 preservada; extensão C01/v0.3 em `models/event-projection-map-v0.2.yaml` |
| Assinatura de manifestos | P0 | Ed25519 definido; implementação e testes pendentes |
| Identidade do signatário e confiança | P0 | administrador do laboratório como autoridade inicial; registro e revogação pendentes de implementação |

## Fase B — validador e projeção

| Item | Prioridade | Estado |
|---|---:|---|
| Parser estrito | P0 | implementado |
| Validação JSON Schema | P0 | código implementado; validar dependências e testes automatizados |
| Cadeia de hashes dos streams | P0 | implementada; ampliar cobertura de testes |
| Ledger | P0 | implementado; ampliar validação cruzada |
| Durações e causalidade | P0 | parcialmente implementadas |
| Manifesto estrutural | P0 | implementado |
| Motor de projeção | P0 | parcialmente implementado |
| Projeção completa das 23 entidades | P0 | pendente |
| Testes unitários e de integração | P0 | diretórios criados; casos de teste pendentes |

## Fase C — matriz experimental v0.3

| Item | Prioridade | Estado |
|---|---:|---|
| Modelo relacional com 23 entidades | P0 | definido em `models/modelo-matriz-v0.3.md` |
| Proveniência por linha | P0 | definida no mapa; incorporar ao dicionário |
| Dicionário completo | P0 | gerado na `matriz-experimental-v0.3.ods` |
| Pontos de coleta | P0 | definidos na aba `pontos_coleta` |
| Geração inicial da ODS | P0 | concluída; automatização pelo motor de projeção permanece pendente |
| Validação cruzada ODS ↔ mapa ↔ eventos | P0 | pendente |
| Migração documentada v0.2 → v0.3 | P0 | sincronizada em `docs/migracao/` |

## Fase D — protocolo e ambiente piloto

| Item | Prioridade | Estado |
|---|---:|---|
| Protocolo experimental consolidado | P0 | v0.3 consolidada; timeout depende da execução exploratória |
| Cenários controlados | P0 | C01 determinístico; C02–C06 aguardam detalhamento após estabilização |
| Política de evidências | P0 | procedimento v0.3 consolidado |
| Ambiente piloto | P0 | 3 hosts equivalentes, Debian 13, Incus e BTRFS definidos |
| Serviços do piloto | P0 | OpenLDAP, MIT Kerberos, Samba e SSH definidos |
| Rede do piloto | P0 | sub-redes Incus não sobrepostas, roteamento explícito e nftables; validação prática pendente |
| Armazenamento local | P0 | limite operacional de 150 GB por host |
| Armazenamento remoto | P0 | NFS 4–8 TB definido como infraestrutura de apoio |
| Controlador dedicado | P0 | `foransi-host-00` definido; configuração pendente |
| Automação Ansible | P0 | estrutura criada; inventários, playbooks e roles pendentes |
| Piloto N0 = 5 por cenário | P1 | planejado |
| Dimensionamento da amostra principal | P1 | regra definida; depende dos dados do piloto |
| Comparação pareada AAA | P1 | definida |
| Exclusão, aborto e outliers | P1 | regras definidas; aquecimento/timeout serão calibrados na exploratória |

## Decisões consolidadas

1. Assinatura de referência por Ed25519, com mecanismo substituível e preservação da verificabilidade histórica.
2. O administrador do laboratório exerce inicialmente a autoridade de emissão, registro, substituição e revogação de identidades e chaves.
3. A cadeia mínima de evidências é: coleta → identificação → hash → armazenamento → validação/uso → retenção → descarte controlado, mantendo registro histórico.
4. O piloto usa três hosts físicos equivalentes, cada um com 4 núcleos, 16 GB de RAM e SSD de 256 GB em BTRFS, executando Debian 13 e Incus.
5. O escopo inicial inclui OpenLDAP, MIT Kerberos, Samba e SSH. Honeypot, bancos de dados, serviços web, DNS/DHCP dedicado e Samba AD/DC ficam fora do MVP.
6. Não haverá dependência de VLAN física. A segregação necessária será lógica e compatível com uma única interface de rede por host.
7. O limite operacional local é 150 GB por host. Evidências consolidadas podem usar repositório remoto de 4–8 TB; artefatos grandes permanecem referenciados por localização, tamanho e hash.
8. `foransi-host-00` é o controlador dedicado e não integra o conjunto de alvos avaliados.
9. NFS é infraestrutura de apoio, fora das métricas funcionais.
10. A rede usa sub-redes Incus não sobrepostas por host e roteamento explícito sobre a rede física.
11. O desvio temporal máximo é 1 segundo, com NTP contínuo e UTC.
12. Falhas em portões de pré-voo (G01–G12) são classificadas formalmente como falhas de pré-condição de infraestrutura e não computam como falha experimental do C01. O evento PRE-C01-20260926-TIME mantém o ambiente intacto até estabilização de hardware/clocksource.

## Próximo marco

A execução exploratória C01 será autorizada exclusivamente após a resolução do evento PRE-C01-20260926-TIME, exigindo:
1. Conclusão do teste A/B de clocksource (`tsc` vs `hpet`) no host-00 e saneamento sintático de `/etc/ntpsec/ntp.conf`;
2. Pelo menos 30 minutos contínuos sem *time stepped*, com peer selecionado (`*`), `reach` estável e offset absoluto $\le 1$ s em todos os nós;
3. Saneamento dos pacotes gráficos residuais nos hosts 02 e 03 para equalização de baseline com o host-01;
4. Configuração completa do preseed BTRFS/Incus, automação Ansible e assinatura Ed25519. A exploratória calibrará timeout e não integrará `N0=5`.
