---
name: spec-scaffold
description: Use quando o usuário quer iniciar uma spec wikiLLM nova — criar a estrutura de diretórios e os arquivos-base de um wiki para um produto. É o primeiro passo de uso do spec-kit.
---

# spec-scaffold

Cria a estrutura de um wiki wikiLLM novo para um produto: a árvore de diretórios de `refined/`, os arquivos-base do wiki e o `CLAUDE.md` na raiz, a partir dos templates em `templates/wiki/` do spec-kit.

É o **primeiro passo** de uso do kit — roda uma vez por produto, antes da skill `intencao-visao` ou de qualquer skill `contrato-*`.

## Quando usar
Quando o usuário pede para começar uma spec nova, criar o wiki de um produto, montar o esqueleto/estrutura do wikiLLM, ou inicializar um repositório de spec.

## Entrada
- O diretório onde o wiki será criado (`<wiki>` — a raiz que conterá `refined/` e `CLAUDE.md`).
- O nome do produto.
- Opcionalmente, se há um pipeline `raw/`/`trusted/` ou se a fonte será conversa/docs (não muda a estrutura criada, só informa o `overview.md`).

## Processo
1. Confirmar com o usuário o diretório `<wiki>` e o nome do produto.
2. Criar a árvore de diretórios sob `<wiki>/refined/`:
   - `refined/intencao/`
   - `refined/contracts/`
   - `refined/entities/personas/` *(opcional)*
   - `refined/entities/features/` *(opcional)*
   - `refined/concepts/` *(opcional)*
   - `refined/analyses/` *(opcional)*
   - `refined/_archive/`
3. Criar os arquivos-base a partir de `templates/wiki/` do spec-kit, substituindo `<produto>` e `<data>`:
   - `refined/index.md` ← `templates/wiki/index.md`
   - `refined/log.md` ← `templates/wiki/log.md`
   - `refined/overview.md` ← `templates/wiki/overview.md`
   - `refined/blueprint.md` ← `templates/contrato/blueprint.md` *(esqueleto; preenchido por `contrato-blueprint`)*
   - `<wiki>/CLAUDE.md` ← `templates/wiki/CLAUDE.md`
4. Semear a Camada de Intenção e a Camada de Contrato com os **esqueletos** dos
   documentos únicos (não preencher o conteúdo — isso é feito pelas skills geradoras):
   - `refined/intencao/visao.md` ← `templates/intencao/visao.md` (a Visão — 3 capítulos)
   - `refined/contracts/_componentes.md` ← `templates/contrato/_componentes.md` (catálogo de componentes)
   - **Não** criar `contracts/<feature>/contrato.md` no scaffold — cada contrato é
     criado por feature (de `templates/contrato/contrato.md`) pelas skills `contrato-*`.
5. Anexar a primeira entrada em `refined/log.md` (`## [YYYY-MM-DD] scaffold | wiki criado`).

## Mínimo vs. opcional
- **Mínimo comum gerado pelo fluxo:** `intencao/visao.md` (3 caps) + `contracts/<feature>/contrato.md` por feature (4 caps) + `blueprint.md`.
- **Opcional** (só quando o projeto pedir): `entities/`, `concepts/`, `analyses/`, princípios, capacidades-IA como doc dedicado, roadmap, métricas detalhadas.

## Saída
- Árvore `refined/{intencao,contracts,entities/personas,entities/features,concepts,analyses,_archive}/` criada (as opcionais podem ficar vazias).
- `refined/index.md`, `refined/log.md`, `refined/overview.md`, `refined/blueprint.md`, `refined/intencao/visao.md`, `refined/contracts/_componentes.md` e `<wiki>/CLAUDE.md` criados a partir dos templates, com o nome do produto e a data preenchidos.
- O wiki pronto para receber a skill `intencao-visao` (e depois as `contrato-*`).
