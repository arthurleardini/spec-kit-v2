---
titulo: Fixture — Modelo de dados canônico
tipo: transversal
---

# Fixture — Modelo de dados canônico

## Entidades

- **Contribuinte** — Pessoa física ou jurídica com obrigação junto ao órgão.
- **Crédito** — Valor devido, com fase e situação.
- **Régua** — Sequência configurada de comunicações.
- **Conector** — Serviço de entrega por canal.
- **Aceite LGPD** — Consentimento vigente por canal e finalidade.

## Relações

```mermaid
erDiagram
    Contribuinte ||--o{ Credito : possui
    Regua ||--o{ Comunicacao : gera
    Conector ||--o{ Comunicacao : entrega
```
