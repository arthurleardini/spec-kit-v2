---
titulo: Cadastro de campanha — Requisitos
tipo: contract
eixo: processo
status: ativo
fontes:
  - fixture negativa do lint crítico
---

# Cadastro de campanha — Requisitos

Fixture negativa: cada bloco abaixo dispara ao menos uma regra do `regras/criticas.toml`.
O mapa de regras esperadas fica em `examples/lint/esperado-ruim.txt` (fora deste arquivo,
para não contaminar as verificações que varrem o texto inteiro).

## 1. Telas & Fluxos

### 1.1 Fluxo (Mermaid)

```mermaid
flowchart LR
    Inicio([Abertura]) --> A[Cadastrar campanha]
    A --> B[Publicar campanha]
    B --> Fim([Encerramento])
```

### 1.2 Telas detalhadas

#### T-01 — Cadastro da campanha
- **Objetivo:** cadastrar a campanha.

- **Conteúdo:** dados da campanha.
- **Ações:** salvar.
- **Componentes:** input, button.

#### T-02 — Lista de campanhas
- **Arquétipo:** A-02
- **Objetivo:** listar campanhas.

- **Conteúdo:** nome e situação.
- **Ações:** abrir.
- **Componentes:** table, button.

---

## 2. Requisitos & Cenários de Teste

### 2.1 Personas & objetivos

| Persona | Objetivo | JTBD |
|---|---|---|
| Gestor | Organizar campanhas | JTBD-01 |

### 2.2 Requisitos Funcionais

| ID | Enunciado | Prioridade | RNs |
|---|---|---|---|
| RF-01 | Permitir cadastrar campanha de forma amigável | Must | RN-01 |
| RF-01 | Cadastrar campanha e publicar campanha, quando aplicável | Must | RN-02 |
| RF-03 | Não usar razão social no canal público | Must | RN-03 |
| RF-04 | O sistema deve suportar o cadastro de campanha de maneira eficiente, otimizada e escalável, contemplando os diversos perfis do órgão, o volume esperado de registros e as regras vigentes de cada unidade | Should | RN-99 |
| RF-05 | A campanha é publicada pelo gestor | Must | RN-06 |
| RF-06 | O sistema deve gerar trilha imutável com carimbo de tempo em toda comunicação | Must | RN-02 |
| RF-07 | O sistema deve exportar a lista de campanhas em planilha | Should | — |

### 2.3 Requisitos Não-Funcionais

#### Performance
- **RNF-P-01** — Latência de abertura da lista abaixo de 2 segundos.

#### Escalabilidade
- **RNF-E-01** — Suporta 200 campanhas ativas por instância.

### 2.4 Cenários de Teste

#### CT-01 — Cadastro da campanha
- **Dado** um gestor autenticado
- **Quando** ele salva a campanha
- **Então** a campanha aparece na lista

#### CT-02 — Trilha de comunicação (verifica RF-06)
- **Dado** uma comunicação registrada
- **Quando** o auditor consulta
- **Então** o sistema gera trilha imutável com carimbo de tempo em toda comunicação

#### CT-03 — Publicação da campanha (verifica RF-05)
- **Dado** uma campanha em rascunho
- **Quando** o gestor publica

---

## 3. Dados

### 3.1 Entidades próprias da feature

#### Crédito
| Campo | Tipo | Descrição |
|---|---|---|
| identificador | texto | Chave do registro |
| situacao |  | Situação atual |

#### campanha_config
| Campo | Tipo | Descrição |
|---|---|---|
| nome | texto | Nome da campanha |

A integração de saída usa o endpoint de publicação do portal.

### 3.2 Relações

- Crédito 1:N campanha_config — vínculo do registro.

---

## Fontes
- fixture negativa do lint crítico

## Relacionado
- [Visão](../visao.md)
- [Catálogo inexistente](../catalogo-que-nao-existe.md)
