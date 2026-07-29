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
  único documento**, `refined/Requisitos/<feature>.md`, com **3 capítulos**
  (1. Telas & Fluxos, 2. Requisitos & Cenários de Teste — que absorve as personas &
  objetivos, antes "Histórias", 3. Dados); mais o blueprint product-level (cadeia de valor)
  e o **ponteiro fino de componentes** (`refined/componentes.md`, na raiz).
- **Transversais** — o que é comum a várias features vive **uma vez**, na raiz de
  `refined/`, e cada feature **referencia**: `modelo-dados.md` (modelo de dados canônico),
  `requisitos-transversais.md` (`RNF-T-*`/`RF-T-*`) e `telas-comuns.md` (arquétipos de tela
  `A-NN`). **Pense transversalmente, não por feature.**

O resultado é um wiki em `refined/` — markdown com links relativos, IDs estáveis de
cross-reference (`JTBD-NN`, `RN-NN`, …) e dois artefatos HTML navegáveis
(`refined-navigator.html`, `refined/blueprint.html`). Diagramas **Mermaid** embutidos
no markdown são renderizados no navegador.

## Princípio da v2

Padronizar o **mínimo comum**; o resto é opcional por projeto. Menos conceitos, mais
robustos. Agentes mais **especialistas** gerando **menos artefatos**. Linguagem de
produto **agnóstica** mantida.

**Transversal-first** — modelo de dados, telas e requisitos são pensados
**transversalmente** (um modelo de dados canônico, um catálogo de arquétipos de tela, um
conjunto de `RNF-T-*`/`RF-T-*`), **não duplicados por feature**. Cada feature referencia
esses transversais e descreve só o que é específico.

**Minimizar telas** — favorecer **menos telas e menos complexidade**: reusar os arquétipos
de `telas-comuns.md` e **fundir vistas em abas/drawers/painéis laterais** em vez de
multiplicar telas; cada tela é etiquetada com seu arquétipo.

## Mínimo comum vs. Opcional

A spec mínima de qualquer produto é composta por **três artefatos**:

- **Mínimo comum**
  - `refined/visao.md` — a Visão (na raiz), com os 3 capítulos (Produto, Glossário,
    Regras & Métricas).
  - Os **3 transversais** (na raiz): `modelo-dados.md` (modelo de dados canônico),
    `requisitos-transversais.md` (`RNF-T-*`/`RF-T-*`) e `telas-comuns.md` (arquétipos `A-NN`).
  - `refined/Requisitos/<feature>.md` — um doc por feature, com os **3 capítulos**
    (1. Telas & Fluxos, 2. Requisitos & Cenários de Teste, 3. Dados). A intenção do usuário
    (persona → objetivo) vive na §2.1; **não há mais capítulo de Histórias**.
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
   `Requisitos/<feature>.md` da feature (telas/fluxos com Mermaid + arquétipo por tela;
   requisitos & cenários de teste com personas & objetivos; dados derivados que referenciam
   o modelo transversal). Rodar também `contrato-blueprint` para o blueprint product-level.
   - **`spec-transversais`** — gerar/manter os 3 docs transversais (`modelo-dados.md`,
     `requisitos-transversais.md`, `telas-comuns.md`) varrendo as features (extrai entidades
     canônicas, requisitos comuns e arquétipos de tela) e **emagrecer** os docs de feature
     para apenas referenciá-los. Rodar à medida que as features surgem.
5. **`spec-navigator`** — rodar os scripts para gerar `refined-navigator.html` e
   `refined/blueprint.html`. Repetir após qualquer mudança no wiki.
6. **`spec-to-html`** — gerar um protótipo HTML navegável das telas a partir da
   Camada de Requisitos (opcional, depois que ela existe). Roda as 4 sub-skills de
   fase: `plano`, `scaffold`, `telas`, `build`.
7. **Manutenção contínua** — `spec-lint` para o health-check (links quebrados,
   órfãs, lacunas) e `spec-wiki` para integrar fontes novas (`ingest`) ou consultar
   o wiki (`query`).

## Loop crítico (gate da Camada de Requisitos)

Antes de entregar uma feature, roda o **loop crítico**: `scripts/lint_critico.py`
(determinístico, com exit code) + **6 agentes críticos especialistas**, orquestrados pela
skill `spec-critico`. Regras num arquivo só — `regras/criticas.toml`; achados num ledger
auditável — `criticas/<feature>-<data>.md`.

O que ele passou a cobrar em requisito funcional: **EARS-PT** (6 padrões), uma capacidade
por RF, vocabulário fechado (sem palavra subjetiva/brecha/verbo oco), desvio declarado
como RF padrão #5, cenário como *key example* que prova o RF, RNF **só** no transversal
citado por ID, e tetos duros de tamanho.

Metodologia e comandos: **[`docs/LOOP-CRITICO.md`](docs/LOOP-CRITICO.md)**.
Referências que originam cada regra: **[`docs/referencias-v3.md`](docs/referencias-v3.md)**.

## Eixo de granularidade do contrato

Cada `Requisitos/<feature>.md` traz no frontmatter `eixo: processo | classe`, que orienta o Cap. 1
(Mermaid) e o Cap. 3 (Dados):

- **`processo`** — fluxo/atividades. A 1.1 funde fluxo e processo num único flowchart
  (estilo BPMN leve), além do Mermaid de navegação entre telas (1.3). Os dados do Cap. 3
  **derivam** das atividades (referenciando o `modelo-dados.md` transversal).
- **`classe`** — formulários/objetos. A 1.1 é um flowchart simples do ciclo do
  formulário/registro; cada formulário ≈ uma classe; a classe já é o modelo de dados do
  Cap. 3.

## Mermaid

Blocos ` ```mermaid ` embutidos no markdown são renderizados no navegador:

- Contrato Cap. 1.1 — fluxo (processo, se `eixo=processo`; ciclo do formulário, se
  `eixo=classe`).
- Contrato Cap. 1.3 — navegação entre telas (sempre). **Não** há subseção 1.4 separada.
- Transversal `modelo-dados.md` — `erDiagram` do modelo de dados canônico (sempre).
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

### Camada de Requisitos (4)

| Skill | O que faz |
| --- | --- |
| `contrato-telas-fluxos` | Escreve o **Cap. 1 (Telas & Fluxos)** do `Requisitos/<feature>.md` da feature, com Mermaid de fluxo (1.1) e de navegação (1.3); etiqueta cada tela com seu arquétipo (`A-NN` de `telas-comuns.md`) e minimiza telas (reusa arquétipos, funde vistas em abas/drawers). |
| `contrato-requisitos` | Escreve o **Cap. 2 (Requisitos & Cenários de Teste)** — `2.1 Personas & objetivos` (a intenção do usuário, antes "Histórias"), `RF-NN`, `RNF-*` (incl. a **linha de referência ao catálogo de Integrações** transversal — não a tabela) + cenários de teste (Gherkin-like). Cita os transversais (`RNF-T-*`/`RF-T-*`) por ID. |
| `contrato-dados` | Escreve o **Cap. 3 (Dados)** — referencia o `modelo-dados.md` transversal e descreve só o que é próprio; modelo derivado (da classe, se `eixo=classe`; das atividades, se `eixo=processo`). |
| `contrato-blueprint` | Blueprint product-level — features na cadeia de valor (inalterado). |


### Operacionais (6)

| Skill | O que faz |
| --- | --- |
| `spec-scaffold` | Cria a estrutura de um wiki wikiLLM novo (incl. os 3 transversais na raiz). Primeiro passo de uso do kit. |
| `spec-transversais` | Gera/mantém os 3 docs transversais (`modelo-dados.md`, `requisitos-transversais.md` — incl. o **catálogo de Integrações** matriz sistema×feature, `telas-comuns.md`) varrendo as features, e emagrece os docs de feature para apenas referenciá-los. |
| `spec-audit` | Auditoria CSD — levanta Certezas, Suposições e Dúvidas como perguntas acionáveis. |
| `spec-lint` | Health-check do wiki — links quebrados, páginas órfãs, lacunas, páginas sem `## Relacionado`, catálogo de **Integrações** (seção `## Integrações` no transversal) + linha de referência por feature (Cap. 2.3) e convenção de **fora de escopo** (arquivados com `status: fora-escopo` + banner; `index.md` com a seção de arquivados). |
| `spec-navigator` | Roda os scripts que (re)geram `refined-navigator.html` e `refined/blueprint.html`. |
| `spec-wiki` | Manutenção contínua — `ingest` (integrar fonte nova) e `query` (consultar o wiki). |

### Loop crítico (7)

Gate da Camada de Requisitos. Um crítico por hard skill de levantamento; nenhum deles
edita o artefato — acham e assinam, a correção é do autor. Ver
[`docs/LOOP-CRITICO.md`](docs/LOOP-CRITICO.md).

| Skill | O que faz |
| --- | --- |
| `spec-critico` | Orquestra o loop: lint → críticos em paralelo → ledger → correção → re-lint, com número fixo de rodadas e critério de saída declarado. |
| `critico-redacao` | Forma EARS-PT, ambiguidade, vocabulário proibido, singularidade, brevidade. |
| `critico-testabilidade` | RF↔cenário, *key example*, fronteira da regra, resultado observável. |
| `critico-simplicidade` | Corta tela, RF, conceito e escopo; pega RF que descreve implementação. |
| `critico-fluxos` | Desvio e exceção não modelados, contradição fluxo↔RF, estado inalcançável. |
| `critico-dados` | Entidade que deveria ser canônica, fonte da verdade por campo, modelo que não sustenta os RF. |
| `critico-rastreabilidade` | ID e link, rastreio falso (RN que não justifica o RF), fato duplicado, RNF fora do transversal. |

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
  modelo-dados.md                  # transversal: modelo de dados canônico — na raiz
  requisitos-transversais.md       # transversal: RNF-T-* / RF-T-* — na raiz
  telas-comuns.md                  # transversal: arquétipos de tela A-NN — na raiz
  Requisitos/
    <feature>.md                   # 1 doc por feature — 3 capítulos (mínimo)
  _archive/                        # artefatos obsoletos + features fora de escopo (opcional)
    <feature>.md                   # status: fora-escopo + banner FORA DE ESCOPO
```

### Convenção de fora-de-escopo (feature não priorizada)

Feature não priorizada **não é apagada** — é arquivada com o conhecimento preservado:
mover `Requisitos/<feature>.md` → `_archive/<feature>.md`, manter o frontmatter na 1ª
linha com `status: fora-escopo`, adicionar logo após ele um banner
`> **FORA DE ESCOPO** — <motivo, citando a fonte de priorização>. Arquivada em <data>; …`,
e listá-la no `index.md` sob `## Fora de escopo (arquivado — não priorizado)`. Os
cross-links se ajustam pela profundidade (`../_archive/x.md` ↔ `../Requisitos/x.md`;
transversais inalterados). O `build-navigator.py` só varre `Requisitos/*.md`, então a
arquivada some do navegador automaticamente. `spec-lint` verifica essa convenção.

> Estrutura **FLAT**: não há pastas `intencao/`, `contracts/`, `entities/`, `concepts/`
> nem `analyses/`. A Visão e o catálogo de componentes ficam na raiz; os docs de feature
> ficam em `Requisitos/`.

## Scripts

Em `scripts/` — utilitários Python (3.11) que geram os artefatos navegáveis a partir
do `refined/`. `<wiki>` é o diretório que contém `refined/`.

- **`scripts/build-navigator.py <wiki>`** — varre a Camada de Intenção
  (`visao.md`), os **transversais** (`modelo-dados.md`, `requisitos-transversais.md`,
  `telas-comuns.md`, `componentes.md` — agrupados sob o submenu **Transversais**) e a Camada
  de Requisitos (`Requisitos/<feature>.md`) e embute todo o conteúdo num único
  `refined-navigator.html`, que abre com duplo-clique (sem servidor). Diagramas Mermaid
  embutidos são renderizados. Se existir `refined/blueprint.md`, ele é renderizado como uma
  tela de cadeia de valor dentro do navegador. Rodar: `python3 scripts/build-navigator.py <wiki>`. O navegador sai no
  padrão visual EloGroup (azul institucional, fontes Outfit/Roboto Mono e logotipo
  embutidos).

Rodar sempre que os `.md` do `refined/` mudarem — ou usar a skill
`spec-navigator`, que faz isso.

- **`scripts/lint_critico.py <refined>`** — lint crítico determinístico (gate do loop).
  28 regras lidas de `regras/criticas.toml`: forma EARS-PT do RF, vocabulário proibido,
  singularidade, RF↔cenário, cobertura de desvio, tetos de tamanho, RNF local, ID/link e
  capítulo de Dados. Flags: `--json`, `--ledger <dir>`, `--so-bloqueia`, `--regras <toml>`.
  Exit `0` limpo · `1` só «corrige» · `2` há «bloqueia».
- **`scripts/testa_lint.py`** — regressão do lint contra as fixtures de `examples/lint/`
  (`feature-boa.md` sai limpa; `feature-ruim.md` dispara as 27 regras esperadas).

## Documentos de referência

Em `docs/` — material de apoio reutilizável.

- **`docs/CONVENCOES-V2.md`** — convenções da v2 (camadas, eixo, transversais, DSL de wireframe).
- **`docs/LOOP-CRITICO.md`** — metodologia do loop crítico: duas camadas, os 6 críticos,
  ciclo, severidade, formato de achado e ledger, o que ficou fora da rodada.
- **`docs/referencias-v3.md`** — dossiê de referências externas (ISO/IEC/IEEE 29148, EARS,
  Wiegers, requirements smells, Specification by Example, *Insanely Simple*, Maeda,
  Shape Up, Google Technical Writing, Amazon PR/FAQ, GitHub Spec Kit) com a regra do kit
  derivada de cada bloco.
- **`docs/backlog-ajustes-metodologia.md`** — os 7 ajustes metodológicos (M1–M7) achados
  na análise transversal do Knowledge-MT. M1–M5 viraram regra do loop crítico.
- **`docs/checklist-levantamento-negocial.md`** — checklist de validação de uma spec de
  **demanda negocial** (contexto/regras/fluxos sem solução técnica). Usado para auditar
  contratos (`spec-audit`). O item *Integrações e sistemas envolvidos* é a origem
  conceitual do **catálogo de Integrações** (seção `## Integrações`) do
  `requisitos-transversais.md` — referenciado por cada feature numa linha na Cap. 2.3.
