# Especificação de Requisitos — Laboratório Forense Replicável  
**Versão:** 0.2   
**Objetivo deste documento:** depurar a criação da DOML v0.2.  
Nesta etapa estamos especificando o que ela deverá representar e validar.

---

RQ-01 — Modelo

O ambiente deve possuir uma descrição declarativa versionada.

RQ-02 — Fonte de verdade

A configuração estrutural do laboratório deve derivar do modelo.

RQ-03 — Provisionamento

O ambiente deve ser provisionável por Ansible.

RQ-04 — Idempotência

A execução repetida do provisionamento não deve produzir alterações indevidas.

RQ-05 — Debian

Os nós Linux do MVP devem utilizar Debian 13.

RQ-06 — Incus

Containers de sistema devem ser executados como instâncias Incus.

RQ-07 — VM

A arquitetura deve permitir VM futura sem alterar o modelo fundamental.

RQ-08 — BTRFS

O armazenamento dos hosts do laboratório deve utilizar BTRFS.

RQ-09 — Snapshot

Deve ser possível criar snapshot do estado conhecido dos alvos.

RQ-10 — Restore

Deve ser possível retornar os alvos ao baseline.

RQ-11 — Rede

O laboratório deve possuir rede logicamente segregada da produção.

RQ-12 — Gerenciamento

O gerenciamento deve possuir acesso separado dos alvos experimentais.

RQ-13 — Ataque

O atacante deve estar restrito à rede experimental.

RQ-14 — Evidência

O armazenamento de evidências deve ser separado dos alvos.

RQ-15 — Honeypot

Deve existir pelo menos um honeypot.

RQ-16 — SSH

Deve existir pelo menos um alvo SSH.

RQ-17 — Web

Deve existir pelo menos um alvo Apache/PHP.

RQ-18 — Samba

Deve existir compartilhamento Samba para experimentos controlados.

RQ-19 — LDAP

Deve existir diretório OpenLDAP para identidade experimental.

RQ-20 — DNS

Deve existir DNS interno controlado.

RQ-21 — DHCP

Deve existir DHCP experimental quando necessário ao cenário.

RQ-22 — Logging

Os principais eventos dos alvos devem ser enviados para fora dos próprios alvos.

RQ-23 — Tempo

Todos os nós relevantes devem utilizar referência temporal consistente.

RQ-24 — Marcação

Cada experimento deve possuir início e término identificáveis.

RQ-25 — Baseline

Cada experimento deve começar a partir de estado conhecido.

RQ-26 — Ground truth

Cada cenário deve possuir registro da atividade deliberadamente executada.

RQ-27 — Coleta

Deve existir procedimento padronizado de aquisição.

RQ-28 — Integridade

Artefatos coletados devem possuir hash criptográfico.

RQ-29 — Manifesto

Cada coleta deve possuir manifesto.

RQ-30 — Proveniência

Cada evidência deve registrar origem, horário, método de aquisição e experimento.

RQ-31 — Preservação

A evidência original deve ser preservada separadamente das cópias utilizadas para análise.

RQ-32 — Análise

A análise deve ocorrer sobre cópia ou representação de trabalho.

RQ-33 — Timeline

O método deve permitir construir uma linha temporal do incidente.

RQ-34 — Correlação

O método deve permitir relacionar eventos provenientes de fontes distintas.

RQ-35 — Restauração

O ambiente deve poder retornar ao estado anterior ao experimento.

RQ-36 — Repetição

O mesmo experimento deve poder ser executado novamente.

RQ-37 — Comparação

Os resultados de execuções distintas devem poder ser comparados.

RQ-38 — Versionamento

DOML, Ansible, políticas, manifests, runbooks e documentação devem ser versionados.

RQ-39 — Reprodutibilidade

Uma terceira pessoa deve conseguir reconstruir o ambiente seguindo a documentação.

RQ-40 — Auditoria

Deve ser possível determinar qual versão do modelo, automação e configuração originou determinado experimento.

RQ-41 — Segurança

Nenhuma atividade ofensiva deve possuir rota não controlada para produção ou Internet.

RQ-42 — Dados

O laboratório deve utilizar exclusivamente dados sintéticos.

RQ-43 — Extensibilidade

A inclusão futura de PostgreSQL, MariaDB, Kerberos, AD/DC, VM etc. não deve exigir alteração conceitual da DOML.
