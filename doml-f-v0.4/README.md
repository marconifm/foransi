# DOML-F Validator v0.1

Validador em desenvolvimento para o contrato de eventos DOML-F.

## Estado atual

Implementado e testável sem dependências externas:

- parser JSONL estrito;
- rejeição de chaves duplicadas e inteiros inseguros;
- cadeias, sequências e identidade dos streams;
- causalidade básica;
- duração monotônica de etapas;
- referências e ordem do ledger;
- referências de correção;
- resumo de streams e hash terminal do ledger no manifesto;
- relatório JSON e códigos de erro.

Implementado, mas dependente dos pacotes declarados no `pyproject.toml`:

- JSON Schema Draft 2020-12;
- canonicalização JCS/RFC 8785;
- recálculo SHA-256.

Ainda pendente:

- assinatura criptográfica real do manifesto;
- resolução de atores contra Kerberos/OpenLDAP;
- resolução das referências DOML-F;
- motor completo do mapa de projeção;
- exportação ODS/SQL;
- quarentena persistente.

## Execução estrutural

```bash
PYTHONPATH=. python3 -m domlf_validator \
  ../contrato-eventos-v0.1/exemplo-execucao-v0.1.jsonl \
  --schema ../contrato-eventos-v0.1/doml-f-event.schema.json \
  --skip-crypto
```

O exemplo usa hashes didáticos. Por isso o teste estrutural usa `--skip-crypto`.

## Testes

```bash
PYTHONPATH=. python3 -m unittest discover -s tests -v
```

## Princípio de segurança

O validador nunca corrige nem sobrescreve eventos. Ele apenas relata inconsistências e, futuramente, encaminhará eventos rejeitados à quarentena.

