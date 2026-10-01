# Registro de decisões metodológicas — matriz v0.3

**Estado:** proposta consolidada para revisão  
**Convenção:** DM = decisão metodológica

| ID | Decisão | Justificativa | Consequência |
|---|---|---|---|
| DM-001 | Separar `execucoes` de `eventos_execucao` | A v0.2 usa o mesmo `Execução_ID` em várias etapas, misturando entidade e log | `execucao_id` identifica a execução; `evento_id` identifica cada ação |
| DM-002 | Usar nomes técnicos sem acentos em `snake_case` | Facilita SQL, scripts, validação e interoperabilidade | Rótulos amigáveis ficam na documentação, não nos identificadores |
| DM-003 | Usar `execucao_id` como FK operacional | Evita repetir `EXP` e ordinal em tabelas filhas | O experimento é obtido por relacionamento |
| DM-004 | Manter `exp` obrigatório em evidências e `execucao_id` opcional | Evidências podem existir antes, durante ou depois de uma execução | Quando ambos existirem, haverá regra de coerência |
| DM-005 | Remover `evidencia_id` de `execucoes` | Uma execução produz muitas evidências; a FK direta cria cardinalidade errada | A relação principal passa a existir em `evidencias.execucao_id` |
| DM-006 | Manter IDs próprios em idempotência e reprodução | Cada observação/comparação precisa de identidade auditável | Resolve omissões de PK da v0.2 |
| DM-007 | Separar drift de teste deliberado de detecção | A antiga `divergencias` mede alteração introduzida, não apenas drift | Criam-se `divergencias` e `testes_deteccao` |
| DM-008 | Separar validação do modelo da validação da execução | Pré-voo DOML-F e verificação experimental possuem objetos e momentos diferentes | Criam-se `validacoes_modelo` e `validacoes_execucao` |
| DM-009 | Registrar transições, não apenas o estado atual | Auditabilidade exige reconstrução cronológica | Cria-se `transicoes_experimento`; `estado_atual` pode ser derivado |
| DM-010 | Adicionar `scenario_id`, `attack_id`, `baseline_id` | A v0.2 não permite reconstruir a configuração experimental DOML-F | Os campos são condicionais conforme o tipo de experimento |
| DM-011 | Implementar trilha de custódia experimental alinhada à ISO/IEC 27037 | A simples coluna `integridade` não registra identificação, coleta, aquisição e preservação | Eventos de custódia registram a fase normativa; não se alega cadeia legal completa |
| DM-012 | Separar definição de métrica, medição e resultado | A v0.2 mistura definição, observação e consolidação | Criam-se `metricas`, `medicoes` e `resultados` |
| DM-013 | Usar `resultado_id` e versionar o cálculo | A PK composta sugerida impediria preservar recalculações | UK em (`exp`, `metrica_id`, `versao_calculo`) |
| DM-014 | Padronizar tempo em UTC e ISO 8601 | Evita ambiguidade temporal e favorece correlação forense | Campos temporais recebem sufixo `_utc` |
| DM-015 | Tratar duração e tempo de detecção como derivados | Digitação manual pode contradizer timestamps | Armazenamento em milissegundos e verificação automática |
| DM-016 | Distinguir booleano de texto explicativo | Campos híbridos impedem validação | Usa-se booleano mais campo de descrição quando necessário |
| DM-017 | Não sobrescrever a matriz v0.2 | A v0.2 é fonte histórica da auditoria | A v0.3 será novo artefato com migração documentada |
| DM-018 | Usar JSONL validado como fonte primária | Preenchimento pós-teste em ODS perde precisão e favorece inconsistência | ODS e SQL passam a ser projeções geradas por exportador |
| DM-019 | Automatizar eventos, medições, evidências e manifestos | Tempos e relações precisam ser capturados no instante da execução | Orquestrador, callback Ansible, coletores e selador emitem registros estruturados |
| DM-020 | Vincular atores à camada AAA | Strings livres enfraquecem autenticação, responsabilização e não repúdio | Cria-se `identidades_atores`; tabelas usam `ator_id` como FK |
| DM-021 | Registrar fingerprints e assinatura sem armazenar segredos | Kerberos/LDAP autenticam no domínio, mas a origem do manifesto precisa ser verificável | Registra-se principal, método, fingerprints e assinatura; proíbem-se contas compartilhadas |
| DM-022 | Usar relógio UTC e monotônico | UTC correlaciona eventos, mas pode sofrer ajuste durante a execução | Duração deriva do relógio monotônico; UTC permanece para linha temporal |
| DM-023 | Adotar desenho estatístico em duas etapas | O `N` final depende da variabilidade real e não deve ser arbitrário | Piloto `N0=5`; piso `N=10`; ajuste por IC95%, teto operacional `N=30` |
| DM-024 | Tratar overhead de autenticação como comparação pareada | Medidas no mesmo ambiente reduzem variabilidade e evitam comparação artificial | Calculam-se diferenças por execução; logins internos não contam como experimentos independentes |
| DM-025 | Adotar JCS/RFC 8785 | Hashes precisam ser reproduzíveis entre implementações | Eventos são canonicalizados com JCS antes de hash/assinatura |
| DM-026 | Usar stream por instância emissora e ciclo de inicialização | Sequenciador global criaria contenção e ponto único de falha | Cada stream possui sequência e cadeia próprias; reinício cria novo stream |
| DM-027 | Criar ledger separado da execução | Streams independentes não fornecem ordem global de aceitação | Agregador registra referências imutáveis sem reescrever eventos |
| DM-028 | Representar nanossegundos como strings decimais | Inteiros podem superar a precisão exata de I-JSON/IEEE 754 | Cálculo usa inteiro arbitrário; JSON preserva valor exato |
| DM-029 | Corrigir registros somente por novo evento | Sobrescrita destruiria a trilha auditável | `record.corrected` referencia ID e hash originais |
| DM-030 | Tornar o mapa de projeção normativo | Transformações implícitas gerariam ODS diferentes a partir do mesmo JSONL | Cada campo, operação, derivação e proveniência é declarado em YAML versionado |
| DM-031 | Preservar proveniência por linha projetada | A ODS precisa retornar ao evento fonte | Registros carregam IDs, streams, hashes e versão da projeção |

## Decisões que limitam as alegações do artigo

1. A trilha implementada é experimental, reprodutível e alinhada às atividades da ISO/IEC 27037, mas não cobre, por si só, todos os agentes e atos exigidos por uma cadeia de custódia legal completa.
2. A identidade do ator deve resolver para principal autenticado e fingerprints verificáveis. Isso aumenta responsabilização, mas não autoriza alegar não repúdio absoluto sem proteção das chaves, proibição de contas compartilhadas e assinatura verificável.
3. As referências a objetos DOML-F são validadas contra a versão do modelo registrada no experimento, não tratadas como FKs internas da planilha.
4. A ODS é instrumento de inspeção, análise e intercâmbio. A coleta automática usa JSONL validado como fonte primária e permite exportação posterior para ODS ou banco relacional sem redefinir a semântica.
5. O número final de repetições será determinado após o piloto conforme variabilidade e precisão; o teto operacional deverá ser declarado como limitação se não produzir o IC desejado.

## Referência normativa da DM-011

ISO/IEC 27037:2012 — *Guidelines for identification, collection, acquisition and preservation of digital evidence*. https://www.iso.org/standard/44381.html

## Ponto de controle

Estas decisões devem ser revisadas antes da geração da ODS. Alterações posteriores que afetem PK, FK, granularidade ou cardinalidade exigirão nova versão do documento.
