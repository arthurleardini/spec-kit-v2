# CLAUDE.md — <produto> (wiki wikiLLM)

O `<produto>` é um **wiki no padrão wikiLLM**: conhecimento de produto destilado de
fontes curadas. O agente escreve e mantém o wiki; o humano cura as fontes e faz
perguntas.

## Três camadas
- **Base** — `trusted/` (resumos, 1 por fonte) + cache de dados (`data/`). Camada
  imutável; o `raw/` original pode ser descartado após a destilação.
- **Wiki** — `refined/`. Markdown gerado/mantido pelo agente.
- **Schema** — este arquivo.

## Layout de refined/ (estrutura FLAT)
- `index.md` — catálogo de tudo, por categoria. Ler PRIMEIRO ao responder uma query.
- `log.md` — histórico append-only (`## [YYYY-MM-DD] <op> | <título>`).
- `overview.md` — porta de entrada.
- `visao.md` — Camada de Intenção, na **raiz**: **um único documento** (a "Visão"), com 3
  capítulos H2: `## 1. Produto` (visão, proposta de valor, personas, jobs `JTBD-NN`,
  não-objetivos), `## 2. Glossário` (termos do domínio +
  convenções de nomenclatura), `## 3. Regras & Métricas` (regras de negócio `RN-NN`,
  regras dependentes de IA `RN-AI-NN` — só se houver — e métricas de sucesso `IM-NN`:
  NSM + 1-2 guard-rails). Fecha com `## Questões em aberto`, `## Fontes`,
  `## Relacionado`.
- `Requisitos/<feature>.md` — Camada de Requisitos: **um único documento por
  feature**, com frontmatter `eixo: processo | classe` e 4 capítulos H2:
  `## 1. Telas & Fluxos` (Mermaid de fluxo na 1.1 + Mermaid de navegação na 1.3; sem
  subseção 1.4 separada; **cada tela `T-NN` traz um bloco ` ```wireframe ` (sketch
  fat-marker do layout) e a linha `Componentes:` com nomes genéricos**), `## 2. Histórias` (`US-NN` — **sem critérios de aceite**, a
  prova vive no Cap. 3.3), `## 3. Requisitos & Cenários de Teste` (`RF-NN`,
  `RNF-*` + cenários Gherkin-like), `## 4. Dados` (modelo **derivado**: da classe se
  `eixo=classe`; das atividades se `eixo=processo`).
- `componentes.md` — **ponteiro fino** (na **raiz**) p/ um vocabulário **genérico de
  front** (button, input, table, card, toolbar, chart…), agnóstico de framework; cada
  projeto mapeia p/ sua lib concreta (Material Angular/MUI/shadcn/HTML — exemplos). **Não**
  é catálogo bespoke de blocos.
- `blueprint.md` — visão geral da solução (cadeia de valor), na **raiz**, artefato
  product-level.
- `_archive/` — artefatos obsoletos *(opcional)*.
- ~~`intencao/`, `contracts/`, `entities/`, `concepts/`, `analyses/`~~ — **não existem**
  na estrutura FLAT da v2 (a Visão e o catálogo de componentes ficam na raiz; os docs de
  feature ficam em `Requisitos/`).

## Mínimo comum vs. opcional
- **Mínimo comum:** `visao.md` (3 caps) + `Requisitos/<feature>.md`
  por feature (4 caps) + `blueprint.md`.
- **Opcional** (só quando o projeto pedir): princípios de produto (`PR-NN`),
  capacidades de IA como doc dedicado (`CAI-NN` — o essencial já vira `RN-AI-NN` na
  Visão), roadmap de evolução, métricas de input/health detalhadas, auditoria extra.
- **Não existem na estrutura FLAT da v2:** pastas `intencao/`, `contracts/`,
  `entities/`, `concepts/`, `analyses/`.

## Eixo do contrato (granularidade)
- `eixo: processo` — fluxo/atividades; a 1.1 funde fluxo e processo num único
  flowchart (estilo BPMN leve); dados do Cap. 4 derivam das atividades.
- `eixo: classe` — formulários/objetos; a 1.1 é um flowchart simples do ciclo do
  formulário/registro; cada formulário ≈ uma classe; a classe já é o modelo de dados
  do Cap. 4.

## Mermaid
Blocos ` ```mermaid ` embutidos no markdown, renderizados no navegador:
- Contrato Cap. 1.1 — fluxo (processo, se `eixo=processo`; ciclo do formulário, se
  `eixo=classe`).
- Contrato Cap. 1.3 — navegação entre telas (sempre). **Não** há subseção 1.4 separada.
- Visão Cap. 1 — jornada macro (opcional).

## Wireframe nas telas
Cada tela `T-NN` (Cap. 1.2) traz um bloco ` ```wireframe ` (DSL line-based) esboçando o
layout, renderizado no navegador como SVG **fat marker, só-layout** (sem texto legível). A
linha `Componentes:` lista os componentes pelo **nome genérico** (toolbar, card, table,
list, button, input, chart…) do vocabulário em `componentes.md`. Gramática da DSL e mapa
DSL → componente: ver `componentes.md` e `docs/CONVENCOES-V2.md`.

## Convenções de página
- Frontmatter YAML: `titulo`, `tipo`, `atualizado_em`, `status`, `fontes` (opcional);
  no contrato, também `eixo: processo | classe`.
- `tipo` ∈ {overview, intencao, contract, persona, feature, concept, analysis, indice,
  blueprint}.
- Links relativos a nível de arquivo. Da raiz de `refined/` para a Visão: `[texto](visao.md)`;
  de um doc em `Requisitos/` para a Visão: `[texto](../visao.md)`.
- Toda página termina com `## Relacionado` (links de saída).
- IDs de cross-reference: `JTBD-NN`, `RN-NN`, `RN-AI-NN`, `IM-NN`, `US-NN`, `RF-NN`,
  `RNF-*` (e os opcionais `PR-NN`, `CAI-NN` quando existirem) — referência textual +
  link para o doc que define o ID. IDs são estáveis: não renumerar.
- Marcadores: `*(inferência)*`; `⚠ NÃO IDENTIFICADO — definir: <pergunta>`;
  `⚠ CONTRADIÇÃO — ver [página](...)`. **Nunca sobrescrever em silêncio** — marcar a
  contradição e preservar as duas versões.

## Workflows

### ingest
Dois caminhos:
- **Lote:** novos docs num `raw/` recriado → pipeline de catálogo/extração/resumo →
  novos `trusted/`.
- **Avulso:** o agente recebe a fonte, converte para Markdown se preciso, discute os
  takeaways, escreve um resumo em `trusted/`.
Depois (comum): o agente lê o(s) `trusted` novo(s), propaga para `visao.md` e os docs em
`Requisitos/`, marca `⚠ CONTRADIÇÃO` em conflitos (nunca sobrescreve em
silêncio), atualiza `index.md`, anexa entrada em `log.md`.

### query
Ler `index.md` → identificar páginas relevantes → ler → responder com citações
(links). O relatório da resposta vai para `log.md` (dispara mini-ingest:
atualiza `index.md`).

### lint
Varrer o wiki: contradições, claims obsoletos, páginas órfãs, links quebrados,
lacunas `⚠`. Relatório vai para `log.md`.

## Navegação
<Comando(s) que regeneram artefatos de navegação a partir do `refined/`, se houver —
ex.: um navigator HTML (que também renderiza o `blueprint.md` como tela de cadeia de
valor). Rodar após qualquer mudança no `refined/`.>
