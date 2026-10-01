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

RQ-44 — Assinatura criptográfica de artefatos
O laboratório DEVE permitir a assinatura criptográfica de manifestos e de outros artefatos cuja autoria, aprovação ou procedência necessite ser verificável. A implementação de referência DEVE utilizar Ed25519, sem tornar o modelo conceitualmente dependente desse algoritmo ou de uma infraestrutura específica de certificação.

RQ-45 — Identificação da assinatura
Toda assinatura criptográfica DEVE permitir identificar, no mínimo, o artefato assinado, o mecanismo e algoritmo utilizados, o signatário ou identidade lógica associada, a credencial ou chave pública correspondente e o instante da assinatura.

RQ-46 — Verificação e confiança
O laboratório DEVE permitir verificar criptograficamente a assinatura e determinar a fonte ou política de confiança utilizada para associar a credencial criptográfica ao signatário declarado.

RQ-47 — Evolução do mecanismo de assinatura
O mecanismo de assinatura DEVE ser substituível ou extensível sem exigir alteração conceitual dos artefatos protegidos e sem impedir a verificação das assinaturas históricas, desde que sejam preservados os algoritmos, credenciais, metadados e demais elementos necessários à sua validação.

RQ-48 — Autoridade de identidade e credenciais
O laboratório DEVE possuir uma autoridade responsável pela emissão, registro, substituição e revogação das identidades e credenciais criptográficas utilizadas na assinatura dos artefatos. Na implementação experimental, essa função PODE ser exercida pelo administrador responsável pelo laboratório. O modelo DEVE permitir futura delegação ou separação dessa função sem alteração conceitual dos artefatos ou registros existentes.

RQ-49 — Retenção das evidências experimentais
Toda evidência coletada DEVE permanecer preservada, íntegra e identificável durante o período necessário à execução, validação, reprodução e documentação do experimento. A política de retenção DEVE definir o evento ou condição que autoriza seu descarte.

RQ-50 — Descarte controlado das evidências
O descarte de uma evidência DEVE ser registrado antes ou no momento de sua realização, preservando-se no histórico, no mínimo, sua identificação, hash anteriormente calculado, data e hora do descarte, responsável e motivo ou condição que autorizou o descarte. O descarte do conteúdo da evidência NÃO DEVE eliminar os registros necessários à reconstrução de seu ciclo de vida.


