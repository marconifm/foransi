# Checklist operacional para preparação e execução do C01

**Versão:** 1.4  
**Escopo:** preparação do laboratório, implementação dos artefatos e liberação da execução exploratória C01  
**Regra:** nenhuma atividade marcada como portão pode permanecer pendente antes da execução correspondente.

**Estado em 26/09/2026:** preparação suspensa por falha no portão temporal; C01 não iniciado.

## Suspensão PRE-C01-20260926-TIME

- [x] **[CONJUNTO]** Interromper a preparação antes da criação das instâncias e antes do início do C01.
- [x] **[CONJUNTO]** Classificar o evento como falha de pré-condição da infraestrutura, não como falha de implantação, idempotência ou reprodução do C01.
- [x] **[CONJUNTO]** Confirmar instabilidade grave de temporização em dois computadores, incompatível com a rastreabilidade cronológica exigida.
- [ ] **[CONJUNTO]** Manter a causa como `suspeita de hardware/clocksource` até teste comparativo ou substituição; os dados ainda não isolam RTC, TSC, HPET, firmware, placa-mãe ou fonte de alimentação.
- [ ] **[VOCÊ][PORTÃO]** Substituir ou reparar os dois computadores afetados e repetir integralmente o preflight de rede, kernel, clocksource e NTP.
- [ ] **[EU]** Preservar configurações, saídas, horários, logs, hashes e decisão de suspensão no conjunto de evidências PRE-C01.
- [ ] **[CONJUNTO][PORTÃO]** Somente liberar novo C01 após pelo menos 30 minutos sem `time stepped`, peer selecionado, `reach` estável e offset absoluto ≤1 s em todos os nós.

## Legenda de responsabilidade

- **[VOCÊ]** preparação física, instalação, endereçamento, acesso e execução no laboratório;
- **[EU]** arquivos, código, automação, contratos, coletores e documentação que serão produzidos por mim;
- **[CONJUNTO]** depende de informação ou execução sua e análise/ajuste meu;
- **[PORTÃO]** bloqueia a execução exploratória ou o piloto enquanto não for aprovado.

## 0. Informações que preciso receber

- [x] **[VOCÊ]** Endereçamento físico coletado dos quatro nós:

  | Nó | IPv4 físico em `10.127.0.0/20` | Gateway | Interface |
  |---|---|---|---|
  | `foransi-host-00` | `10.127.0.10/20` | `10.127.0.1` | `enp5s0` |
  | `foransi-host-01` | `10.127.0.11/20` | sem gateway/rota padrão no estado atual | `enp5s0` |
  | `foransi-host-02` | `10.127.0.12/20` | sem gateway/rota padrão no estado atual | `enp5s0` |
  | `foransi-host-03` | `10.127.0.13/20` | sem gateway/rota padrão no estado atual | `enp5s0` |

- [x] **[VOCÊ]** Informar a interface física do host-00: `enp5s0`.
- [x] **[VOCÊ]** Interface física dos hosts 01–03 confirmada: `enp5s0`.
- [x] **[CONJUNTO]** Validar o host-01 após reinicialização: somente `10.127.0.11/20`, sem endereço DHCP, sem rota padrão e com `networking.service`/`ifupdown` ativo.
- [x] **[CONJUNTO]** Confirmar no host-01 que `dhcpcd`, `systemd-networkd` e `NetworkManager` estão inativos; a existência de `/etc/dhcpcd.conf` não representa serviço em execução.
- [x] **[CONJUNTO]** Validar o host-02 após reinicialização: somente `10.127.0.12/20`, sem endereço DHCP, sem rota padrão e com `networking.service`/`ifupdown` ativo.
- [x] **[CONJUNTO]** Confirmar no host-02 que `dhcpcd`, `systemd-networkd` e `NetworkManager` estão inativos; `/etc/dhcpcd.conf` é apenas arquivo residual/de exemplo sem daemon correspondente.
- [x] **[CONJUNTO]** Validar o host-03 após reinicialização: somente `10.127.0.13/20`, sem endereço DHCP, sem rota padrão e com `networking.service`/`ifupdown` ativo.
- [x] **[CONJUNTO]** Confirmar no host-03 que `dhcpcd`, `systemd-networkd` e `NetworkManager` estão inativos; `/etc/dhcpcd.conf` não possui daemon ativo associado.
- [x] **[CONJUNTO]** Encerrar a suspeita de concorrência persistente de gerenciadores nos hosts 01–03. Os endereços `10.131.*` dos inventários representam estado anterior ao reboot e não reapareceram na configuração vigente.
- [ ] **[EU]** Registrar a divergência entre o inventário inicial e o estado pós-reboot como evento de baseline, sem classificá-la como falha experimental do C01.
- [ ] **[VOCÊ][PORTÃO]** Confirmar o caminho exportado pelo NFS, endereço do servidor e opções autorizadas de montagem.
- [ ] **[VOCÊ][PORTÃO]** Definir o realm Kerberos, base DN LDAP e domínio/workgroup Samba do piloto.
- [ ] **[VOCÊ]** Informar se existe DNS interno utilizável ou se o piloto começará com entradas controladas em `/etc/hosts`.
- [ ] **[CONJUNTO]** Registrar essas decisões em `ansible/inventories/lab/group_vars/all.yml`, sem incluir segredos.

## 1. Convenção de nomes e endereçamento

### 1.1 Nomes

- [ ] **[VOCÊ]** Configurar os nomes físicos:

  - `foransi-host-00`: controlador;
  - `foransi-host-01`: host do provedor de identidade;
  - `foransi-host-02`: host do servidor de arquivos;
  - `foransi-host-03`: host do cliente de validação.

- [ ] **[EU]** Criar o inventário Ansible usando esses nomes como identificadores estáveis.
- [ ] **[EU]** Criar teste que rejeite hostname inesperado ou duplicado.
- [x] **[VOCÊ]** Hostname curto do controlador configurado como `foransi-host-00`.
- [ ] **[VOCÊ][PORTÃO]** Antes de configurar LDAP/Kerberos, alterar o FQDN de `foransi-host-00.foransi` para `foransi-host-00.foransi.test`.
- [ ] **[CONJUNTO]** Adotar, salvo decisão contrária documentada:

  - domínio DNS do laboratório: `foransi.test`;
  - realm Kerberos: `FORANSI.TEST`;
  - base DN LDAP: `dc=foransi,dc=test`;
  - workgroup Samba: `FORANSI`.

- [ ] **[EU]** Atualizar inventário, templates e testes para rejeitar o sufixo não reservado `.foransi`.

### 1.2 Redes Incus

- [ ] **[VOCÊ][PORTÃO]** Reservar as redes sem sobreposição:

  | Host | Rede Incus | Gateway local sugerido | Instância inicial | IP sugerido |
  |---|---|---|---|---|
  | host-01 | `10.179.1.0/24` | `10.179.1.1` | `idp-01` | `10.179.1.10` |
  | host-02 | `10.179.2.0/24` | `10.179.2.1` | `files-01` | `10.179.2.10` |
  | host-03 | `10.179.3.0/24` | `10.179.3.1` | `client-01` | `10.179.3.10` |

- [ ] **[VOCÊ][PORTÃO]** Confirmar que nenhum outro equipamento usa essas três redes.
- [ ] **[EU]** Criar configuração declarativa das três redes Incus, rotas e regras mínimas de encaminhamento.
- [ ] **[CONJUNTO][PORTÃO]** Aplicar primeiro em janela de manutenção, mantendo uma sessão administrativa de contingência.
- [ ] **[CONJUNTO][PORTÃO]** Testar comunicação autorizada entre as três instâncias e ausência de rota não prevista para produção/Internet.
- [ ] **[EU]** Gerar `network-baseline.json`, `routes.txt`, `ip-address.txt` e `nftables-ruleset.nft` para cada host.

### 1.3 Gerenciador de rede

- [x] **[VOCÊ]** Manter `ifupdown` no host-01; a configuração vigente está em `/etc/network/interfaces` e `networking.service` está ativo.
- [ ] **[VOCÊ]** Não ativar simultaneamente `systemd-networkd` para as mesmas interfaces.
- [ ] **[EU]** Fazer o coletor identificar e registrar o gerenciador efetivamente ativo.
- [x] **[CONJUNTO]** Confirmar um único gerenciador para `enp5s0` no host-01.
- [x] **[CONJUNTO]** Confirmar um único gerenciador para `enp5s0` no host-02.
- [x] **[CONJUNTO]** Confirmar um único gerenciador para `enp5s0` no host-03; hosts 01–03 estão homogêneos.
- [x] **[CONJUNTO]** Adotar `foransi-host-00` (`10.127.0.10`) como servidor NTP intermediário dos hosts avaliados; não adicionar rota padrão nem rota para `10.131.0.0/16` nos hosts 01–03.

## 2. `foransi-host-00` — controlador dedicado

### Estado observado em 25/09/2026

- [x] **[VOCÊ]** Registrar Debian 13.7, kernel `6.12.107+deb13-amd64`, 4 vCPU, aproximadamente 5,7 GiB RAM e raiz BTRFS de 231,59 GiB.
- [x] **[VOCÊ]** Registrar `ansible` 12.0, `ansible-core` 2.19.11, `incus-client` 6.0.4, `nfs-common`, `nftables`, `ntpsec`, `ntpsec-ntpdate`, `openssh-server`, `python3`, `jq`, `rsync`, `sudo` e `vim` já instalados.
- [ ] **[CONJUNTO]** Verificar somente os itens restantes da lista de pacotes do controlador; não reinstalar indiscriminadamente o conjunto já presente.
- [ ] **[CONJUNTO][PORTÃO]** Considerar a RAM menor do host-00 no dimensionamento dos processos de controle. Ela é aceitável porque o controlador está fora do conjunto avaliado e não hospedará as instâncias experimentais.

### 2.0 Proveniência da instalação

- [x] **[VOCÊ]** Imagem utilizada: `debian-13.7.0-amd64-netinst.iso`.
- [x] **[VOCÊ]** Caminho original registrado: `/home/marconi/Downloads/debian-13.7.0-amd64-netinst.iso` no host `phoenyx`.
- [x] **[VOCÊ]** SHA-256 local calculado:

  ```text
  a7ef94ac2fb9a7fec454552abd629b7cc9d5155c886165a45649f5ce6167e355
  ```

- [ ] **[VOCÊ][PORTÃO]** Verificar a ISO contra `SHA256SUMS` ou `SHA512SUMS` oficial e validar a assinatura `.sign` com o chaveiro Debian.
- [ ] **[EU]** Registrar separadamente:

  - nome e tamanho da ISO;
  - hash local;
  - algoritmo;
  - URL/origem;
  - data da obtenção;
  - arquivo de checksums;
  - resultado da assinatura OpenPGP;
  - fingerprint da chave de assinatura.

- [x] **[VOCÊ]** Mídia gravada em `/dev/sdb` com:

  ```text
  dd if=/home/marconi/Downloads/debian-13.7.0-amd64-netinst.iso of=/dev/sdb bs=4M
  ```

- [x] **[VOCÊ]** Resultado do `dd` registrado:

  ```text
  189+0 records in
  189+0 records out
  792723456 bytes (793 MB, 756 MiB)
  193,39 s
  4,1 MB/s
  ```

- [ ] **[VOCÊ]** Se a mídia ainda estiver disponível, executar `sync` e comparar os primeiros `792723456` bytes da mídia com a ISO.
- [ ] **[EU]** Preservar os registros como `installer-media.json`, `iso-checksums.txt` e `usb-write.txt`.
- [x] **[VOCÊ]** Instalação padrão concluída com alteração da partição raiz de ext4 para BTRFS.
- [ ] **[EU]** Coletar o layout efetivo; a descrição “BTRFS padrão” não substitui UUID, mounts, subvolumes e opções.
- [ ] **[VOCÊ]** Preservar `/var/log/installer/` antes de qualquer limpeza de logs.
- [ ] **[EU]** Gerar arquivo compactado e hash de `/var/log/installer/`.

### 2.1 Instalação básica

- [x] **[VOCÊ]** Instalar Debian 13.7 em máquina dedicada e fora do conjunto avaliado.
- [x] **[VOCÊ]** Realizar primeiro acesso remoto como usuário `marconi`.
- [x] **[VOCÊ]** Registrar elevação inicial para root com `su -` como procedimento de bootstrap.
- [x] **[VOCÊ]** Instalar `vim` por familiaridade operacional e compatibilidade.
- [ ] **[EU]** Registrar a versão exata do `vim` e dos demais pacotes no manifesto de baseline.
- [ ] **[VOCÊ]** Não realizar novas instalações manuais após o congelamento; qualquer pacote adicional deverá ser aplicado por automação versionada.
- [ ] **[VOCÊ]** Aplicar atualização completa e reiniciar antes de registrar o baseline.
- [ ] **[VOCÊ]** Instalar os pacotes de controle:

  ```text
  git
  ansible-core
  python3
  python3-venv
  python3-pip
  python3-cryptography
  openssh-client
  sudo
  jq
  rsync
  curl
  ca-certificates
  nftables
  ntpsec
  ntpsec-ntpdate
  nfs-common
  openssl
  acl
  attr
  ```

- [ ] **[VOCÊ]** Instalar `incus-client` se o controle remoto do Incus for adotado.
- [ ] **[VOCÊ]** Não instalar serviços experimentais OpenLDAP, KDC ou Samba no host-00.
- [ ] **[EU]** Criar script `scripts/preflight/controller.sh` para verificar pacotes, versões, relógio, Git, SSH, Vault, NFS e espaço.

### 2.2 Rede e tempo

- [x] **[VOCÊ]** Configurar IPv4 fixo `10.127.0.10/20` na interface `enp5s0`.
- [x] **[VOCÊ]** Configurar gateway `10.127.0.1`.
- [x] **[VOCÊ]** Confirmar uso de `ifupdown` por `/etc/network/interfaces`.
- [x] **[VOCÊ]** Registrar DNS provisório `8.8.8.8` e `8.8.4.4` durante a preparação.
- [ ] **[VOCÊ][PORTÃO]** Substituir DNS público por DNS interno controlado ou remover servidores externos antes da execução isolada.
- [ ] **[VOCÊ]** Registrar MAC e MTU de `enp5s0`.
- [ ] **[EU]** Preservar cópia e SHA-256 de `/etc/network/interfaces` e `/etc/hosts`.
- [ ] **[EU]** Gerar `network-config.json` com:

  ```text
  hostname=foransi-host-00
  interface=enp5s0
  address=10.127.0.10/20
  gateway=10.127.0.1
  manager=ifupdown
  ```

- [ ] **[VOCÊ][PORTÃO]** Depois de mudar o domínio, ajustar `/etc/hosts` para:

  ```text
  127.0.0.1  localhost
  127.0.1.1  foransi-host-00.foransi.test foransi-host-00
  ```

- [ ] **[CONJUNTO]** Adicionar nomes dos demais hosts/instâncias ao DNS interno ou a um arquivo `/etc/hosts` gerenciado pelo Ansible.
- [ ] **[VOCÊ][PORTÃO]** Configurar `ntpsec` no host-00 com fonte primária `10.131.0.7` e habilitá-lo para servir tempo em `10.127.0.0/20`.
- [ ] **[VOCÊ]** Manter `a.ntp.br`/`200.160.0.8` no host-00 apenas como fallback quando houver conectividade.
- [x] **[CONJUNTO]** Validar que o host-01 alcança `10.127.0.10`: resposta stratum 2, estado `no-leap` e correção inicial de `+1,939847 s` em 26/09/2026 às 10:51 -03.
- [ ] **[VOCÊ][PORTÃO]** Configurar sincronização contínua do host-01 contra `10.127.0.10`; `ntpdate` isolado é apenas bootstrap e não comprova manutenção do relógio.
- [ ] **[VOCÊ][PORTÃO]** Executar nova consulta após estabilização e comprovar desvio absoluto ≤1 s.
- [x] **[CONJUNTO]** Diagnosticar em 26/09/2026 que `ntpsec` está habilitado e ativo nos hosts 01–03, porém configurado apenas com `*.debian.pool.ntp.org`, inacessível no laboratório isolado.
- [x] **[CONJUNTO]** Registrar falha do portão de tempo: `ntpq -pn` mostrou `reach=0`, stratum 16 e nenhum peer selecionado nos três hosts; `ntpdate -q 10.127.0.10` mediu offsets de `+3,576451 s`, `+3,369580 s` e `+3,336984 s`.
- [ ] **[VOCÊ][PORTÃO]** Substituir os pools externos por `server 10.127.0.10 iburst prefer` em `/etc/ntpsec/ntp.conf` nos hosts 01–03.
- [ ] **[CONJUNTO][PORTÃO]** Após o bootstrap, confirmar em cada host: linha `*10.127.0.10` em `ntpq -pn`, `reach` diferente de zero, stratum válido e offset absoluto ≤1 s.
- [x] **[CONJUNTO]** Confirmar em 26/09/2026 que o host-00 está sincronizado: peer selecionado `*200.20.186.76`, stratum remoto 1, `reach=377`, serviço habilitado e ativo.
- [x] **[CONJUNTO]** Confirmar a precisão dos hosts avaliados por consulta direta a `10.127.0.10`: host-01 `+0,013812 s`, host-02 `+0,010501 s` e host-03 `+0,007536 s`, todos dentro da tolerância de 1 segundo.
- [ ] **[VOCÊ][PORTÃO]** Remover a diretiva redundante `pool 10.127.0.10`, se presente, mantendo somente `server 10.127.0.10 iburst prefer`; a associação `.POOL.` apareceu ao lado da associação unicast nos três clientes.
- [ ] **[CONJUNTO][PORTÃO]** Aguardar aumento de `reach` e confirmar `*10.127.0.10`; no primeiro ciclo os clientes mostraram `+10.127.0.10`, portanto alcançável e candidato, mas ainda não selecionado como system peer.
- [x] **[CONJUNTO]** Identificar no host-00 passos recorrentes do relógio: `+0,485521 s` às 12:14:05 e `+0,496844 s` às 12:30:26 de 26/09/2026, intervalo compatível com deriva aproximada de 500 ppm.
- [x] **[CONJUNTO]** Registrar estado anômalo após o segundo passo: `leap_alarm`, `sync_unspec`, `no_sys_peer`, stratum 16, `frequency=75,677 ppm`, `clk_wander=13,33131` e driftfile ainda em `0.000000`.
- [x] **[CONJUNTO]** Identificar erro sintático em `/etc/ntpsec/ntp.conf` linha 32, opções `nopeer`/`notrap` ignoradas e conflito entre `disable monitor` e `limited`.
- [ ] **[VOCÊ][PORTÃO]** Corrigir a configuração NTPsec antes de novo teste: remover opções obsoletas/invalidas, manter `limited` com monitoramento e remover `tos orphan 5` para que perda de upstream resulte em falha explícita.
- [ ] **[CONJUNTO][PORTÃO]** Executar teste A/B do clocksource: preservar diagnóstico com `tsc`, alternar temporariamente para `hpet`, reinicializar a disciplina NTP e comparar deriva por pelo menos 30 minutos.
- [ ] **[EU]** Registrar a ocorrência como anomalia de baseline, não como resultado do C01; somente classificar como defeito de hardware se a deriva persistir com `hpet` e configuração válida.
- [ ] **[EU]** Criar coleta de fonte NTP, offset, jitter, stratum e estado de sincronização.
- [ ] **[CONJUNTO][PORTÃO]** Confirmar desvio absoluto máximo de 1 segundo antes e depois da execução.

### 2.3 Conta de automação e chaves

- [ ] **[VOCÊ][PORTÃO]** Criar conta exclusiva `ansible` no controlador e nos alvos.
- [ ] **[VOCÊ]** Gerar par Ed25519 exclusivo para o laboratório no host-00.
- [ ] **[VOCÊ]** Instalar somente a chave pública nos alvos.
- [ ] **[VOCÊ]** Restringir a chave, quando aplicável, ao endereço do host-00 em `authorized_keys`.
- [ ] **[VOCÊ][PORTÃO]** Desabilitar login SSH direto de `root`.
- [ ] **[VOCÊ][PORTÃO]** Desabilitar autenticação por senha depois de validar a chave e o acesso de contingência.
- [ ] **[VOCÊ]** Configurar `sudo` não interativo para a conta de automação no laboratório isolado.
- [ ] **[EU]** Criar regra de validação para fingerprint, permissões dos arquivos SSH, origem da conexão e configuração efetiva do `sshd`.
- [ ] **[EU]** Criar registro `controller-identity.json` sem chave privada.

### 2.4 Repositório e ambiente Python

- [ ] **[VOCÊ]** Clonar o repositório `doml-f` no host-00.
- [ ] **[VOCÊ]** Confirmar que o repositório está limpo antes da execução.
- [ ] **[EU]** Definir ambiente virtual e dependências com versões fixadas.
- [ ] **[EU]** Criar comando único de pré-voo, inicialmente `domlf preflight`.
- [ ] **[EU]** Criar comando de execução, inicialmente `domlf run C01`.
- [ ] **[EU]** Criar comando de verificação, inicialmente `domlf verify EXP-XXXX`.

## 3. Hosts-alvo `foransi-host-01` a `03`

### 3.0 Estado observado em 25/09/2026

| Item | `host-01` | `host-02` | `host-03` | Avaliação |
|---|---:|---:|---:|---|
| Debian | 13.7 | 13.7 | 13.7 | homogêneo |
| Kernel | `6.12.107+deb13-amd64` | igual | igual | homogêneo |
| CPU | 4 × AMD Athlon Gold 3150G | igual | igual | homogêneo |
| RAM | ~15 GiB | ~15 GiB | ~15 GiB | suficiente para 3–4 instâncias de 2 GiB, com controle de concorrência |
| Raiz | BTRFS em `/dev/sda2[/@rootfs]` | igual | igual | adequado |
| Capacidade BTRFS | 225,22 GiB | 225,22 GiB | 225,22 GiB | suficiente para teto operacional de 150 GB |
| Incus | 6.0.4 | 6.0.4 | 6.0.4 | homogêneo |

- [x] **[VOCÊ]** Fornecer inventários iniciais dos hosts 00–03.
- [x] **[EU]** Calcular SHA-256 dos inventários recebidos:

  | Arquivo | SHA-256 |
  |---|---|
  | `inventario_foransi-host-00.txt` | `86cc9f6c34a8ec698d2780f088197a9eb256c923717acd26d8ff101e4739834b` |
  | `inventario_foransi-host-01.txt` | `998c19b2b5f9859785fa8ccca41fc94df6ea1520f0f1b8d5cca3e5af2bb1c165` |
  | `inventario_foransi-host-02.txt` | `8e92ae3ed0f3cd438f0219901c242506fe677f3ea71230afea536d5a61991d39` |
  | `inventario_foransi-host-03.txt` | `dfaa90974754c40f31a190ddb2c7eb5486060b89a7e9c275348ee3e689c4bf8b` |

- [ ] **[EU]** Preservar os quatro inventários no repositório de evidências e vinculá-los ao snapshot de baseline.
- [ ] **[CONJUNTO][PORTÃO]** Comparar os manifests completos de pacotes. Os hosts 02 e 03 possuem um conjunto gráfico/multimídia muito maior que o host-01; determinar a origem antes de remover ou instalar pacotes.
- [ ] **[CONJUNTO][PORTÃO]** Tornar equivalentes os pacotes relevantes dos hosts avaliados ou registrar a diferença como variável de controle aprovada.

### 3.1 Base comum

- [x] **[VOCÊ]** Instalar Debian 13.7 em cada host.
- [x] **[VOCÊ]** Confirmar kernel `6.12.107+deb13-amd64`.
- [x] **[VOCÊ]** Confirmar 4 núcleos, aproximadamente 16 GB RAM e SSD nominal de 256 GB por host.
- [ ] **[VOCÊ]** Aplicar atualização completa e reiniciar antes do congelamento.
- [ ] **[VOCÊ]** Instalar a base comum:

  ```text
  incus
  btrfs-progs
  nftables
  openssh-server
  sudo
  python3
  rsync
  jq
  curl
  ca-certificates
  ntpsec
  ntpsec-ntpdate
  acl
  attr
  auditd
  lsof
  procps
  iproute2
  ethtool
  smartmontools
  dmidecode
  pciutils
  ```

- [ ] **[VOCÊ]** Instalar `nfs-common` somente nos nós que realmente precisarem acessar o repositório.
- [ ] **[VOCÊ]** Não instalar manualmente OpenLDAP, Kerberos ou Samba nos hosts físicos; esses serviços pertencem às instâncias e serão implantados pelo Ansible.
- [ ] **[EU]** Criar role `host_baseline` para validar e registrar a base comum sem alterá-la silenciosamente.

### 3.2 BTRFS

- [ ] **[VOCÊ][PORTÃO]** Criar em cada alvo um subvolume BTRFS dedicado ao pool do Incus e usar esse caminho como `source`; não aceitar silenciosamente o pool loop-backed padrão.
- [ ] **[VOCÊ][PORTÃO]** Confirmar que o storage do Incus usa o driver BTRFS e aponta para o subvolume dedicado.
- [x] **[VOCÊ]** Registrar montagem, capacidade, uso, opções e subvolume raiz; ainda faltam UUID e perfis de dados/metadados no registro consolidado.
- [ ] **[VOCÊ]** Não criar layout adicional apenas para satisfazer o experimento antes de o baseline ser coletado.
- [ ] **[EU]** Criar coleta dos comandos:

  ```text
  findmnt
  btrfs filesystem show
  btrfs filesystem usage /
  btrfs subvolume list /
  ```

- [ ] **[EU]** Gerar `btrfs-baseline.txt` e hash correspondente.
- [x] **[CONJUNTO]** Confirmar capacidade física compatível com teto operacional de 150 GB por host.

### 3.3 Incus

- [x] **[VOCÊ]** Confirmar Incus 6.0.4 nos hosts 01–03; no host-01, `incus --version` retornou `6.0.4` em 26/09/2026.
- [ ] **[VOCÊ]** Inicializar o Incus sem criar bridge conflitante com as redes previstas.
- [ ] **[VOCÊ][PORTÃO]** Obter uma única imagem Debian 13 para contêiner Incus durante a preparação, antes de remover o acesso à Internet.
- [ ] **[EU]** Fixar a imagem em artefato exportado; não usar alias remoto móvel durante a execução.
- [ ] **[VOCÊ]** Copiar o mesmo artefato para os hosts 01–03, verificar SHA-256 antes da importação e importar sob alias versionado, inicialmente `debian-13-foransi-v0.1`.
- [ ] **[CONJUNTO][PORTÃO]** Confirmar o mesmo fingerprint Incus nos três hosts e registrar alias, fingerprint completo, arquitetura, data, origem, SHA-256 do artefato e modo privilegiado/não privilegiado.
- [ ] **[EU]** Gerar `image-manifest.json`, `image.sha256` e teste de fingerprint do portão `G05`.
- [ ] **[VOCÊ]** Garantir que `idp-01`, `files-01` e `client-01` estejam ausentes antes do C01.
- [ ] **[EU]** Criar profiles Incus com limite de 2 vCPU e 2 GiB por instância.
- [ ] **[EU]** Criar definições das redes, dispositivos, discos e parâmetros de inicialização.
- [ ] **[EU]** Criar as três instâncias a partir do mesmo fingerprint: `idp-01` no host-01, `files-01` no host-02 e `client-01` no host-03.
- [ ] **[EU]** Atribuir endereços fixos no dispositivo NIC do Incus e validar endereço, gateway, DNS e rotas dentro de cada instância.
- [ ] **[CONJUNTO][PORTÃO]** Validar boot, `systemctl is-system-running`, acesso SSH/exec, 2 vCPU, 2 GiB RAM, BTRFS e ausência de acesso à Internet não autorizado.
- [ ] **[EU]** Criar `scripts/preflight/incus.sh` e `scripts/reset/c01.sh`.

#### Ordem de preparação da imagem e das instâncias

- [ ] **[VOCÊ]** Concluir a sincronização contínua de tempo e a conferência dos pacotes do host-01; rede e versão do Incus já foram validadas.
- [ ] **[EU]** Entregar preseed idempotente para criar o pool BTRFS dedicado, as bridges `incus-br0` com sub-redes específicas por host e o profile de recursos.
- [ ] **[CONJUNTO]** Aplicar o preseed separadamente em cada host e arquivar a entrada, saída e código de retorno.
- [ ] **[CONJUNTO]** Importar a imagem versionada nos três hosts e comparar os fingerprints antes de criar qualquer instância.
- [ ] **[EU]** Criar as instâncias paradas, aplicar NIC/IP e limites, iniciar e executar o smoke test.
- [ ] **[EU]** Produzir snapshot limpo `baseline-ready` somente depois do smoke test e antes da instalação dos serviços.
- [ ] **[CONJUNTO][PORTÃO]** Testar restauração do snapshot ou exclusão/recriação a partir da imagem e comparar o estado resultante.

### 3.4 `foransi-host-01`

- [ ] **[VOCÊ]** Reservar `10.179.1.0/24` e gateway local `10.179.1.1`.
- [ ] **[VOCÊ]** Confirmar resolução de `idp-01` para `10.179.1.10`.
- [ ] **[EU]** Criar instância `idp-01`.
- [ ] **[EU]** Criar roles OpenLDAP, MIT Kerberos e SSH.
- [ ] **[EU]** Criar testes de porta, busca LDAP autenticada e obtenção/validação de TGT.
- [ ] **[EU]** Gerar evidências de configuração sanitizada, pacotes, serviços e testes.

### 3.5 `foransi-host-02`

- [ ] **[VOCÊ]** Reservar `10.179.2.0/24` e gateway local `10.179.2.1`.
- [ ] **[VOCÊ]** Confirmar resolução de `files-01` para `10.179.2.10`.
- [ ] **[EU]** Criar instância `files-01`.
- [ ] **[EU]** Criar roles Samba e SSH integradas à identidade central.
- [ ] **[EU]** Criar compartilhamento e arquivos exclusivamente sintéticos.
- [ ] **[EU]** Criar teste funcional de autenticação, leitura e escrita.
- [ ] **[EU]** Não incluir o serviço NFS de apoio nas métricas funcionais do Samba.

### 3.6 `foransi-host-03`

- [ ] **[VOCÊ]** Reservar `10.179.3.0/24` e gateway local `10.179.3.1`.
- [ ] **[VOCÊ]** Confirmar resolução de `client-01` para `10.179.3.10`.
- [ ] **[EU]** Criar instância `client-01`.
- [ ] **[EU]** Instalar nela somente clientes necessários a LDAP, Kerberos, Samba e SSH.
- [ ] **[EU]** Criar scripts de teste funcional e coleta.
- [ ] **[EU]** Garantir que o cliente use identidades e dados sintéticos.

## 4. NFS — infraestrutura de apoio

- [ ] **[VOCÊ][PORTÃO]** Confirmar servidor, export, filesystem subjacente, capacidade entre 4 e 8 TB e espaço livre.
- [ ] **[VOCÊ]** Criar diretório exclusivo para o projeto, sem reutilizar pasta de produção.
- [ ] **[VOCÊ]** Restringir o export às origens necessárias.
- [ ] **[VOCÊ]** Definir UID/GID e permissões de escrita.
- [ ] **[VOCÊ]** Montar preferencialmente no host-00, evitando que os alvos escrevam diretamente no repositório.
- [ ] **[CONJUNTO][PORTÃO]** Testar criar, sincronizar, ler, calcular hash e remover um artefato sintético.
- [ ] **[EU]** Criar estrutura:

  ```text
  EXP-XXXX/
  ├── input/
  ├── events/
  ├── manifests/
  ├── custody/
  ├── evidence/
  └── results/
  ```

- [ ] **[EU]** Criar transferência atômica, verificação SHA-256 e evento de custódia.
- [ ] **[EU]** Registrar `classe_armazenamento=REMOTO_NFS` e `caminho_uri`.
- [ ] **[EU]** Impedir inclusão na amostra enquanto o hash remoto não for verificado.

## 5. Artefatos que você precisa preparar ou decidir

- [ ] **[VOCÊ][PORTÃO]** Endereços físicos, interfaces, gateway e DNS.
- [ ] **[VOCÊ][PORTÃO]** Realm Kerberos, base DN LDAP e domínio Samba.
- [ ] **[VOCÊ][PORTÃO]** Endereço/export do NFS e permissões.
- [ ] **[VOCÊ]** Imagem Debian Incus disponível localmente.
- [ ] **[VOCÊ]** Chave SSH Ed25519 da conta de automação.
- [ ] **[VOCÊ]** Senha de desbloqueio do Vault, mantida fora do Git.
- [ ] **[VOCÊ]** Identidades e arquivos sintéticos que representarão o uso legítimo.
- [ ] **[VOCÊ]** Janela de manutenção para testar rede/roteamento sem risco ao acesso remoto.

## 6. Artefatos que serão criados por mim

- [ ] **[EU]** DOML-F específica do C01.
- [ ] **[EU]** Inventário Ansible e variáveis sem segredos.
- [ ] **[EU]** Roles de baseline, Incus, rede, OpenLDAP, Kerberos, Samba, SSH e cliente.
- [ ] **[EU]** Playbooks de pré-voo, implantação, validação, coleta, selamento e restauração.
- [ ] **[EU]** Templates de `nftables`, rotas, resolução de nomes e configurações dos serviços.
- [ ] **[EU]** Coletor de baseline físico/lógico.
- [ ] **[EU]** Callback Ansible para eventos JSONL.
- [ ] **[EU]** Validação dos eventos contra JSON Schema.
- [ ] **[EU]** Streams, cadeia de hashes e ledger.
- [ ] **[EU]** Manifesto determinístico e assinatura/verificação Ed25519.
- [ ] **[EU]** Eventos de custódia e transferência ao NFS.
- [ ] **[EU]** Exportador JSONL → matriz experimental v0.3.
- [ ] **[EU]** Testes automatizados unitários e de integração.
- [ ] **[EU]** Runbook da execução exploratória C01.
- [ ] **[EU]** Relatório automático de pré-condições e portões.

## 7. Arquivos de baseline que deverão ser produzidos

- [ ] **[EU]** Por host físico:

  ```text
  host-identity.json
  os-release.txt
  uname.txt
  hardware.json
  packages.tsv
  mounts.txt
  btrfs-baseline.txt
  incus-info.json
  incus-storage.json
  ip-address.txt
  routes.txt
  network-config.tar
  nftables-ruleset.nft
  ntp-status.json
  resource-usage.json
  services.txt
  file-hashes.sha256
  ```

- [ ] **[EU]** Por instância:

  ```text
  instance-config.json
  image-fingerprint.txt
  packages.tsv
  services.txt
  effective-config/
  functional-tests.json
  logs/
  file-hashes.sha256
  ```

- [ ] **[EU]** No controlador:

  ```text
  git-status.txt
  component-versions.json
  inventory.sha256
  ansible-output.log
  events.jsonl
  ledger.jsonl
  manifest.json
  manifest.sig
  custody.jsonl
  ```

## 8. Congelamento antes da execução

- [ ] **[CONJUNTO][PORTÃO]** Repositório Git limpo.
- [ ] **[EU]** Registrar:

  - `doml_commit`;
  - `ansible_commit`;
  - `validator_version`;
  - `protocol_version`;
  - `schema_version`;
  - `projection_version`;
  - `inventory_hash`;
  - fingerprint da imagem Incus;
  - hash do material cifrado do Vault.

- [ ] **[CONJUNTO][PORTÃO]** Validar que nenhuma configuração foi alterada depois do congelamento.
- [ ] **[EU]** Fazer o executor recusar árvore Git suja, salvo modo exploratório explicitamente marcado.

## 9. Portões automáticos do C01

- [ ] **[EU]** `G01`: identidade e hostname corretos.
- [ ] **[EU]** `G02`: hardware e versões compatíveis com o protocolo.
- [ ] **[EU]** `G03`: relógio sincronizado e offset ≤1 s.
- [ ] **[EU]** `G04`: Git limpo e componentes identificados.
- [ ] **[EU]** `G05`: imagem Incus disponível e fingerprint correta.
- [ ] **[EU]** `G06`: instâncias residuais ausentes.
- [ ] **[EU]** `G07`: redes não sobrepostas, rotas e filtros válidos.
- [ ] **[EU]** `G08`: espaço local dentro do limite.
- [ ] **[EU]** `G09`: NFS disponível e gravável.
- [ ] **[EU]** `G10`: SSH, sudo e Vault operacionais.
- [ ] **[EU]** `G11`: DOML-F aprovada sintática, semântica e forensemente.
- [ ] **[EU]** `G12`: diretório da execução criado e IDs emitidos.

## 10. Evidências e critérios de sucesso

- [ ] **[EU]** Capturar eventos JSONL de início/fim, Ansible, validações, coleta, custódia e selamento.
- [ ] **[EU]** Preservar saída integral, código de retorno e duração do Ansible.
- [ ] **[EU]** Validar OpenLDAP por busca autenticada.
- [ ] **[EU]** Validar Kerberos por obtenção e validação de TGT sintético.
- [ ] **[EU]** Validar Samba por autenticação, leitura e escrita controladas.
- [ ] **[EU]** Validar SSH por chave e comando não destrutivo.
- [ ] **[EU]** Verificar streams, ledger, manifesto, assinatura e hashes local/remoto.
- [ ] **[CONJUNTO]** Classificar a execução como sucesso, falha válida, aborto ou exclusão.

Uma falha causada por DOML-F, Ansible, validador, coletor ou serviço é resultado experimental válido. Falha externa documentada pode invalidar a execução, mas seus registros não são apagados.

## 11. Preparação posterior de C05 e C06

- [ ] **[EU]** C05: comparar estados antes/depois e classificar cada alteração.
- [ ] **[EU]** C05: exigir zero alteração indevida para declarar idempotência.
- [ ] **[EU]** C06: recriar instâncias em host equivalente com os mesmos artefatos.
- [ ] **[CONJUNTO]** Definir previamente campos variáveis permitidos.
- [ ] **[EU]** Separar diferenças permitidas de divergências estruturais.
- [ ] **[EU]** Não incluir C05/C06 na amostra antes de seus procedimentos determinísticos serem congelados.

## 12. Registro de divergências

- [ ] **[EU]** Gerar ID único e registrar esperado × observado.
- [ ] **[EU]** Vincular requisito, cenário, host, etapa, artefato e evidências.
- [ ] **[EU]** Classificar categoria, criticidade e impacto.
- [ ] **[CONJUNTO]** Registrar causa confirmada ou hipótese marcada.
- [ ] **[CONJUNTO]** Decidir entre aceitar, corrigir em nova versão, repetir ou excluir.
- [ ] **[EU]** Produzir evento corretivo; nunca sobrescrever evento aceito.

## 13. Sequência recomendada de trabalho

1. **[VOCÊ]** fornecer endereços, interfaces, domínio/realm/base DN e NFS;
2. **[VOCÊ]** instalar e atualizar host-00 e hosts 01–03;
3. **[VOCÊ]** disponibilizar imagem Incus, contas, chaves e NFS;
4. **[EU]** produzir inventário, DOML, roles, playbooks e coletores;
5. **[CONJUNTO]** validar rede e acesso sem risco ao gerenciamento remoto;
6. **[EU]** executar/avaliar os portões automáticos;
7. **[CONJUNTO]** realizar uma execução exploratória C01;
8. **[EU]** corrigir o instrumento e congelar timeout;
9. **[CONJUNTO]** iniciar `N0=5` somente sem pendências P0.

## 14. Critério de prontidão imediata

Para eu começar a gerar a automação, você não precisa concluir toda a preparação. Basta fornecer primeiro:

- [x] IPv4 físico e nome da interface do host-00;
- [ ] IPv4 físico e nome da interface dos hosts 01–03;
- [ ] confirmar realm `FORANSI.TEST`, base DN `dc=foransi,dc=test` e workgroup `FORANSI`;
- [ ] endereço e export NFS;
- [x] confirmação do gerenciador de rede do host-00: `ifupdown`;
- [ ] confirmação de que a imagem Debian Incus está disponível;
- [x] confirmação de que o host-00 está instalado;
- [ ] concluir instalação dos pacotes de controle indicados.

Com esses seis grupos de dados, a implementação pode começar em paralelo à preparação física.

## 15. Referências de verificação

- Debian, *Verifying authenticity of Debian images*: https://www.debian.org/CD/verify
- Debian, página de download do instalador 13.7: https://www.debian.org/download
- RFC 6761, domínio especial `.test`: https://www.rfc-editor.org/rfc/rfc6761
