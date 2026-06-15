# Spec Kit (v2)

Kit de skills para criar uma especificação de produto no modelo wikiLLM (Camada de
Intenção + Camada de Requisitos), independente da fonte.

## O que é

O **spec-kit** é um kit replicável de skills para construir a especificação de um
produto no modelo **wikiLLM** — um wiki de markdown navegável, escrito e mantido por
um agente, com o conhecimento de produto destilado de fontes curadas.

A spec é organizada em duas camadas:

- **Camada de Intenção** — *por que e para quem* o produto existe. Consolidada em **um
  único documento**, `refined/visao.md` (a "Visão", na raiz de `refined/`), com 3
  capítulos: 1. Produto (visão, proposta de valor, personas, jobs), 2. Glossário do
  domínio, 3. Regras & Métricas.
- **Camada de Requisitos** — *o que* o produto faz, feature a feature. Por feature, **um
  único documento**, `refined/Requisitos/<feature>.md`, com 4 capítulos
  (telas/fluxos, histórias, requisitos & cenários de teste, dados); mais o blueprint
  product-level (cadeia de valor) e o **ponteiro fino de componentes**
  (`refined/componentes.md`, na raiz) — um vocabulário genérico de front, não um catálogo
  bespoke.

O resultado é um wiki em `refined/` — markdown com links relativos, IDs estáveis de
cross-reference (`JTBD-NN`, `RN-NN`, …) e dois artefatos HTML navegáveis
(`refined-navigator.html`, `refined/blueprint.html`). Diagramas **Mermaid** embutidos
no markdown são renderizados no navegador.

## Princípio da v2

Padronizar o **mínimo comum**; o resto é opcional por projeto. Menos conceitos, mais
robustos. Agentes mais **especialistas** gerando **menos artefatos**. Linguagem de
produto **agnóstica** mantida.

## Mínimo comum vs. Opcional

A spec mínima de qualquer produto é composta por **três artefatos**:

- **Mínimo comum**
  - `refined/visao.md` — a Visão (na raiz), com os 3 capítulos (Produto, Glossário,
    Regras & Métricas).
  - `refined/Requisitos/<feature>.md` — um doc por feature, com os 4
    capítulos (Telas & Fluxos, Histórias, Requisitos & Cenários de Teste, Dados). As
    histórias **não** levam critérios de aceite — a prova vive nos cenários do Cap. 3.3.
  - `refined/blueprint.md` — blueprint product-level (cadeia de valor).
- **Opcional** (só quando o projeto pedir; não gerado por padrão)
  - Princípios de produto (`PR-NN`).
  - Capacidades de IA como documento dedicado (`CAI-NN`) — o essencial já vira regras
    `RN-AI-NN` na Visão.
  - Roadmap de evolução.
  - Métricas de input/health detalhadas (além do NSM + 1-2 guard-rails).
  - Auditoria extra.

  **Não existem na estrutura FLAT da v2:** pastas `intencao/`, `contracts/`, `entities/`,
  `concepts/`, `analyses/`. A Visão e o catálogo de componentes ficam na raiz de
  `refined/`; os docs de feature ficam em `refined/Requisitos/`.

## Portas de entrada (conversa / docs / pipeline)

O kit aceita três formas de alimentar a spec — e funciona **independente** de existir
ou não um pipeline de dados:

1. **Conversa / brainstorm** — o agente conduz a conversa com o usuário e destila o
   conhecimento direto para os documentos do wiki.
2. **Conjunto de documentos** — um acervo de docs (PDF/DOCX/PPTX/markdown). Fontes
   binárias são convertidas com `markitdown` antes de ler.
3. **Pipeline raw/trusted (opcional)** — quando existe um pipeline de dados, o `raw/`
   é catalogado e destilado em resumos `trusted/` (1 por fonte), e o wiki é gerado a
   partir do `trusted/`.

As skills `intencao-visao` e `contrato-*` consomem qualquer uma dessas portas — ter ou
não um `raw/`/`trusted/` não muda o fluxo.

## Fluxo de uso ponta a ponta

1. **`spec-scaffold`** — cria o wiki novo: a árvore de `refined/` e os arquivos-base
   (`index.md`, `log.md`, `overview.md`, `blueprint.md`, `CLAUDE.md`). Roda uma vez
   por produto.
2. **Camada de Intenção** — rodar a skill **`intencao-visao`** com a fonte disponível
   (conversa, docs ou trusted). Gera/mantém o documento único
   `refined/visao.md` (na raiz) inteiro (3 capítulos).
3. **`spec-audit`** — auditar a Visão pelo método CSD (Certezas, Suposições, Dúvidas);
   resolver as perguntas acionáveis antes de avançar.
4. **Camada de Requisitos** — por feature, definir o `eixo` (`processo` ou `classe`) e
   rodar as skills `contrato-*`: cada uma escreve um **capítulo** do
   `Requisitos/<feature>.md` da feature (telas/fluxos com Mermaid, histórias, requisitos &
   cenários de teste, dados derivados). Rodar também `contrato-blueprint` para o
   blueprint product-level.
5. **`spec-navigator`** — rodar os scripts para gerar `refined-navigator.html` e
   `refined/blueprint.html`. Repetir após qualquer mudança no wiki.
6. **`spec-to-html`** — gerar um protótipo HTML navegável das telas a partir da
   Camada de Requisitos (opcional, depois que ela existe). Roda as 4 sub-skills de
   fase: `plano`, `scaffold`, `telas`, `build`.
7. **Manutenção contínua** — `spec-lint` para o health-check (links quebrados,
   órfãs, lacunas) e `spec-wiki` para integrar fontes novas (`ingest`) ou consultar
   o wiki (`query`).

## Eixo de granularidade do contrato

Cada `Requisitos/<feature>.md` traz no frontmatter `eixo: processo | classe`, que orienta o Cap. 1
(Mermaid) e o Cap. 4 (Dados):

- **`processo`** — fluxo/atividades. A 1.1 funde fluxo e processo num único flowchart
  (estilo BPMN leve), além do Mermaid de navegação entre telas (1.3). Os dados do Cap. 4
  **derivam** das atividades.
- **`classe`** — formulários/objetos. A 1.1 é um flowchart simples do ciclo do
  formulário/registro; cada formulário ≈ uma classe; a classe já é o modelo de dados do
  Cap. 4.

## Mermaid

Blocos ` ```mermaid ` embutidos no markdown são renderizados no navegador:

- Contrato Cap. 1.1 — fluxo (processo, se `eixo=processo`; ciclo do formulário, se
  `eixo=classe`).
- Contrato Cap. 1.3 — navegação entre telas (sempre). **Não** há subseção 1.4 separada.
- Visão Cap. 1 — jornada macro (opcional).

## Wireframe nas telas + vocabulário de componentes

Cada tela `T-NN` (Cap. 1.2 de `Requisitos/<feature>.md`) traz um bloco ` ```wireframe `
(DSL line-based) que esboça o layout, renderizado no navegador como SVG **fat marker,
só-layout** — formas sem texto legível. A linha `Componentes:` de cada tela lista os
componentes pelo **nome genérico** (toolbar, card, table, list, button, input, chart…).

`refined/componentes.md` é um **ponteiro fino** p/ esse vocabulário **genérico de
front-end**, agnóstico de framework (button, slider, input, select, table, list, card,
tabs, dialog, toolbar, chart…); cada projeto mapeia p/ a sua lib concreta (Material
Angular, MUI, shadcn/ui, HTML nativo — só exemplos). Gramática da DSL e mapa
DSL → componente: `docs/CONVENCOES-V2.md`.

## As skills

### Camada de Intenção (1)

| Skill | O que faz |
| --- | --- |
| `intencao-visao` | Produz e mantém o documento único `visao.md` (a Visão, na raiz) — os 3 capítulos: Produto/Personas/Jobs, Glossário do domínio, Regras & Métricas. Especialista; adiciona seções opcionais (princípios, capacidades-IA, roadmap) só quando pedido. |

### Camada de Requisitos (5)

| Skill | O que faz |
| --- | --- |
| `contrato-telas-fluxos` | Escreve o **Cap. 1 (Telas & Fluxos)** do `Requisitos/<feature>.md` da feature, com Mermaid de fluxo (1.1) e de navegação (1.3). |
| `contrato-historias` | Escreve o **Cap. 2 (Histórias)** — `US-NN`. |
| `contrato-requisitos` | Escreve o **Cap. 3 (Requisitos & Cenários de Teste)** — `RF-NN`, `RNF-*` + cenários de teste (Gherkin-like). |
| `contrato-dados` | Escreve o **Cap. 4 (Dados)** — modelo derivado (da classe, se `eixo=classe`; das atividades, se `eixo=processo`). |
| `contrato-blueprint` | Blueprint product-level — features na cadeia de valor (inalterado). |

### Operacionais (5)

| Skill | O que faz |
| --- | --- |
| `spec-scaffold` | Cria a estrutura de um wiki wikiLLM novo. Primeiro passo de uso do kit. |
| `spec-audit` | Auditoria CSD — levanta Certezas, Suposições e Dúvidas como perguntas acionáveis. |
| `spec-lint` | Health-check do wiki — links quebrados, páginas órfãs, lacunas, páginas sem `## Relacionado`. |
| `spec-navigator` | Roda os scripts que (re)geram `refined-navigator.html` e `refined/blueprint.html`. |
| `spec-wiki` | Manutenção contínua — `ingest` (integrar fonte nova) e `query` (consultar o wiki). |

### Geração de protótipo (5)

Família `spec-to-html` — transforma a Camada de Requisitos num protótipo HTML
navegável (sem backend), que abre com duplo-clique como arquivo único.

| Skill | O que faz |
| --- | --- |
| `spec-to-html` | Orquestradora/índice — descreve as 4 fases e os 2 checkpoints. |
| `spec-to-html-plano` | Cria o repo do protótipo e seleciona o conjunto 80/20 de telas. |
| `spec-to-html-scaffold` | Copia o design system EloGroup e escreve o esqueleto invariável. |
| `spec-to-html-telas` | Gera um partial `screens/NN-*.html` por tela da tabela. |
| `spec-to-html-build` | Monta o `index.html` autossuficiente, finaliza o README e verifica. |

## Estrutura do `refined/` gerado

```
refined/
  index.md  log.md  overview.md  blueprint.md   # 4 mds da wiki
  visao.md                         # a Visão — 3 capítulos (mínimo) — na raiz
  componentes.md                   # ponteiro fino: vocabulário genérico de componentes — na raiz
  Requisitos/
    <feature>.md                   # 1 doc por feature — 4 capítulos (mínimo)
  _archive/                        # artefatos obsoletos (opcional)
```

> Estrutura **FLAT**: não há pastas `intencao/`, `contracts/`, `entities/`, `concepts/`
> nem `analyses/`. A Visão e o catálogo de componentes ficam na raiz; os docs de feature
> ficam em `Requisitos/`.

## Scripts

Em `scripts/` — utilitários Python (3.11) que geram os artefatos navegáveis a partir
do `refined/`. `<wiki>` é o diretório que contém `refined/`.

- **`scripts/build-navigator.py <wiki>`** — varre a Camada de Intenção
  (`visao.md`) e a Camada de Requisitos (`Requisitos/<feature>.md`) e
  embute todo o conteúdo num único `refined-navigator.html`, que abre com duplo-clique
  (sem servidor). Diagramas Mermaid embutidos são renderizados. Se existir
  `refined/blueprint.md`, ele é renderizado como uma tela de cadeia de valor dentro do
  navegador. Rodar: `python3 scripts/build-navigator.py <wiki>`. O navegador sai no
  padrão visual EloGroup (azul institucional, fontes Outfit/Roboto Mono e logotipo
  embutidos).

Rodar sempre que os `.md` do `refined/` mudarem — ou usar a skill
`spec-navigator`, que faz isso.
