---
name: spec-scaffold
description: Use quando o usuário quer iniciar uma spec wikiLLM nova — criar a estrutura de diretórios e os arquivos-base de um wiki para um produto. É o primeiro passo de uso do spec-kit.
---

# spec-scaffold

Cria a estrutura **FLAT** de um wiki wikiLLM novo para um produto: os arquivos-base do wiki (incluindo `visao.md` e `componentes.md` na raiz de `refined/`), a pasta `refined/Requisitos/` e o `CLAUDE.md` na raiz, a partir dos templates em `templates/wiki/` do spec-kit.

É o **primeiro passo** de uso do kit — roda uma vez por produto, antes da skill `intencao-visao` ou de qualquer skill `contrato-*`.

## Quando usar
Quando o usuário pede para começar uma spec nova, criar o wiki de um produto, montar o esqueleto/estrutura do wikiLLM, ou inicializar um repositório de spec.

## Entrada
- O diretório onde o wiki será criado (`<wiki>` — a raiz que conterá `refined/` e `CLAUDE.md`).
- O nome do produto.
- Opcionalmente, se há um pipeline `raw/`/`trusted/` ou se a fonte será conversa/docs (não muda a estrutura criada, só informa o `overview.md`).

## Processo
1. Confirmar com o usuário o diretório `<wiki>` e o nome do produto.
2. Criar a estrutura **FLAT** sob `<wiki>/refined/`:
   - `refined/Requisitos/` — pasta (vazia no scaffold) que receberá um `<feature>.md` por feature.
   - `refined/_archive/` *(opcional — artefatos obsoletos)*.
   - **Não** há mais pastas `intencao/` nem `contracts/`. A Visão e o catálogo de
     componentes ficam na **raiz** de `refined/`.
3. Criar os arquivos-base a partir de `templates/wiki/` do spec-kit, substituindo `<produto>` e `<data>`:
   - `refined/index.md` ← `templates/wiki/index.md`
   - `refined/log.md` ← `templates/wiki/log.md`
   - `refined/overview.md` ← `templates/wiki/overview.md`
   - `refined/blueprint.md` ← `templates/contrato/blueprint.md` *(esqueleto; preenchido por `contrato-blueprint`)*
   - `<wiki>/CLAUDE.md` ← `templates/wiki/CLAUDE.md`
4. Semear a Camada de Intenção e o ponteiro de componentes com os **esqueletos**, na
   **raiz** de `refined/` (não preencher o conteúdo — isso é feito pelas skills geradoras):
   - `refined/visao.md` ← `templates/intencao/visao.md` (a Visão — 3 capítulos)
   - `refined/componentes.md` ← `templates/contrato/_componentes.md` (ponteiro fino: vocabulário genérico de componentes)
   - **Não** criar `Requisitos/<feature>.md` no scaffold — cada doc de requisitos é
     criado por feature (de `templates/contrato/contrato.md`) pelas skills `contrato-*`.
5. Anexar a primeira entrada em `refined/log.md` (`## [YYYY-MM-DD] scaffold | wiki criado`).

## Mínimo vs. opcional
- **Mínimo comum gerado pelo fluxo:** `visao.md` (3 caps) + `Requisitos/<feature>.md` por feature (4 caps) + `blueprint.md`.
- **Opcional** (só quando o projeto pedir): `_archive/`, princípios, capacidades-IA como doc dedicado, roadmap, métricas detalhadas.

## Saída
- Estrutura FLAT criada: `refined/` com `index.md`, `log.md`, `overview.md`,
  `blueprint.md`, `visao.md` e `componentes.md` na raiz, mais a pasta `refined/Requisitos/`
  (vazia). Sem pastas `intencao/` ou `contracts/`.
- `refined/index.md`, `refined/log.md`, `refined/overview.md`, `refined/blueprint.md`, `refined/visao.md`, `refined/componentes.md` e `<wiki>/CLAUDE.md` criados a partir dos templates, com o nome do produto e a data preenchidos.
- O wiki pronto para receber a skill `intencao-visao` (e depois as `contrato-*`).
