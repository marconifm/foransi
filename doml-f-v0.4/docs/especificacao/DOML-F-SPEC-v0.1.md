# DOML-F Specification v0.1

**DOML-F --- DevOps Modeling Language for Forensic Laboratories**\
Status: Draft implementável\
Versão: 0.1.0\
Data: 2026-09-09

## 1. Finalidade

DOML-F é uma especialização orientada a modelos para descrever, validar,
materializar e auditar laboratórios forenses cibernéticos reproduzíveis.

O modelo é a fonte declarativa da intenção do ambiente. Ansible, Incus e
demais mecanismos são implementadores derivados do modelo.

DOML-F não substitui Ansible ou Incus: ela define o estado desejado, as
relações, restrições, requisitos experimentais e propriedades forenses
que esses mecanismos devem materializar.

## 2. Princípios normativos

Os termos MUST, MUST NOT, SHOULD, SHOULD NOT e MAY possuem o significado
convencional de requisitos normativos.

1.  O modelo DOML-F MUST ser versionado.
2.  Cada objeto referenciável MUST possuir `id` único no modelo.
3.  Referências MUST apontar para objetos existentes.
4.  Configuração crítica MUST ser derivável do modelo ou de artefatos
    explicitamente declarados como derivados.
5.  Segredos MUST NOT ser armazenados em texto claro no modelo.
6.  Um experimento MUST referenciar versão imutável do modelo.
7.  Evidência MUST possuir origem, experimento, timestamp UTC, método e
    hash.
8.  Ataques MUST possuir fonte, alvo, escopo e critérios de
    encerramento.
9.  A rede de evidências MUST ser segregada da rede de ataque.
10. Um modelo inválido MUST NOT ser provisionado.
11. O estado instalado SHOULD ser exportável e comparável ao estado
    desejado.
12. O ambiente MUST permitir restore antes da repetição de um cenário
    destrutivo.

## 3. Arquitetura em camadas

### 3.1 Meta Layer

Contém identidade do documento, versão da linguagem, schema e metadados.

### 3.2 Application Layer

Descreve serviços e componentes funcionais sem depender do mecanismo
concreto de execução.

### 3.3 Abstract Infrastructure Layer

Descreve nós, redes, volumes, armazenamento e relações de infraestrutura
de maneira independente do fornecedor.

### 3.4 Concrete Infrastructure Layer

Mapeia abstrações para Debian, Incus, BTRFS, Ansible e demais
implementações concretas.

### 3.5 Experimental/Forensic Layer

Acrescenta cenários, ataques, baselines, ground truth, coleta,
evidências, manifestos, cadeia de custódia, métricas e validações.

## 4. Entidades

As entidades mínimas da versão 0.1 são:

-   `model`
-   `metadata`
-   `provider`
-   `objective`
-   `use_case`
-   `network`
-   `storage`
-   `image`
-   `node`
-   `identity`
-   `service`
-   `telemetry`
-   `hardening`
-   `scenario`
-   `attack`
-   `baseline`
-   `ground_truth`
-   `collection`
-   `experiment`
-   `evidence`
-   `custody_event`
-   `manifest`
-   `validation`
-   `secret_ref`

## 5. Modelo de identidade

Todo objeto referenciável MUST possuir:

``` yaml
id: unique-identifier
type: object-type
```

Objetos versionáveis SHOULD possuir `version`. Identidade lógica e
versão são conceitos distintos: alteração de atributos não cria novo
`id` quando a identidade semântica permanece a mesma.

IDs MUST ser estáveis entre versões do modelo enquanto representarem a
mesma entidade lógica.

## 6. Relações

Relações possuem:

``` yaml
relations:
  - type: requires
    source: object-a
    target: object-b
```

Tipos iniciais:

-   `requires`
-   `depends_on`
-   `provides`
-   `connects_to`
-   `hosts`
-   `uses`
-   `collects`
-   `attacks`
-   `observes`
-   `generates`
-   `derived_from`
-   `contains`

Relações MUST referenciar objetos existentes.

Relações de dependência (`requires`, `depends_on`) MUST formar um grafo
acíclico no escopo em que representam pré-requisitos de materialização.

## 7. Redes

Tipos iniciais:

-   `management`
-   `target`
-   `attack`
-   `evidence`

Regras:

-   `management` é destinada à administração e provisionamento.
-   `target` contém ativos submetidos aos cenários.
-   `attack` contém ferramentas e atores ofensivos.
-   `evidence` contém coletores e armazenamento de evidências.
-   `attack` MUST NOT possuir conectividade irrestrita com `evidence`.
-   tráfego destinado a redes externas MUST ser explicitamente proibido
    ou controlado no perfil de laboratório.
-   um nó com múltiplas redes MUST declarar explicitamente suas
    interfaces.

## 8. Nós

Tipos:

-   `physical`
-   `container`
-   `vm`

Papéis:

-   `infrastructure`
-   `attacker`
-   `target`
-   `identity`
-   `collector`
-   `forensic`
-   `monitoring`

Um `container` MUST referenciar imagem compatível. Uma `vm` MUST possuir
definição de recursos e armazenamento de disco.

Privilégios elevados são exceção e MUST possuir justificativa.

## 9. Serviços

Serviços suportados no perfil inicial:

-   PostgreSQL
-   MariaDB
-   Apache/PHP
-   Samba
-   BIND
-   Kea
-   OpenLDAP
-   MIT Kerberos
-   SSH
-   SSSD
-   logging

Cada serviço MUST declarar nó hospedeiro e SHOULD declarar versão quando
esta for relevante ao experimento.

## 10. Telemetria

Uma fonte de telemetria MUST declarar:

-   origem;
-   tipo;
-   retenção;
-   associação a experimento, quando aplicável.

Fontes podem incluir logs de sistema, autenticação, web, banco, LDAP,
Kerberos, Samba, DNS, DHCP, firewall e captura de rede.

## 11. Hardening

Um perfil de hardening MUST possuir:

-   identificador;
-   versão;
-   alvo;
-   controles aplicáveis.

O resultado do hardening MUST ser verificável.

## 12. Cenários e ataques

Um cenário MUST declarar:

-   objetivo ou hipótese;
-   escopo;
-   entradas controladas;
-   critérios de sucesso;
-   critérios de falha;
-   IOCs esperados;
-   artefatos esperados.

Um ataque MUST declarar:

-   fonte;
-   alvo;
-   cenário;
-   ferramenta;
-   versão da ferramenta, quando relevante;
-   autorização/escopo;
-   mecanismo de abortamento;
-   runbook ou referência equivalente.

Ataques MUST ocorrer somente contra objetos pertencentes ao escopo
experimental.

## 13. Baseline

Baseline representa o estado conhecido e aprovado antes da execução.

Um baseline MUST referenciar:

-   modelo;
-   alvo(s);
-   método de criação;
-   estado de integridade;
-   snapshot/export quando aplicável.

Um experimento destrutivo MUST possuir baseline válido antes de
`RUNNING`.

## 14. Ground truth

Quando o cenário possuir eventos previamente conhecidos, estes MAY ser
descritos como `ground_truth`.

Ground truth representa o que o experimento deliberadamente produziu,
não o que a coleta conseguiu observar.

Isso permite medir cobertura e completude:

`observed_evidence / expected_artifacts`.

## 15. Experimentos

Estados:

`DRAFT -> VALIDATED -> PROVISIONED -> BASELINED -> READY -> RUNNING -> COLLECTING -> SEALED -> ANALYZED -> RESTORED -> COMPLETED`

Estados de exceção:

`INVALID`, `FAILED`, `ABORTED`, `CONTAMINATED`.

Transições inválidas MUST ser rejeitadas.

Um experimento MUST registrar:

-   `id`;
-   modelo e versão;
-   cenário;
-   baseline;
-   ataque;
-   entradas controladas;
-   timestamps UTC;
-   markers de início e fim;
-   coleta;
-   resultado;
-   anomalias/desvios.

## 16. Evidências

Uma evidência MUST conter:

``` yaml
id:
experiment:
source:
collected_at:
method:
hash:
```

`hash` MUST declarar algoritmo e valor.

Métodos iniciais:

-   `snapshot`
-   `export`
-   `filesystem`
-   `logical`
-   `memory`
-   `network_capture`
-   `log_export`
-   `configuration_export`

`memory` é reservado para VMs e outras fontes explicitamente suportadas;
não implica aquisição completa de memória de containers.

## 17. Cadeia de custódia

Eventos mínimos:

-   `collected`
-   `sealed`
-   `transferred`
-   `analyzed`
-   `archived`

Cada evento MUST conter:

-   timestamp UTC;
-   responsável;
-   ação;
-   evidência afetada.

## 18. Manifestos

Um manifesto MUST permitir reconstruir a relação:

`evidence -> experiment -> model version -> environment version`.

Deve incluir:

-   caso/experimento;
-   evidências;
-   origem;
-   timestamps;
-   hashes;
-   método;
-   versão do ambiente;
-   ferramenta de coleta;
-   cadeia de custódia.

Assinatura digital é SHOULD na v0.1.

## 19. Estado desejado versus observado

DOML-F define o estado desejado.

O provisionamento produz estado observado.

Divergências iniciais:

-   `missing`
-   `unexpected`
-   `modified`
-   `unknown`

A comparação MUST identificar o objeto afetado e o tipo de divergência.

## 20. Segredos

Segredos são representados por referências:

``` yaml
secret_ref:
  id: ldap-admin-password
  provider: external-secret-store
```

O valor secreto MUST NOT aparecer no modelo, manifesto, inventário
versionado ou código gerado.

## 21. Validação

Três níveis:

### Sintática

Schema, tipos, campos obrigatórios e estrutura.

### Semântica

Referências, dependências, relações, recursos, topologia e
compatibilidade.

### Segurança/forense

Isolamento, evidências, baseline, coleta, hashes, escopo ofensivo e
cadeia de custódia.

Formalmente:

`VALID(model) = syntax && semantics && security_forensics`.

Somente modelos `VALID=true` podem entrar na fase de materialização.

## 22. Invariantes

-   `INV-001`: IDs são únicos.
-   `INV-002`: toda referência resolve para objeto existente.
-   `INV-003`: dependências não possuem ciclos.
-   `INV-004`: evidência possui hash.
-   `INV-005`: evidência pertence a experimento existente.
-   `INV-006`: experimento referencia versão de modelo.
-   `INV-007`: ataque possui fonte e alvo.
-   `INV-008`: fonte e alvo pertencem ao escopo do experimento.
-   `INV-009`: atacante não possui acesso irrestrito à rede de
    evidências.
-   `INV-010`: segredos não possuem valor literal no modelo.
-   `INV-011`: experimento destrutivo possui baseline válido.
-   `INV-012`: estado `RUNNING` só é alcançável após `READY`.
-   `INV-013`: `COMPLETED` exige coleta e resultado registrados.
-   `INV-014`: `RESTORED` exige validação de restauração.
-   `INV-015`: configuração crítica é derivável do modelo ou
    explicitamente declarada como artefato derivado.
-   `INV-016`: objetos de evidência são imutáveis após `SEALED`, salvo
    criação de nova versão ou evento de custódia.

## 23. Regras normativas

### Identidade e modelo

`DOML-R001` todo objeto referenciável possui ID único.\
`DOML-R002` IDs estáveis preservam identidade lógica.\
`DOML-R003` referências devem resolver.\
`DOML-R004` tipos devem pertencer ao vocabulário permitido.\
`DOML-R005` alterações do modelo devem incrementar sua versão.

### Infraestrutura

`DOML-R010` nó deve possuir tipo válido.\
`DOML-R011` container deve possuir imagem.\
`DOML-R012` VM deve possuir recursos e disco.\
`DOML-R013` rede deve possuir finalidade válida.\
`DOML-R014` dependências devem ser acíclicas.

### Segurança

`DOML-R020` plano de gerenciamento deve ser segregado dos alvos.\
`DOML-R021` atacante deve ser isolado de evidências.\
`DOML-R022` tráfego externo do laboratório deve ser negado por padrão.\
`DOML-R023` privilégio elevado deve ser justificado.\
`DOML-R024` segredo não pode ser literal no modelo.\
`DOML-R025` ferramenta ofensiva deve ser inventariada.

### Forense

`DOML-R030` evidência possui origem.\
`DOML-R031` evidência possui timestamp UTC.\
`DOML-R032` evidência possui hash.\
`DOML-R033` evidência possui método de coleta.\
`DOML-R034` evidência referencia experimento.\
`DOML-R035` manifesto referencia versão do ambiente.\
`DOML-R036` cadeia de custódia registra responsável e transferências.

### Experimentos

`DOML-R040` experimento possui objetivo/hipótese.\
`DOML-R041` experimento possui escopo.\
`DOML-R042` experimento possui baseline quando requerido.\
`DOML-R043` experimento possui ataque ou cenário.\
`DOML-R044` cenário possui critérios de sucesso e falha.\
`DOML-R045` cenário possui IOCs e artefatos esperados.\
`DOML-R046` início e fim são marcados.\
`DOML-R047` desvios são registrados.\
`DOML-R048` restore precede repetição de cenário destrutivo.

### Reprodutibilidade

`DOML-R050` DOML é fonte de verdade.\
`DOML-R051` inventário é derivado da DOML.\
`DOML-R052` configuração crítica é derivável.\
`DOML-R053` estado instalado é exportável.\
`DOML-R054` modelo e ambiente são versionados.\
`DOML-R055` software crítico possui versão registrada.\
`DOML-R056` baseline possui manifesto.\
`DOML-R057` evidências possuem manifesto.\
`DOML-R058` recriação limpa é testável.\
`DOML-R059` restore é testável.\
`DOML-R060` divergências são auditáveis.

## 24. Compatibilidade com a implementação

O perfil concreto v0.1 fixa:

-   OS: Debian 13;
-   virtualização: Incus;
-   storage primário: BTRFS;
-   provisionamento: Ansible;
-   identidade: OpenLDAP + MIT Kerberos;
-   serviços: PostgreSQL, MariaDB, Apache/PHP, Samba, BIND e Kea;
-   coleta: snapshots, exports, logs, configuração, processos/conexões
    quando viável e captura de rede;
-   hash padrão: SHA-256;
-   tempo: UTC.

O suporte futuro a Samba AD DC deve ser modelado como extensão de
infraestrutura concreta, preferencialmente em VM.

## 25. Fora do escopo da v0.1

-   cluster Incus;
-   HA de LDAP/Kerberos;
-   AD/DC completo;
-   integração com Windows real;
-   SIEM pesado;
-   agentes complexos;
-   memória completa de containers;
-   rootkits de kernel avançados;
-   container escape destrutivo;
-   dados reais;
-   exposição à internet;
-   conformidade judicial formal;
-   resposta autônoma.

## 26. Critério de conformidade do MVP

O MVP DOML-F é conforme quando:

1.  um modelo válido gera inventário;
2.  o inventário permite provisionamento via Ansible;
3.  Incus cria o ambiente;
4.  identidade funciona;
5.  serviços-alvo funcionam;
6.  telemetria é coletada;
7.  baseline é criado;
8.  ataque controlado é executado;
9.  evidências são coletadas e hashadas;
10. manifesto é gerado;
11. ambiente é restaurado;
12. cenário é repetido;
13. divergências são verificadas;
14. a cadeia modelo -\> ambiente -\> experimento -\> evidência é
    auditável.

## 27. Estratégia de implementação

A ordem recomendada é:

1.  JSON Schema;
2.  modelo YAML mínimo;
3.  validador sintático;
4.  validador semântico;
5.  validador de segurança/forense;
6.  gerador de inventário;
7.  gerador Ansible;
8.  integração Incus;
9.  baseline/snapshot;
10. executor de cenário;
11. coletor;
12. manifesto;
13. comparação desired/observed;
14. testes de recriação e restore.

A primeira implementação não deve tentar construir todos os serviços
simultaneamente. O caminho de prova deve começar por um cenário mínimo:
atacante -\> SSH -\> alvo Debian -\> logs -\> snapshot -\> evidência -\>
restore -\> repetição.
