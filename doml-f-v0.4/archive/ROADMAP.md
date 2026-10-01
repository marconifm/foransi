# Roadmap técnico e pontos de decisão

## Classificação de prioridade

- **P0 — bloqueador:** necessário antes do primeiro experimento válido.
- **P1 — necessário:** necessário antes da análise consolidada/artigo.
- **P2 — evolução:** pode ser implementado depois do MVP experimental.

## Fase A — contrato e rastreabilidade

| Item | Prioridade | Estado |
|---|---:|---|
| Contrato JSONL | P0 | concluído em proposta |
| JSON Schema | P0 | concluído em proposta |
| JCS e regras de hash | P0 | definido; integração pendente |
| Streams e ledger | P0 | definido; núcleo validável |
| Correções imutáveis | P0 | definido |
| Mapa de projeção | P0 | primeira versão criada |

## Fase B — validador

| Item | Prioridade | Estado |
|---|---:|---|
| Parser estrito | P0 | implementado |
| Validação JSON Schema | P0 | código implementado; dependência não instalada no ambiente atual |
| JCS/SHA-256 | P0 | código implementado; dependência não instalada no ambiente atual |
| Cadeia dos streams | P0 | implementado |
| Ledger | P0 | implementado |
| Durações/causalidade | P0 | implementado parcialmente |
| Manifesto estrutural | P0 | implementado |
| Assinatura criptográfica | P0 | Definido: Ed25519; arquitetura extensível |
| AAA Kerberos/OpenLDAP | P0 | Ambiente piloto Definido: 3 hosts × 4 cores × 16 GB × SSD 256 GB/BTRFS; Debian 13/Incus; LDAP + MIT Kerberos + Samba + SSH; sem VLAN física/honeypot |
| Projeção completa | P0 | Definido: limite operacional local de 150 GB/host; remoto 4–8 TB; sem limite arbitrário único por evidência |

## Fase C — matriz ODS v0.3

| Item | Prioridade | Estado |
|---|---:|---|
| 23 entidades operacionais | P0 | modeladas |
| Proveniência por linha | P0 | definida no mapa; incorporar ao dicionário |
| Dicionário completo | P0 | pendente |
| Geração automática | P0 | pendente do motor de projeção |
| Validação cruzada ODS/mapa | P0 | **Definido:** administrador do laboratório no MVP  |

## Fase D — protocolo experimental

| Item | Prioridade | Estado |
|---|---:|---|
| Piloto N0=5 | P1 | planejado |
| Dimensionamento N | P1 | regra definida |
| Comparação pareada AAA | P1 | definida |
| Política de exclusão/outliers | P1 | Definido: cadeia simples, preservando registro histórico |

## Decisões externas ainda necessárias

1. ~~Método e infraestrutura de assinatura do manifesto: SSH signing, certificado X.509 ou outro mecanismo institucional.~~
2. Autoridade responsável por emitir/revogar identidades e chaves no laboratório.
3. ~~Política formal de retenção e descarte das evidências.~~
4. ~~Parâmetros definitivos do ambiente piloto e cenários executados.~~
5. ~~Limite operacional de armazenamento e tamanho máximo de evento/evidência.~~

Nenhuma dessas decisões impede continuar o motor de projeção estrutural. Elas bloqueiam apenas assinatura real, integração AAA completa e execução experimental válida.

