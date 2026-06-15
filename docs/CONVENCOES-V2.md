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

## Mudança 2 — Camada de Requisitos: 1 doc por feature, com eixo de granularidade

A antiga "Camada de Contrato" passa a se chamar **Camada de Requisitos**. Por feature, os 4 docs viram **um** `refined/Requisitos/<feature>.md`. Frontmatter inclui `eixo: processo | classe`. Capítulos H2:

- `## 1. Telas & Fluxos` — telas + **diagrama Mermaid** de navegação entre telas.
- `## 2. Histórias` — `US-NN`.
- `## 3. Requisitos & Cenários de Teste` — `RF-NN`, `RNF-*` + cenários de teste (Gherkin-like).
- `## 4. Dados` — modelo **derivado** (não paralelo): se `eixo=classe`, a própria classe é o modelo; se `eixo=processo`, deriva das atividades.

**Eixo:**
- `processo` — fluxo/atividades; o Mermaid do Cap. 1 e/ou um Mermaid de processo (flowchart estilo BPMN leve); dados derivam das atividades.
- `classe` — formulários/objetos; cada formulário ≈ uma classe; a classe já é o modelo de dados.

**Skills:** mantêm-se especialistas, mas **escrevem capítulos** no `Requisitos/<feature>.md` (não arquivos soltos), cientes do `eixo`:
- `contrato-telas-fluxos` → Cap. 1 (com Mermaid).
- `contrato-historias` → Cap. 2.
- `contrato-requisitos` → Cap. 3 (agora inclui cenários de teste).
- `contrato-dados` → Cap. 4 (derivado).
- `contrato-blueprint` → inalterado (product-level PRD).

## Mudança 3 — Mermaid (BL-21)

Blocos ` ```mermaid ` embutidos no markdown:
- Contrato Cap. 1 (navegação entre telas) — sempre.
- Contrato `eixo=processo` (fluxo de processo) — quando aplicável.
- Visão Cap. 1 (jornada macro) — opcional.
O `scripts/build-navigator.py` deve **renderizar Mermaid** no HTML (incluir mermaid.js, inicializar nos blocos ` ```mermaid `).

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
- **Mínimo comum:** `visao.md` (3 caps) + `Requisitos/<feature>.md` por feature (4 caps) + `blueprint.md`.
- **Opcional:** princípios, capacidades-IA dedicada, roadmap, input/health metrics, auditoria extra.

## Estrutura final do `refined/` gerado

```
refined/
  index.md  log.md  overview.md  blueprint.md   (4 mds da wiki)
  visao.md                                        (a Visão — Camada de Intenção, na raiz)
  componentes.md                                  (catálogo de componentes de UI, na raiz)
  Requisitos/
    <feature>.md                                  (1 doc por feature = Camada de Requisitos)
```

## Regra de não-regressão

Não apagar o `spec-kit/` original. Trabalhar só em `spec-kit-v2/`. Preservar conteúdo bom dos templates antigos ao consolidar (copiar as boas instruções, não reinventar).
