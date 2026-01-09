# Monitor de Rede - API

API simples de monitoramento de rede feita em Python (FastAPI),
rodando em Docker.

## Funcionalidades
- Health check (`/health`)
- Informações de rede (`/network`)
  - IP
  - Gateway
  - Teste de conectividade (ping)

## Tecnologias
- Python
- FastAPI
- Docker
- Docker Compose
- Linux

## Como rodar
Execute:

```bash
docker compose up --build
```
Endpoints disponíveis:

- http://localhost:8000/health
- http://localhost:8000/network