# Especificação de Requisitos — Laboratório Forense Replicável  
**Versão:** 0.1 — pré-DOML  
**Objetivo deste documento:** definir requisitos antes da criação da DOML v0.1.  
Nesta etapa **não** estamos criando a DOML, apenas especificando o que ela deverá representar e validar.

---

## 1. Contexto e propósito

O laboratório deve permitir a construção de um ambiente replicável para análise forense de ataques contra servidores Linux baseados em **Debian 13**, usando **containers Incus**, **VMs Incus quando necessário**, **hosts físicos opcionais**, storage **BTRFS**, identidade central com **OpenLDAP + Kerberos**, serviços comuns de infraestrutura e mecanismos completos de coleta de evidências.

O foco principal é permitir que um experimento de ataque possa ser:

1. modelado;
2. provisionado de forma idempotente;
3. observado por logs e telemetria;
4. atacado de forma controlada;
5. coletado forensemente;
6. analisado;
7. restaurado;
8. repetido;
9. auditado;
10. exportado para outro ambiente compatível.

---

## 2. Decisões já incorporadas

Estas decisões fazem parte do escopo desta especificação:

| Decisão | Posição adotada |
|---|---|
| Virtualização | Containers Incus e VMs Incus quando necessário |
| Hosts físicos | Permitidos como nós complementares, desde que modelados |
| Storage | BTRFS |
| Identidade inicial | OpenLDAP + Kerberos MIT |
| Futuro AD/DC | Será atendido por Samba AD DC em VM, não por OpenLDAP puro |
| Sistema base | Debian 13 |
| Provisionamento | Ansible |
| Modelo | DOML como fonte de verdade |
| Forense | Coleta com cadeia de custódia, hashes e manifesto |
| Experimentos | Ataques controlados e reproduzíveis |

---

## 3. Objetivos do laboratório

| ID | Objetivo | Prioridade |
|---|---|---|
| OBJ-01 | Criar um ambiente replicável baseado em Debian 13, Incus e BTRFS | Must |
| OBJ-02 | Permitir análise forense de ataques com evidências íntegras | Must |
| OBJ-03 | Capacitar o sistema a replicar o modelo instalado | Must |
| OBJ-04 | Executar ataques controlados e observáveis | Must |
| OBJ-05 | Garantir logs suficientes para detecção, investigação e timeline | Must |
| OBJ-06 | Validar hardening, segurança e mecanismos de resposta | Must |
| OBJ-07 | Suportar serviços comuns: PostgreSQL, MariaDB, Apache+PHP, Samba, BIND, Kea | Must |
| OBJ-08 | Preparar evolução futura para AD/DC com Samba em VM | Should |
| OBJ-09 | Produzir métricas experimentais comparáveis entre execuções | Should |
| OBJ-10 | Permitir auditoria completa do processo de construção e coleta | Must |

---

## 4. Papéis e atores do laboratório

| Papel | Descrição |
|---|---|
| Arquiteto/Modelador | Define a DOML, topologia, cenários e critérios |
| Engenheiro de Provisionamento | Implementa Ansible, imagens, redes, storage e serviços |
| Operador de Ataque | Executa cenários ofensivos controlados |
| Analista Forense | Coleta, preserva e analisa evidências |
| Validador/QA | Confere reprodutibilidade, consistência e critérios de aceite |
| Administrador do Laboratório | Controla acesso, backups, integridade e segurança do próprio ambiente |

---

## 5. Casos de uso principais

## 5.1 Tabela de casos de uso

| ID | Caso de uso | Descrição resumida | Prioridade |
|---|---|---|---|
| UC-01 | Modelar o ambiente | Descrever topologia, nós, redes, storage, identidade, serviços e políticas | Must |
| UC-02 | Provisionar ambiente limpo | Criar ambiente completo a partir do modelo | Must |
| UC-03 | Validar baseline | Confirmar serviços, identidade, logs e integridade antes do ataque | Must |
| UC-04 | Executar ataque SSH | Simular brute force, acesso indevido e persistência via SSH | Must |
| UC-05 | Executar ataque web | Simular upload de webshell, execução de comando e persistência via Apache/PHP | Must |
| UC-06 | Atacar banco de dados | Simular acesso indevido, dump ou alteração em PostgreSQL/MariaDB | Must |
| UC-07 | Atacar identidade | Simular enumeração LDAP, senha fraca, criação de usuário ou abuso de Kerberos | Must |
| UC-08 | Abusar de Samba | Simular acesso indevido a share, alteração/exclusão de arquivos ou ransomware sintético | Should |
| UC-09 | Anomalia DNS/DHCP | Simular consultas suspeitas, rogue DHCP ou alteração indevida de zona | Should |
| UC-10 | Coletar evidências pós-ataque | Executar coleta volátil, snapshots, exports, logs e metadados | Must |
| UC-11 | Analisar evidências | Montar/ler evidências em estação forense isolada, somente leitura | Must |
| UC-12 | Restaurar ambiente | Retornar ao estado limpo via snapshot ou re-provisionamento | Must |
| UC-13 | Replicar ambiente | Exportar e reconstruir o laboratório em outro host compatível | Must |
| UC-14 | Auditar experimento | Verificar hashes, manifests, logs de execução e consistência | Must |
| UC-15 | Testar resposta a incidente | Aplicar contenção, bloqueio, hardening adicional e validar efeito | Should |
| UC-16 | Evoluir para AD/DC | Adicionar futura VM Samba AD DC sem quebrar coleta e reprodutibilidade | Could |

---

## 5.2 Detalhamento dos casos de uso críticos

### UC-01 — Modelar o ambiente

**Descrição:**  
O operador define declarativamente todos os elementos do laboratório.

**Entradas:**
- topologia de rede;
- lista de containers/VMs;
- storage;
- identidade;
- serviços;
- políticas de segurança;
- cenários de ataque;
- requisitos de evidência.

**Saídas:**
- modelo validável;
- inventário gerável;
- parâmetros de provisionamento.

**Critério de aceite:**
- nenhuma configuração relevante pode depender de ação manual;
- o modelo deve permitir validação de consistência antes do provisionamento.

---

### UC-02 — Provisionar ambiente limpo

**Descrição:**  
O sistema constrói o laboratório a partir do modelo.

**Fluxo principal:**
1. preparar host e storage;
2. criar redes e perfis;
3. criar imagens base;
4. instanciar containers/VMs;
5. aplicar identidade;
6. instalar serviços;
7. configurar telemetria;
8. gerar baseline.

**Critério de aceite:**
- provisionamento idempotente;
- ambiente recriável;
- validação automática de serviços;
- logs de execução preservados.

---

### UC-03 — Validar baseline

**Descrição:**  
Validar que o ambiente está limpo, íntegro e observável.

**Critérios de aceite:**
- serviços respondem conforme esperado;
- identidade central funciona;
- logs estão chegando ao coletor;
- hashes de baseline gerados;
- snapshots iniciais criados;
- nenhum artefato de ataque presente.

---

### UC-04 — Executar ataque SSH

**Descrição:**  
Simular ataque contra serviço SSH.

**Exemplos:**
- brute force;
- credential stuffing;
- chave não autorizada;
- criação de usuário malicioso;
- persistência em `authorized_keys`;
- alteração de configuração.

**Evidências mínimas:**
- logs de autenticação;
- auditoria de arquivos;
- processos;
- conexões;
- usuários criados;
- chaves inseridas;
- snapshot pós-ataque.

---

### UC-05 — Executar ataque web

**Descrição:**  
Simular comprometimento de aplicação Apache+PHP.

**Exemplos:**
- upload de webshell;
- execução de comando;
- escrita em diretório web;
- reverse shell;
- persistência via cron ou arquivo PHP.

**Evidências mínimas:**
- access log;
- error log;
- arquivos criados;
- processos iniciados;
- conexões de saída;
- snapshot do filesystem;
- logs centralizados.

---

### UC-06 — Atacar banco de dados

**Descrição:**  
Simular abuso de PostgreSQL ou MariaDB.

**Exemplos:**
- login indevido;
- dump de dados;
- alteração de grants;
- criação de usuário;
- execução de comandos administrativos.

**Evidências mínimas:**
- logs de autenticação;
- logs de conexão;
- logs de consultas relevantes;
- alterações de usuários;
- arquivos de dump, se houver;
- snapshot consistente.

---

### UC-10 — Coletar evidências pós-ataque

**Descrição:**  
Coletar artefatos preservando integridade.

**Princípios:**
- respeitar ordem de volatilidade;
- minimizar alteração do alvo;
- registrar hashes;
- gerar manifesto;
- documentar cadeia de custódia.

**Critério de aceite:**
- evidências verificáveis por hash;
- manifesto completo;
- coleta replicável;
- análise possível em ambiente isolado.

---

### UC-13 — Replicar ambiente

**Descrição:**  
Exportar o laboratório e recriá-lo em outro host compatível.

**Artefatos necessários:**
- modelo;
- imagens;
- snapshots;
- exports de containers/VMs;
- manifests;
- backups de identidade;
- configurações de rede e storage;
- documentação de execução.

**Critério de aceite:**
- ambiente restaurado com mesma identidade funcional;
- hashes conferem;
- serviços voltam a operar;
- logs e evidências permanecem auditáveis.

---

## 6. Requisitos Funcionais

## 6.1 Modelagem e provisionamento

| ID | Requisito | Prioridade |
|---|---|---|
| RF-MOD-01 | O ambiente deve ser descrito por modelo declarativo único, futuramente materializado na DOML | Must |
| RF-MOD-02 | O modelo deve descrever nós, redes, storage, identidade, serviços, telemetria, ataques e evidências | Must |
| RF-MOD-03 | O modelo deve permitir versionamento e auditoria de mudanças | Must |
| RF-MOD-04 | O modelo deve suportar containers, VMs e hosts físicos opcionais | Must |
| RF-PROV-01 | O provisionamento deve ser executado por Ansible | Must |
| RF-PROV-02 | O provisionamento deve ser idempotente | Must |
| RF-PROV-03 | O provisionamento deve gerar inventário a partir do modelo | Must |
| RF-PROV-04 | Nenhuma configuração crítica deve depender de ajuste manual | Must |
| RF-PROV-05 | O sistema deve registrar logs de execução do provisionamento | Must |
| RF-PROV-06 | O sistema deve permitir validação em modo check antes da aplicação | Should |
| RF-PROV-07 | O sistema deve suportar imagens base imutáveis e versionadas | Must |
| RF-PROV-08 | O sistema deve permitir recriação completa do ambiente | Must |

---

## 6.2 Arquitetura de execução

| ID | Requisito | Prioridade |
|---|---|---|
| RF-ARC-01 | O ambiente deve suportar containers Incus com systemd | Must |
| RF-ARC-02 | O ambiente deve suportar VMs Incus para casos de memória, kernel ou AD/DC | Must |
| RF-ARC-03 | O ambiente deve suportar hosts físicos como nós complementares, se necessário | Could |
| RF-ARC-04 | O host Incus deve ser tratado como parte do escopo forense | Must |
| RF-ARC-05 | A arquitetura deve separar plano de gerenciamento, alvos, atacante e evidências | Must |
| RF-ARC-06 | O ambiente deve permitir perfis distintos por tipo de nó | Must |
| RF-ARC-07 | O ambiente deve permitir limites de CPU, memória e disco por nó | Should |
| RF-ARC-08 | O ambiente deve suportar expansão futura sem perda de rastreabilidade | Should |

---

## 6.3 Storage e snapshots

| ID | Requisito | Prioridade |
|---|---|---|
| RF-STO-01 | O storage principal deve usar BTRFS | Must |
| RF-STO-02 | O ambiente deve suportar snapshots por subvolume | Must |
| RF-STO-03 | Snapshots devem ser nomeados de forma determinística | Must |
| RF-STO-04 | O ambiente deve suportar quotas ou controle de uso de disco | Should |
| RF-STO-05 | Deve existir armazenamento separado para evidências | Must |
| RF-STO-06 | O armazenamento de evidências deve ser logicamente isolado dos alvos | Must |
| RF-STO-07 | O ambiente deve permitir exportação de snapshots ou volumes | Must |
| RF-STO-08 | O ambiente deve suportar restauração a partir de snapshot | Must |
| RF-STO-09 | Snapshots de bancos de dados devem observar política de consistência | Must |
| RF-STO-10 | O sistema deve registrar metadados de snapshot: origem, data, motivo, hash quando aplicável | Must |

---

## 6.4 Redes

| ID | Requisito | Prioridade |
|---|---|---|
| RF-NET-01 | O ambiente deve possuir rede de gerenciamento isolada | Must |
| RF-NET-02 | O ambiente deve possuir rede de alvos/serviços | Must |
| RF-NET-03 | O ambiente deve possuir rede de ataque segregada | Must |
| RF-NET-04 | O ambiente deve possuir rede ou canal dedicado para evidências | Must |
| RF-NET-05 | O ambiente deve permitir firewall entre segmentos | Must |
| RF-NET-06 | O ambiente deve suportar DNS interno | Must |
| RF-NET-07 | O ambiente deve suportar DHCP interno | Should |
| RF-NET-08 | O ambiente deve permitir captura de pacotes em pontos estratégicos | Must |
| RF-NET-09 | Nenhuma interface crítica deve ficar exposta à internet pública | Must |
| RF-NET-10 | O ambiente deve suportar zonas DNS direta e reversa | Must |
| RF-NET-11 | O ambiente deve permitir controle de rotas e NAT apenas quando justificado | Should |

---

## 6.5 Identidade

| ID | Requisito | Prioridade |
|---|---|---|
| RF-IDE-01 | O ambiente deve prover OpenLDAP como diretório central | Must |
| RF-IDE-02 | O ambiente deve prover Kerberos MIT para autenticação | Must |
| RF-IDE-03 | O ambiente deve integrar usuários/grupos via SSSD ou mecanismo equivalente | Must |
| RF-IDE-04 | O ambiente deve garantir sincronismo de tempo confiável | Must |
| RF-IDE-05 | O ambiente deve possuir domínio e realm consistentes | Must |
| RF-IDE-06 | O ambiente deve suportar TLS para serviços de identidade | Must |
| RF-IDE-07 | O ambiente deve registrar operações relevantes do LDAP | Must |
| RF-IDE-08 | O ambiente deve registrar eventos relevantes do KDC | Must |
| RF-IDE-09 | O ambiente deve permitir backup e restore do diretório | Must |
| RF-IDE-10 | O ambiente deve permitir backup e restore das chaves do Kerberos | Must |
| RF-IDE-11 | O modelo deve suportar futura adição de Samba AD DC em VM | Should |
| RF-IDE-12 | O ambiente deve permitir políticas de senha e conta | Should |
| RF-IDE-13 | O ambiente deve permitir usuários sintéticos para experimentos | Must |

---

## 6.6 SSH

| ID | Requisito | Prioridade |
|---|---|---|
| RF-SSH-01 | O SSH deve suportar hardening aplicável a todos os nós relevantes | Must |
| RF-SSH-02 | O acesso direto como root deve ser desabilitado por padrão | Must |
| RF-SSH-03 | Autenticação por senha deve ser controlada e, idealmente, desabilitada | Must |
| RF-SSH-04 | O SSH deve gerar logs detalhados de autenticação | Must |
| RF-SSH-05 | O ambiente deve permitir gestão centralizada de chaves autorizadas | Must |
| RF-SSH-06 | O ambiente deve suportar restrição por usuário/grupo | Must |
| RF-SSH-07 | O ambiente deve suportar política de host keys | Should |
| RF-SSH-08 | O ambiente deve permitir futura adoção de SSH CA | Could |
| RF-SSH-09 | O SSH deve ser testável quanto a sucesso e falha de login | Must |

---

## 6.7 Serviços alvo

| ID | Requisito | Prioridade |
|---|---|---|
| RF-SVC-01 | O ambiente deve prover PostgreSQL como serviço alvo | Must |
| RF-SVC-02 | O ambiente deve prover MariaDB como serviço alvo | Must |
| RF-SVC-03 | O ambiente deve prover Apache + PHP como serviço alvo | Must |
| RF-SVC-04 | O ambiente deve prover Samba, inicialmente como file server ou member server | Must |
| RF-SVC-05 | O ambiente deve prover BIND como DNS interno | Must |
| RF-SVC-06 | O ambiente deve prover Kea como DHCP interno | Should |
| RF-SVC-07 | Cada serviço deve ter logs mínimos habilitados | Must |
| RF-SVC-08 | Cada serviço deve ter dados sintéticos | Must |
| RF-SVC-09 | Cada serviço deve possuir baseline de configuração | Must |
| RF-SVC-10 | Cada serviço deve poder ser restaurado a estado limpo | Must |
| RF-SVC-11 | Os serviços devem expor métricas ou logs suficientes para detecção | Must |
| RF-SVC-12 | O ambiente deve permitir configurar autenticação central nos serviços quando aplicável | Could |

---

## 6.8 Logs e telemetria

| ID | Requisito | Prioridade |
|---|---|---|
| RF-LOG-01 | O ambiente deve possuir servidor central de logs | Must |
| RF-LOG-02 | Os logs devem ser enviados para fora dos alvos | Must |
| RF-LOG-03 | O journald deve estar persistente nos nós relevantes | Must |
| RF-LOG-04 | O host Incus deve gerar logs próprios auditáveis | Must |
| RF-LOG-05 | Eventos do Incus devem ser coletados | Must |
| RF-LOG-06 | Logs de autenticação devem ser coletados | Must |
| RF-LOG-07 | Logs de LDAP devem ser coletados | Must |
| RF-LOG-08 | Logs de Kerberos devem ser coletados | Must |
| RF-LOG-09 | Logs de DNS devem ser coletados | Must |
| RF-LOG-10 | Logs de DHCP devem ser coletados | Should |
| RF-LOG-11 | Logs de banco de dados devem ser coletados | Must |
| RF-LOG-12 | Logs web devem ser coletados | Must |
| RF-LOG-13 | Logs de Samba devem ser coletados | Should |
| RF-LOG-14 | O ambiente deve suportar auditoria de arquivos críticos | Must |
| RF-LOG-15 | O ambiente deve suportar marcação temporal de início/fim de experimento | Must |
| RF-LOG-16 | O ambiente deve permitir retenção configurável | Should |
| RF-LOG-17 | Os logs devem usar timestamps consistentes | Must |

---

## 6.9 Ataques controlados

| ID | Requisito | Prioridade |
|---|---|---|
| RF-ATK-01 | O ambiente deve possuir nó atacante isolado | Must |
| RF-ATK-02 | O nó atacante deve ser modelado e versionado | Must |
| RF-ATK-03 | Cada ataque deve possuir runbook | Must |
| RF-ATK-04 | Cada ataque deve possuir objetivo e artefatos esperados | Must |
| RF-ATK-05 | O ambiente deve permitir ataques determinísticos | Must |
| RF-ATK-06 | O ambiente deve permitir habilitar/desabilitar controles de resposta por experimento | Should |
| RF-ATK-07 | O ambiente deve registrar início e fim do ataque | Must |
| RF-ATK-08 | O ambiente deve permitir repetição do mesmo cenário | Must |
| RF-ATK-09 | O ambiente deve suportar captura de saída do atacante quando aplicável | Should |
| RF-ATK-10 | O ambiente deve evitar que o ataque escape do laboratório | Must |

---

## 6.10 Coleta e preservação de evidências

| ID | Requisito | Prioridade |
|---|---|---|
| RF-EVI-01 | O ambiente deve permitir coleta de evidências sem contaminação evitável | Must |
| RF-EVI-02 | O ambiente deve suportar coleta volátil antes de ações destrutivas | Must |
| RF-EVI-03 | O ambiente deve suportar snapshot pós-ataque | Must |
| RF-EVI-04 | O ambiente deve suportar exportação de containers e VMs | Must |
| RF-EVI-05 | O ambiente deve suportar geração de manifesto de evidências | Must |
| RF-EVI-06 | O manifesto deve conter identificação única, origem, timestamp e hash | Must |
| RF-EVI-07 | O ambiente deve suportar hashes criptográficos das evidências | Must |
| RF-EVI-08 | O ambiente deve suportar armazenamento de evidências em área isolada | Must |
| RF-EVI-09 | O ambiente deve permitir validação posterior de integridade | Must |
| RF-EVI-10 | O ambiente deve suportar coleta de metadados do Incus | Must |
| RF-EVI-11 | O ambiente deve suportar coleta de metadados de rede | Should |
| RF-EVI-12 | O ambiente deve suportar coleta de logs remotos originais | Must |
| RF-EVI-13 | O ambiente deve suportar cadeia de custódia | Must |

---

## 6.11 Restauração e replicação

| ID | Requisito | Prioridade |
|---|---|---|
| RF-RES-01 | O ambiente deve permitir retorno ao estado limpo via snapshot | Must |
| RF-RES-02 | O ambiente deve permitir re-provisionamento completo | Must |
| RF-RES-03 | O ambiente deve permitir restauração de identidade | Must |
| RF-RES-04 | O ambiente deve permitir restauração de serviços | Must |
| RF-RES-05 | O ambiente deve permitir restauração de logs de referência | Should |
| RF-RES-06 | O ambiente deve permitir replicação em outro host compatível | Must |
| RF-RES-07 | A replicação deve preservar rastreabilidade | Must |
| RF-RES-08 | O ambiente deve permitir teste de restore | Must |
| RF-RES-09 | O ambiente deve permitir exportação de artefatos de baseline | Must |
| RF-RES-10 | O ambiente deve permitir importação de artefatos de baseline | Must |

---

## 7. Requisitos Não Funcionais

## 7.1 Desempenho e capacidade

| ID | Requisito | Prioridade |
|---|---|---|
| RNF-DES-01 | O ambiente deve suportar o MVP com containers e ao menos 1 VM simultânea | Must |
| RNF-DES-02 | Snapshots devem ser concluídos em tempo operacionalmente viável | Must |
| RNF-DES-03 | A restauração deve ser concluída em tempo compatível com uso iterativo | Must |
| RNF-DES-04 | O ambiente deve permitir medição de tempos de provisionamento, snapshot e restore | Should |
| RNF-DES-05 | O ambiente deve evitar consumo descontrolado de disco por logs ou snapshots | Must |

---

## 7.2 Confiabilidade e integridade

| ID | Requisito | Prioridade |
|---|---|---|
| RNF-CON-01 | O ambiente deve ser recriável de forma determinística | Must |
| RNF-CON-02 | O ambiente deve detectar divergência entre estado esperado e estado real | Should |
| RNF-CON-03 | Evidências devem ser verificáveis por hash | Must |
| RNF-CON-04 | Backups devem ser testados | Must |
| RNF-CON-05 | O ambiente deve permitir validação pós-provisionamento | Must |

---

## 7.3 Observabilidade

| ID | Requisito | Prioridade |
|---|---|---|
| RNF-OBS-01 | O ambiente deve permitir correlação de eventos por tempo e origem | Must |
| RNF-OBS-02 | O ambiente deve permitir busca por serviço, host e experimento | Must |
| RNF-OBS-03 | O ambiente deve preservar logs mesmo após comprometimento local do alvo | Must |
| RNF-OBS-04 | O ambiente deve permitir visualização de estado de serviços | Should |
| RNF-OBS-05 | O ambiente deve permitir auditoria de alterações de configuração | Must |

---

## 7.4 Manutenibilidade e usabilidade

| ID | Requisito | Prioridade |
|---|---|---|
| RNF-MAN-01 | Todo o ambiente deve ser documentado | Must |
| RNF-MAN-02 | Runbooks devem existir para provisionamento, ataque, coleta e restauração | Must |
| RNF-MAN-03 | O modelo deve ser legível e auditável | Must |
| RNF-MAN-04 | O ambiente deve permitir evolução incremental | Should |
| RNF-MAN-05 | O ambiente deve reduzir dependência de conhecimento tácito | Must |

---

## 7.5 Portabilidade e compatibilidade

| ID | Requisito | Prioridade |
|---|---|---|
| RNF-POR-01 | O ambiente deve ser compatível com Debian 13 | Must |
| RNF-POR-02 | O ambiente deve registrar versões de Incus, Ansible e componentes críticos | Must |
| RNF-POR-03 | O ambiente deve evitar dependências não versionadas | Must |
| RNF-POR-04 | O ambiente deve permitir migração para hosts equivalentes | Should |
| RNF-POR-05 | O ambiente deve documentar requisitos mínimos de hardware | Must |

---

## 7.6 Escalabilidade e evolução

| ID | Requisito | Prioridade |
|---|---|---|
| RNF-EVO-01 | O ambiente deve suportar adição de novos serviços | Should |
| RNF-EVO-02 | O ambiente deve suportar adição de VMs futuras | Must |
| RNF-EVO-03 | O ambiente deve suportar futuro Samba AD DC | Should |
| RNF-EVO-04 | O ambiente deve suportar futura integração com SIEM ou agentes adicionais | Could |
| RNF-EVO-05 | O ambiente deve suportar novos cenários de ataque sem perda de rastreabilidade | Must |

---

## 8. Requisitos de Segurança

## 8.1 Segurança do próprio laboratório

| ID | Requisito | Prioridade |
|---|---|---|
| SEG-01 | O laboratório deve ser isolado de redes externas não controladas | Must |
| SEG-02 | O laboratório não deve expor serviços críticos à internet | Must |
| SEG-03 | O laboratório deve usar apenas dados sintéticos | Must |
| SEG-04 | Credenciais reais não devem ser utilizadas | Must |
| SEG-05 | Segredos devem ser armazenados fora do modelo e do código | Must |
| SEG-06 | O acesso administrativo ao laboratório deve ser restrito | Must |
| SEG-07 | O plano de gerenciamento deve ser segregado dos alvos | Must |
| SEG-08 | O atacante deve ser isolado dos componentes de evidência | Must |
| SEG-09 | O ambiente deve evitar fuga de tráfego malicioso para fora do laboratório | Must |
| SEG-10 | Backups e evidências devem ter controle de acesso | Must |

---

## 8.2 Segurança dos nós e serviços

| ID | Requisito | Prioridade |
|---|---|---|
| SEG-11 | Containers devem operar com menor privilégio possível | Must |
| SEG-12 | Privilégios elevados devem ser exceção justificada | Must |
| SEG-13 | SSH deve ser endurecido por padrão | Must |
| SEG-14 | TLS deve ser usado onde houver transporte sensível | Must |
| SEG-15 | Logs remotos devem ser protegidos contra alteração indevida | Must |
| SEG-16 | O ambiente deve permitir aplicação de baseline de hardening | Must |
| SEG-17 | O ambiente deve registrar ações administrativas relevantes | Must |
| SEG-18 | O ambiente deve suportar verificação de integridade de pacotes e arquivos críticos | Should |

---

## 8.3 Segurança de identidade

| ID | Requisito | Prioridade |
|---|---|---|
| SEG-19 | O ambiente deve proteger bases LDAP e chaves Kerberos | Must |
| SEG-20 | O ambiente deve proteger keytabs e materiais sensíveis | Must |
| SEG-21 | O ambiente deve evitar exposição anônima indevida do diretório | Must |
| SEG-22 | O ambiente deve registrar tentativas de autenticação relevantes | Must |
| SEG-23 | O ambiente deve permitir revogação de acesso | Must |
| SEG-24 | O ambiente deve suportar política de senhas | Should |

---

## 8.4 Segurança experimental

| ID | Requisito | Prioridade |
|---|---|---|
| SEG-25 | Ataques devem ser executados apenas contra alvos do laboratório | Must |
| SEG-26 | Ferramentas ofensivas devem ser controladas e inventariadas | Must |
| SEG-27 | O ambiente deve permitir desabilitar ataque em caso de comportamento inesperado | Must |
| SEG-28 | O ambiente deve registrar autorização/escopo de cada campanha de teste | Should |

---

## 9. Requisitos Forenses

## 9.1 Princípios gerais

| ID | Requisito | Prioridade |
|---|---|---|
| FOR-01 | A coleta deve respeitar a ordem de volatilidade | Must |
| FOR-02 | A coleta deve minimizar alteração do estado original | Must |
| FOR-03 | Toda evidência deve possuir identificação única | Must |
| FOR-04 | Toda evidência deve possuir origem registrada | Must |
| FOR-05 | Toda evidência deve possuir timestamp UTC | Must |
| FOR-06 | Toda evidência deve possuir hash criptográfico | Must |
| FOR-07 | Toda evidência deve ser verificável posteriormente | Must |
| FOR-08 | O processo deve suportar cadeia de custódia | Must |
| FOR-09 | O processo deve suportar manifesto de evidências | Must |
| FOR-10 | A análise deve ocorrer preferencialmente em estação isolada | Must |
| FOR-11 | A análise deve ocorrer sobre cópias, não sobre originais | Must |
| FOR-12 | O ambiente deve registrar limitações de coleta conhecidas | Must |

---

## 9.2 Evidências de host

| ID | Requisito | Prioridade |
|---|---|---|
| FOR-13 | A coleta deve incluir processos relevantes do host | Must |
| FOR-14 | A coleta deve incluir conexões de rede relevantes | Must |
| FOR-15 | A coleta deve incluir usuários logados | Must |
| FOR-16 | A coleta deve incluir mounts e estado de storage | Must |
| FOR-17 | A coleta deve incluir logs do host | Must |
| FOR-18 | A coleta deve incluir auditoria do host | Must |
| FOR-19 | A coleta deve incluir estado de módulos e cgroups quando aplicável | Should |
| FOR-20 | A coleta deve incluir inventário de pacotes | Must |

---

## 9.3 Evidências de Incus

| ID | Requisito | Prioridade |
|---|---|---|
| FOR-21 | A coleta deve incluir lista e estado de containers/VMs | Must |
| FOR-22 | A coleta deve incluir configurações dos containers/VMs | Must |
| FOR-23 | A coleta deve incluir perfis, redes e storage pools | Must |
| FOR-24 | A coleta deve incluir snapshots existentes | Must |
| FOR-25 | A coleta deve incluir eventos e operações relevantes do Incus | Should |
| FOR-26 | A coleta deve permitir exportação de container/VM para análise externa | Must |

---

## 9.4 Evidências de container

| ID | Requisito | Prioridade |
|---|---|---|
| FOR-27 | A coleta deve incluir filesystem do container via snapshot/export | Must |
| FOR-28 | A coleta deve incluir logs internos do container | Must |
| FOR-29 | A coleta deve incluir processos internos quando viável | Must |
| FOR-30 | A coleta deve incluir conexões internas quando viável | Must |
| FOR-31 | A coleta deve incluir arquivos de persistência comuns | Must |
| FOR-32 | A coleta deve incluir configurações de serviços | Must |
| FOR-33 | A coleta deve incluir artefatos de usuários e SSH | Must |

---

## 9.5 Evidências de VM

| ID | Requisito | Prioridade |
|---|---|---|
| FOR-34 | VMs devem suportar aquisição de disco | Must |
| FOR-35 | VMs devem suportar aquisição de memória quando requisitado | Should |
| FOR-36 | A coleta de VM deve registrar estado de energia | Must |
| FOR-37 | A coleta de VM deve registrar configuração da VM | Must |
| FOR-38 | A coleta de VM deve suportar snapshot consistente | Must |

---

## 9.6 Evidências de rede

| ID | Requisito | Prioridade |
|---|---|---|
| FOR-39 | O ambiente deve permitir captura de pacotes | Must |
| FOR-40 | Capturas devem poder ser associadas a experimento | Must |
| FOR-41 | Capturas devem ser armazenadas com hash | Must |
| FOR-42 | Capturas devem ter retenção controlada | Should |
| FOR-43 | O ambiente deve permitir coleta de tabelas de firewall relevantes | Should |

---

## 9.7 Evidências de identidade e serviços

| ID | Requisito | Prioridade |
|---|---|---|
| FOR-44 | A coleta deve incluir logs LDAP | Must |
| FOR-45 | A coleta deve incluir logs Kerberos | Must |
| FOR-46 | A coleta deve incluir logs SSSD quando aplicável | Should |
| FOR-47 | A coleta deve incluir logs de banco | Must |
| FOR-48 | A coleta deve incluir logs web | Must |
| FOR-49 | A coleta deve incluir logs Samba | Should |
| FOR-50 | A coleta deve incluir logs DNS | Must |
| FOR-51 | A coleta deve incluir logs DHCP | Should |
| FOR-52 | A coleta deve incluir backups de identidade anteriores ao incidente | Must |

---

## 9.8 Manifesto e cadeia de custódia

| ID | Requisito | Prioridade |
|---|---|---|
| FOR-53 | O manifesto deve conter ID do caso/experimento | Must |
| FOR-54 | O manifesto deve conter ID da evidência | Must |
| FOR-55 | O manifesto deve conter origem da evidência | Must |
| FOR-56 | O manifesto deve conter timestamp UTC | Must |
| FOR-57 | O manifesto deve conter hash e algoritmo | Must |
| FOR-58 | O manifesto deve conter método de coleta | Must |
| FOR-59 | O manifesto deve conter versão do ambiente | Must |
| FOR-60 | O manifesto deve permitir assinatura criptográfica ou selo de integridade por mecanismo identificável e substituível. | Should |
| FOR-60A | A assinatura deve registrar mecanismo, algoritmo, identidade do signatário, identificação da credencial, instante da assinatura e referência à assinatura. |  |
| FOR-60B | A verificação deve permitir determinar a política ou fonte de confiança utilizada para reconhecer o signatário. |  |
| FOR-60C | A substituição ou evolução do mecanismo de assinatura não deve invalidar assinaturas históricas nem exigir alteração conceitual do manifesto. |  |
| FOR-61 | A cadeia de custódia deve registrar transferências relevantes | Must |
| FOR-62 | A cadeia de custódia deve registrar responsável/coletor | Must |

---

## 10. Requisitos Experimentais

## 10.1 Desenho experimental

| ID | Requisito | Prioridade |
|---|---|---|
| EXP-01 | Cada experimento deve possuir hipótese ou objetivo claro | Must |
| EXP-02 | Cada experimento deve possuir escopo definido | Must |
| EXP-03 | Cada experimento deve possuir entradas controladas | Must |
| EXP-04 | Cada experimento deve possível de ser repetido | Must |
| EXP-05 | Cada experimento deve registrar versão do modelo | Must |
| EXP-06 | Cada experimento deve registrar baseline usado | Must |
| EXP-07 | Cada experimento deve registrar ataque executado | Must |
| EXP-08 | Cada experimento deve registrar coleta realizada | Must |
| EXP-09 | Cada experimento deve registrar resultado observado | Must |
| EXP-10 | Cada experimento deve permitir comparação com execuções anteriores | Should |

---

## 10.2 Controle de variáveis

| ID | Requisito | Prioridade |
|---|---|---|
| EXP-11 | Versões de software devem ser controladas | Must |
| EXP-12 | Configurações devem ser controladas | Must |
| EXP-13 | Dados sintéticos devem ser controlados | Must |
| EXP-14 | Aleatoriedade deve ser limitada ou registrada | Must |
| EXP-15 | Tempo deve ser sincronizado e registrado | Must |
| EXP-16 | Rede deve ser controlada e segmentada | Must |
| EXP-17 | Credenciais de teste devem ser controladas | Must |
| EXP-18 | Ferramentas de ataque devem ser inventariadas | Must |

---

## 10.3 Cenários e métricas

| ID | Requisito | Prioridade |
|---|---|---|
| EXP-19 | Cada cenário deve possuir IOC esperados | Must |
| EXP-20 | Cada cenário deve possuir artefatos esperados | Must |
| EXP-21 | Cada cenário deve possuir critérios de sucesso | Must |
| EXP-22 | Cada cenário deve possuir critérios de falha | Must |
| EXP-23 | O ambiente deve permitir medir tempo de detecção | Should |
| EXP-24 | O ambiente deve permitir medir cobertura de logs | Should |
| EXP-25 | O ambiente deve permitir medir completude de evidências | Should |
| EXP-26 | O ambiente deve permitir medir taxa de sucesso de restauração | Must |
| EXP-27 | Cenários devem ser mapeáveis a técnicas conhecidas, quando aplicável | Could |

---

## 10.4 Execução experimental

| ID | Requisito | Prioridade |
|---|---|---|
| EXP-28 | Deve existir marker de início de experimento | Must |
| EXP-29 | Deve existir marker de fim de experimento | Must |
| EXP-30 | Deve ser possível repetir o mesmo cenário após restore | Must |
| EXP-31 | Deve ser possível executar múltiplos cenários sequencialmente | Should |
| EXP-32 | O ambiente deve registrar desvios ou anomalias do experimento | Must |
| EXP-33 | O ambiente deve permitir pausar/abortar campanha com segurança | Must |

---

## 11. Requisitos de Reprodutibilidade

## 11.1 Fonte de verdade

| ID | Requisito | Prioridade |
|---|---|---|
| REP-01 | A DOML futura deve ser a fonte de verdade do ambiente | Must |
| REP-02 | Nenhuma configuração crítica deve existir fora do modelo | Must |
| REP-03 | O inventário deve ser derivado do modelo | Must |
| REP-04 | Alterações no modelo devem ser versionadas | Must |
| REP-05 | O modelo deve ser validável antes do provisionamento | Must |
| REP-06 | O modelo deve permitir revisão de consistência contra requisitos | Must |

---

## 11.2 Idempotência e estado

| ID | Requisito | Prioridade |
|---|---|---|
| REP-07 | O provisionamento deve ser idempotente | Must |
| REP-08 | O ambiente deve permitir recriação completa | Must |
| REP-09 | O ambiente deve permitir destruição e reconstrução | Must |
| REP-10 | O ambiente deve permitir comparação entre estado esperado e real | Should |
| REP-11 | O ambiente deve registrar estado instalado como artefato | Must |
| REP-12 | O ambiente deve permitir exportação do modelo instalado | Must |

---

## 11.3 Versionamento e dependências

| ID | Requisito | Prioridade |
|---|---|---|
| REP-13 | Versões de sistema operacional, Incus e Ansible devem ser registradas | Must |
| REP-14 | Versões de imagens base devem ser registradas | Must |
| REP-15 | Versões de pacotes críticos devem ser registradas | Must |
| REP-16 | Dependências externas devem ser minimizadas ou espelhadas | Should |
| REP-17 | Certificados e chaves de teste devem ser versionados com controle | Must |
| REP-18 | Segredos não devem ser versionados em texto claro | Must |

---

## 11.4 Artefatos replicáveis

| ID | Requisito | Prioridade |
|---|---|---|
| REP-19 | O ambiente deve gerar inventário exportável | Must |
| REP-20 | O ambiente deve gerar manifesto de baseline | Must |
| REP-21 | O ambiente deve gerar manifesto de evidências | Must |
| REP-22 | O ambiente deve gerar exports de containers/VMs | Must |
| REP-23 | O ambiente deve gerar snapshots versionados | Must |
| REP-24 | O ambiente deve gerar backups de identidade | Must |
| REP-25 | O ambiente deve gerar documentação de execução | Must |
| REP-26 | O ambiente deve gerar logs de provisionamento | Must |

---

## 11.5 Validação de reprodutibilidade

| ID | Requisito | Prioridade |
|---|---|---|
| REP-27 | O ambiente deve passar por teste de recriação limpa | Must |
| REP-28 | O ambiente deve passar por teste de restore | Must |
| REP-29 | O ambiente deve passar por teste de replicação em host equivalente | Should |
| REP-30 | O ambiente deve passar por verificação de hashes | Must |
| REP-31 | O ambiente deve passar por validação funcional pós-recriação | Must |
| REP-32 | O ambiente deve permitir auditoria de divergências | Must |

---

## 12. Requisitos de Dados

| ID | Requisito | Prioridade |
|---|---|---|
| DADO-01 | Todos os dados de negócio devem ser sintéticos | Must |
| DADO-02 | Usuários devem ser fictícios | Must |
| DADO-03 | Credenciais devem ser de laboratório | Must |
| DADO-04 | Dados devem ser geráveis de forma controlada | Must |
| DADO-05 | Dados devem permitir associação a casos de uso | Must |
| DADO-06 | Dados devem ser recriáveis | Must |
| DADO-07 | Dados devem ter tamanho controlado para não degradar o laboratório | Must |
| DADO-08 | Dados sensíveis reais não devem ser usados | Must |

---

## 13. Requisitos de Aceitação Geral

O MVP será considerado aceitável quando cumprir, no mínimo:

1. provisionamento recriável via modelo + Ansible;
2. identidade OpenLDAP + Kerberos funcional;
3. SSH hardened funcional;
4. serviços alvo operacionais;
5. logs centralizados funcionais;
6. baseline íntegro gerado;
7. snapshot limpo gerado;
8. ataque controlado executado;
9. evidências coletadas com hashes;
10. manifesto gerado;
11. restauração validada;
12. repetição do experimento validada;
13. documentação mínima disponível;
14. auditoria de consistência aprovada.

---

## 14. Critérios de rastreabilidade

Cada requisito deverá ser rastreável para:

- objetivo;
- caso de uso;
- entidade futura na DOML;
- teste de validação;
- evidência de cumprimento.

### Matriz resumida de rastreabilidade

| Objetivo | Casos de uso relacionados | Grupos de requisitos |
|---|---|---|
| OBJ-01 | UC-01, UC-02, UC-12, UC-13 | RF-MOD, RF-PROV, RF-ARC, REP |
| OBJ-02 | UC-09, UC-10, UC-11 | FOR, RF-EVI |
| OBJ-03 | UC-01, UC-02, UC-13 | RF-MOD, RF-PROV, REP |
| OBJ-04 | UC-04 a UC-09 | RF-ATK, EXP |
| OBJ-05 | UC-03, UC-04 a UC-10 | RF-LOG, RNF-OBS |
| OBJ-06 | UC-03, UC-15 | SEG, RF-SSH, RF-LOG |
| OBJ-07 | UC-02, UC-03, UC-04 a UC-09 | RF-SVC |
| OBJ-08 | UC-16 | RF-IDE-11, RNF-EVO |
| OBJ-09 | UC-04 a UC-14 | EXP |
| OBJ-10 | UC-10, UC-11, UC-14 | FOR, REP |

---

## 15. Fora do escopo inicial

Ficam fora da v0.1, salvo decisão posterior:

1. cluster Incus;
2. alta disponibilidade de LDAP/Kerberos;
3. Samba AD DC completo;
4. integração com Windows real;
5. SIEM pesado;
6. agentes complexos de segurança;
7. forense de memória completa em containers;
8. rootkits de kernel avançados;
9. container escape destrutivo;
10. uso de dados reais;
11. exposição do laboratório à internet;
12. conformidade legal formal de cadeia de custódia para uso judicial;
13. automação de resposta autônoma.

---

## 16. Premissas importantes - verificar com GPT quanto adequação

1. O laboratório será usado para pesquisa e treinamento, não para produção.
2. Ataques serão executados apenas contra alvos controlados.
3. O ambiente será isolado.
4. Dados reais não serão utilizados.
5. O operador possui permissão para executar testes ofensivos no laboratório.
6. O hardware suportará Incus com containers e VMs.
7. BTRFS será usado corretamente com snapshots e subvolumes.
8. O futuro AD/DC será implementado com Samba em VM, não OpenLDAP puro.

---

## 17. Riscos relevantes já identificados

| Risco | Impacto | Mitigação |
|---|---|---|
| OpenLDAP + Kerberos complexo | Alto | Modelar identidade com cuidado, validar DNS/NTP e backup |
| Expectativa errada de AD com OpenLDAP | Alto | Tratar Samba AD DC como evolução futura em VM |
| Snapshots inconsistentes | Médio | Definir política de quiesce/stop para bancos |
| Logs insuficientes | Alto | Definir fontes mínimas obrigatórias |
| Coleta altera evidência | Alto | Procedimentos read-only e coleta volátil controlada |
| Falta de reprodutibilidade | Alto | DOML + Ansible + inventário gerado |
| Ataque não determinístico | Médio | Runbooks e variáveis controladas |
| Armazenamento insuficiente | Médio | Quotas, retenção e separação de volumes |
| VM de AD futura quebrar o modelo | Médio | Preparar extensão no modelo desde já |

---

## 18. Como estes requisitos deverão guiar a futura DOML v0.1

A DOML deverá cobrir pelo menos as seguintes entidades conceituais:

1. **objetivos**;
2. **casos de uso**;
3. **topologia de nós**;
4. **redes**;
5. **storage**;
6. **imagens**;
7. **identidade**;
8. **serviços**;
9. **telemetria**;
10. **hardening**;
11. **ataques**;
12. **evidências**;
13. **experimentos**;
14. **manifestos**;
15. **validações**.

A futura revisão de consistência deverá verificar se:

- cada requisito essencial possui entidade ou atributo correspondente;
- cada caso de uso crítico pode ser executado pelo modelo;
- cada requisito forense pode ser satisfeito pela topologia;
- cada requisito de reprodutibilidade pode ser auditável;
- nenhum requisito foi implementado fora da DOML.
