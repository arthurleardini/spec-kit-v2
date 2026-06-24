# Convenções spec-kit v2 — Rodada 1

Fonte única de verdade para a Rodada 1. Decisões vêm de `../../spec-kit/docs/2026-06-14-backlog-v2.md` (cópia em `docs/` do repo original). Tudo aqui se aplica a `spec-kit-v2/`.

## Princípio geral

Padronizar o **mínimo comum**; o resto é opcional por projeto. Menos conceitos, mais robustos. Agentes mais **especialistas** gerando **menos artefatos**. Linguagem de produto **agnóstica** mantida.

## Mudança 1 — Camada de Intenção vira "Visão" (1 doc, 3 capítulos)

Os 5 documentos viram **um único** `refined/visao.md` (na raiz de `refined/`; H1 + 3 capítulos H2):

- `## 1. Produto` — Visão, Proposta de Valor, Personas, Jobs/Necessidades (`JTBD-NN`), Não-objetivos.
- `## 2. Glossário` — Termos do domínio, Convenções de nomenclatura. (guard-rail de linguagem; mantido inteiro)
- `## 3. Regras & Métricas` — Regras de Negócio (`RN-NN`), Regras dependentes de IA (`RN-AI-NN`, só se houver), Métricas de sucesso (NSM + 1-2 guard-rails, `IM-NN`).

Final do doc: `## Questões em aberto`, `## Fontes`, `## Relacionado`.

**IDs preservados:** `JTBD-NN`, `RN-NN`, `RN-AI-NN`, `IM-NN`.
**Saem do mínimo (viram OPCIONAIS, não gerados por padrão):** Princípios (`PR-NN`), Capacidades de IA como doc dedicado (`CAI-NN` — o essencial vira `RN-AI`), Roadmap de evolução, Input/Health metrics detalhadas.

**Skill:** os 5 `intencao-*` viram **um** `skills/intencao-visao/` — o "agente gerador de visão", especialista, que produz/mantém o `visao.md` inteiro. Pode adicionar seções opcionais **só quando pedido**.

## Mudança 2 — Camada de Requisitos: 1 doc por feature, 3 capítulos, com eixo de granularidade

A antiga "Camada de Contrato" passa a se chamar **Camada de Requisitos**. Por feature, os docs viram **um** `refined/Requisitos/<feature>.md`. Frontmatter inclui `eixo: processo | classe`. Capítulos H2:

- `## 1. Telas & Fluxos` — telas + **diagrama Mermaid** de navegação entre telas. Cada tela declara seu **arquétipo** (`A-NN` de `telas-comuns.md`).
- `## 2. Requisitos & Cenários de Teste` — `2.1 Personas & objetivos` (intenção do usuário), `2.2 RF`, `2.3 RNF`, `2.4 Cenários` (Gherkin-like). Cita os transversais (`RNF-T-*`/`RF-T-*`) por ID.
- `## 3. Dados` — referencia o **modelo de dados transversal** (`modelo-dados.md`) e descreve só o que é próprio da feature; modelo **derivado** do eixo.

> **Histórias morreu (evolução de 5 loops).** Histórias e Requisitos eram redundantes. O
> antigo `## 2. Histórias` (`US-NN`) foi **eliminado**; a intenção do usuário (persona →
> objetivo) foi absorvida pela subseção `2.1 Personas & objetivos` dentro de Requisitos. O
> contrato passa de 4 para **3 capítulos**.

**Eixo:**
- `processo` — fluxo/atividades; o Mermaid do Cap. 1 e/ou um Mermaid de processo (flowchart estilo BPMN leve); dados derivam das atividades.
- `classe` — formulários/objetos; cada formulário ≈ uma classe; a classe já é o modelo de dados.

**Skills:** mantêm-se especialistas, mas **escrevem capítulos** no `Requisitos/<feature>.md` (não arquivos soltos), cientes do `eixo`:
- `contrato-telas-fluxos` → Cap. 1 (com Mermaid + arquétipo por tela).
- `contrato-requisitos` → Cap. 2 (personas & objetivos + RF/RNF + cenários de teste).
- `contrato-dados` → Cap. 3 (derivado, referenciando `modelo-dados.md`).
- `contrato-blueprint` → inalterado (product-level PRD).

## Mudança 2-bis — Pense transversalmente (modelo de dados, requisitos e telas comuns)

A maior lição dos loops de evolução: **não duplicar por feature** o que é comum. Três
documentos transversais vivem na **raiz** de `refined/`, e cada feature **referencia** em
vez de remodelar:

- `modelo-dados.md` — **modelo de dados canônico** (entidades do domínio num só lugar:
  `## Entidades` + `## Relações` + `erDiagram` em Mermaid). O Cap. 3 de cada feature
  referencia essas entidades e descreve só o que é próprio (configs, logs, execução).
- `requisitos-transversais.md` — **requisitos cross-cutting**: `RNF-T-<categoria>-NN` por
  categoria + `RF-T-NN`. O Cap. 2 de cada feature cita os IDs em vez de redefini-los.
- `telas-comuns.md` — **arquétipos de tela** `A-NN` (wireframe + "Quando usar"). Cada tela
  `T-NN` declara seu `**Arquétipo:**` e descreve só o que muda.

**Princípio transversal-first** — modelo de dados, telas e requisitos são pensados
transversalmente (um modelo canônico, um catálogo de arquétipos, um conjunto de
`RNF-T-*`/`RF-T-*`), não por feature. Skill dedicada **`spec-transversais`** gera/mantém os
3 docs varrendo as features (extrai entidades canônicas, requisitos comuns, arquétipos) e
emagrece os docs de feature para apenas referenciá-los. O `spec-scaffold` semeia os 3
esqueletos na raiz, junto de `visao.md`/`componentes.md`.

**Princípio de minimização de telas** — favorecer **menos telas e menos complexidade**:
antes de criar uma tela, reusar um arquétipo de `telas-comuns.md`; preferir **fundir vistas
em abas/drawers/painéis laterais** a multiplicar telas; cada tela é **etiquetada com seu
arquétipo**. Se um padrão de tela aparece em ≥ 2 features, promovê-lo a arquétipo
transversal (não duplicá-lo).

## Mudança 3 — Mermaid (BL-21)

Blocos ` ```mermaid ` embutidos no markdown:
- Contrato Cap. 1 (navegação entre telas) — sempre.
- Contrato `eixo=processo` (fluxo de processo) — quando aplicável.
- Visão Cap. 1 (jornada macro) — opcional.
- Transversal `modelo-dados.md` (`erDiagram` do modelo canônico) — sempre.
O `scripts/build-navigator.py` deve **renderizar Mermaid** no HTML (incluir mermaid.js, inicializar nos blocos ` ```mermaid `).

## Navegador — submenu "Transversais"

O `scripts/build-navigator.py` agrupa `modelo-dados.md`, `requisitos-transversais.md`,
`telas-comuns.md` e `componentes.md` sob um submenu **Transversais** no navegador, separados
da Camada de Intenção (`visao.md`) e da Camada de Requisitos (`Requisitos/<feature>.md`).

## Wireframe nas telas (DSL)

Cada tela `T-NN` (Cap. 1.2 de `Requisitos/<feature>.md`) traz, logo após **Objetivo**, um
bloco ` ```wireframe ` que esboça o layout. O `build-navigator.py` renderiza esse bloco como
um SVG **fat marker, só-layout** (parser próprio + rough.js inline, offline): mostra apenas
as **formas** — sem texto legível. Os rótulos escritos na DSL servem ao autor e à prosa; o
renderer os converte em rabisco de marcador, nunca em texto.

**Gramática** (line-based, de cima p/ baixo num stack vertical; 2 espaços indentam dentro de
um `card`):

| Sintaxe | Nó | Componente genérico |
|---|---|---|
| `# Texto` | barra de título (largura total) | toolbar |
| `## Texto` | subtítulo / cabeçalho de seção | — |
| `[[ a \| b \| c ]]` | linha de N células iguais | grid / card row |
| `card "Título":` + linhas indentadas | card/região com filhos | card |
| `[Rótulo____]` (≥2 underscores finais) | input | input / form-field |
| `[~ legenda ~]` | placeholder de gráfico | chart |
| `[Texto]` (1+ por linha, sem underscores) | botão(ões) | button |
| `(!) texto` | alerta/banner | banner |
| `- item` | item de lista (linhas `-` consecutivas = uma lista) | list |
| `\| a \| b \|` (linhas consecutivas) | tabela; 1ª linha = cabeçalho | table |
| `texto` (livre) | label/parágrafo | — |
| linha em branco | espaçamento vertical | — |

Desambiguação: `[token]` sem `____`/`~` → botão; `[token____]` → input; `[~...~]` → gráfico;
`[[ ... | ... ]]` é a única linha multi-coluna; card só via `card "...":` + indentação
(não há `[box]` genérico, p/ evitar ambiguidade com botão).

### Vocabulário genérico de componentes

`componentes.md` (na raiz de `refined/`) é um **ponteiro fino**: um vocabulário **genérico
de front-end**, agnóstico de framework — os componentes comuns que se repetem (button,
slider, input, select, table, list, card, tabs, dialog, toolbar, chart…). As telas citam o
componente pelo **nome genérico** (campo **Componentes:**, que substitui o antigo `Blocos:`);
cada projeto **mapeia** p/ a sua lib concreta (Material Angular, MUI, shadcn/ui, HTML
nativo — só exemplos; conjunto canônico de referência:
https://material.angular.dev/components/categories). **Não** há catálogo bespoke de blocos.

## Mudança 4 — Mínimo vs Opcional (BL-01)

Marcar explicitamente em README, `spec-scaffold` e `templates/wiki/CLAUDE.md`:
- **Mínimo comum:** `visao.md` (3 caps) + os 3 transversais (`modelo-dados.md`, `requisitos-transversais.md`, `telas-comuns.md`) + `Requisitos/<feature>.md` por feature (3 caps) + `blueprint.md`.
- **Opcional:** princípios, capacidades-IA dedicada, roadmap, input/health metrics, auditoria extra.

## Estrutura final do `refined/` gerado

```
refined/
  index.md  log.md  overview.md  blueprint.md   (4 mds da wiki)
  visao.md                                        (a Visão — Camada de Intenção, na raiz)
  componentes.md                                  (vocabulário genérico de componentes, na raiz)
  modelo-dados.md                                 (transversal: modelo de dados canônico)
  requisitos-transversais.md                      (transversal: RNF-T-* / RF-T-*)
  telas-comuns.md                                 (transversal: arquétipos de tela A-NN)
  Requisitos/
    <feature>.md                                  (1 doc por feature = Camada de Requisitos, 3 caps)
```

## Regra de não-regressão

Não apagar o `spec-kit/` original. Trabalhar só em `spec-kit-v2/`. Preservar conteúdo bom dos templates antigos ao consolidar (copiar as boas instruções, não reinventar).
