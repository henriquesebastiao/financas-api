# Finanças API

Este projeto é uma API RESTful [_self-hosted_](https://dev.to/carrie_luo1/self-hosting-what-why-and-how-14o4) de código aberto para gerenciamento de finanças pessoais.

### Segurança

Tendo em vista o foco em execução _self-host_, a API não possui autenticação,
portanto cabe ao usuário implementar medidas de segurança ao nível de _firewall_, por exemplo.
O sistema também não conta com suporte a multiplos usuários,
ao menos não está no escopo de desenvolvimento até o momento.

### Ferramentas utilizadas

Esta API está sendo desenvolvida utilizando as seguintes ferramentas:

- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL

## Licença

Este projeto está licenciado sob a [Licença PolyForm Noncommercial](LICENSE), o que significa que ele pode ser usado, modificado e distribuído para fins não comerciais, desde que os termos da licença sejam respeitados. Para mais detalhes, consulte o arquivo de licença incluído no projeto.