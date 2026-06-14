# Design — Wireframe "fat marker" nas Telas + vocabulário canônico

**Data:** 2026-06-14
**Status:** aprovado (brainstorm) — pronto para plano de implementação
**Escopo:** spec-kit v2 (método) + knowledge_cob (instância)

## Contexto

Hoje cada tela (`T-NN`, Cap. 1 "Telas & Fluxos" de cada `Requisitos/<feature>.md`) é
descrita só em prosa (Objetivo/Conteúdo/Ações/Estados/Navegação/Blocos). Não há
representação visual do layout. O `componentes.md` é um catálogo **bespoke** de 11
blocos (`dashboard-indicadores`, `lista-com-filtros`, …) que os times mantêm à mão.

Dois problemas:
1. Falta um **fat marker sketch** (wireframe baixa-fidelidade) por tela que comunique
   o layout de relance e convide crítica (referência: https://wiremd.dev).
2. A biblioteca de componentes **não deveria ser bespoke**: a ideia é usar um
   vocabulário de **componentes genéricos de front-end que se repetem** (button,
   slider, input, table, card, tabs, dialog…), agnóstico de framework. Material
   Angular (https://material.angular.dev/components/categories) é só **um exemplo** de
   conjunto canônico desse tipo (MUI, shadcn/ui, etc. são outros). O catálogo existe só
   para dar uma **referência canônica de como descrever telas**, não para inventar
   componentes próprios.

## Objetivos

- Cada tela ganha um wireframe **fat marker** renderizado no navigator, autorado em
  um bloco ` ```wireframe ` no próprio markdown.
- `componentes.md` vira um **ponteiro fino** p/ um vocabulário de componentes genéricos
  de front (button, slider, input, table, card…); telas referenciam o nome genérico.
  Os 11 blocos bespoke são removidos.
- Render **self-contained e offline** no `refined-navigator.html`.

## Não-objetivos

- Não adotar o wiremd como dependência (parser/bundle dele). Implementamos um subset.
- Não gerar código de UI real (Angular). É wireframe de especificação, agnóstico.
- Não substituir a prosa da tela — o sketch **aumenta** a descrição (decisão do dono).

## Decisões (do brainstorm)

| # | Decisão |
|---|---------|
| D1 | `componentes.md` = **ponteiro fino** p/ um vocabulário de componentes genéricos de front (button, slider, input, table, card…), agnóstico de framework (Material Angular/MUI/shadcn = exemplos). Telas citam o nome genérico. Remove os 11 blocos bespoke. |
| D2 | Estilo do sketch = **fat marker** (hand-drawn). |
| D3 | Autoria = bloco ` ```wireframe ` por tela, **DSL ASCII estilo wiremd** (subset próprio). |
| D4 | Render = **parser próprio + rough.js** embutido inline no navigator (offline). |
| D5 | Prosa = **aumentar** (mantém Objetivo/Conteúdo/Ações/Estados/Navegação + sketch). `Blocos:` → `Componentes:` (nomes genéricos). |

## DSL `wireframe` (gramática fechada)

Bloco line-based. Linhas processadas de cima p/ baixo num **stack vertical** de nós.
Indentação de 2 espaços aninha dentro de um `card`.

| Sintaxe | Nó | Componente (genérico) |
|---|---|---|
| `# Texto` | barra de título (largura total) | toolbar |
| `## Texto` | subtítulo / cabeçalho de seção | — |
| `[[ a \| b \| c ]]` | **linha** de N células iguais; cada célula é um token recursivo | grid / card row |
| `card "Título":` + linhas indentadas | **card/região**; conteúdo = linhas filhas | card |
| `[Rótulo____]` (≥2 underscores finais) | **input** | input / form-field |
| `[~ legenda ~]` | **placeholder de gráfico** | chart |
| `[Texto]` (1+ por linha, sem underscores) | **botão(ões)** | button |
| `(!) texto` | **alerta/banner** | banner |
| `- item` | **item de lista** (linhas `-` consecutivas = uma lista) | list |
| `\| a \| b \|` (linhas consecutivas) | **tabela**; 1ª linha = cabeçalho | table |
| `texto` (livre) | **label/parágrafo** | — |
| linha em branco | espaçamento vertical | — |

(Nomes genéricos; cada projeto mapeia p/ sua lib — `button`→`mat-button`/`Button`/`<button>`.)

Regras de desambiguação:
- Uma linha só com `[token]` (um ou mais, sem `____` e sem `~`) → **botões**.
- `[token____]` (termina em underscores) → **input**.
- `[~ ... ~]` → **gráfico**.
- Card só via `card "...":` + indentação (não há `[box]` genérico — evita ambiguidade
  com botão).
- `[[ ... | ... ]]` é a única forma de linha multi-coluna.

Exemplo canônico (T-01 Painel do Modelo):
```wireframe
# Painel do Modelo
[[ v7 | 82% acc | drift OK ]]
[~ tendência de acurácia ~]
(!) 312 créditos sem rating
[Configurar] [Precision/Recall] [Recalcular]
```

## Pipeline de render (navigator)

1. `build-navigator.py` já embute o conteúdo markdown no HTML. No cliente, ao
   renderizar markdown, blocos ` ```wireframe ` **não** vão pro highlighter normal:
   são marcados (`<div class="wireframe-src">` com o texto cru).
2. Um módulo JS (`renderWireframe`) embutido no HTML:
   - **Parser:** lê o texto do bloco → árvore de nós (stack vertical, cards aninhados,
     rows horizontais), conforme a gramática acima.
   - **Layout:** motor simples — largura fixa do canvas (ex. 520px); fluxo vertical;
     `[[..]]` divide a largura em N colunas; cards desenham borda + empilham filhos;
     altura de linha fixa por tipo de nó.
   - **Desenho:** **rough.js** (embutido inline, ~9KB) desenha retângulos/inputs/
     botões com traço hand-drawn (fillStyle hachure, roughness alto = fat marker);
     texto via SVG `<text>` com fonte handwriting (stack: "Comic Sans MS","Segoe Print",
     cursive). Saída = um `<svg>` por wireframe, inserido no lugar do bloco.
3. rough.js é **vendorizado inline** no template do navigator (sem CDN) → funciona
   offline no remoto.

## Estrutura por tela (depois)

```
#### T-01 — Painel do Modelo
- **Objetivo:** ...
```wireframe
# Painel do Modelo
[[ v7 | 82% acc | drift OK ]]
[~ tendência de acurácia ~]
(!) 312 créditos sem rating
[Configurar] [Precision/Recall] [Recalcular]
```
- **Conteúdo:** ...
- **Ações:** ...
- **Estados:** carregando, sucesso, alerta de drift
- **Navegação:** entra do menu; sai p/ T-02, T-05
- **Componentes:** toolbar, card, list, button
```

`Blocos:` (bespoke) é renomeado p/ `Componentes:` listando os componentes genéricos
(button, card, list, toolbar…). Cada projeto mapeia p/ sua lib (Material/MUI/etc.).

## componentes.md (ponteiro fino)

Reescrito para:
- 1 parágrafo: "O vocabulário de componentes é **genérico de front-end** — os
  componentes comuns que se repetem (button, slider, input, select, table, list, card,
  tabs, dialog, toolbar, chart…). Telas referenciam o componente pelo **nome genérico**;
  o sketch usa a DSL `wireframe`. Cada projeto mapeia esse vocabulário p/ a sua lib
  concreta (Material Angular, MUI, shadcn/ui, HTML nativo…). Este arquivo é só a
  **referência canônica de vocabulário** — não um catálogo próprio."
- A lista dos componentes genéricos por categoria (entrada, navegação, layout,
  ações & indicadores, popups & modais, dados/tabela) + o mapa DSL→componente (tabela
  acima) + link p/ um exemplo de conjunto canônico
  (https://material.angular.dev/components/categories).
- Remove os 11 blocos bespoke.

## Arquivos a mudar

**spec-kit v2 (método):**
- `templates/contrato/contrato.md` — Cap. 1.2: adicionar bloco ` ```wireframe ` por
  tela; `Blocos:` → `Componentes:` (nomes genéricos).
- `templates/contrato/_componentes.md` — reescrever como ponteiro fino (vira
  `componentes.md` no output).
- `skills/contrato-telas-fluxos/SKILL.md` — instruir geração do bloco `wireframe`
  (DSL), o `Componentes:` genérico, e a referência ao vocabulário canônico.
- `scripts/build-navigator.py` + template HTML — parser + rough.js inline + CSS do
  sketch; tratar ` ```wireframe ` como SVG renderizado.
- `docs/CONVENCOES-V2.md` — documentar a DSL e o vocabulário canônico.
- `templates/wiki/CLAUDE.md`, `README.md` — mencionar wireframe + Material.

**knowledge_cob (instância):**
- `refined/componentes.md` — reescrever como ponteiro fino (remove 11 blocos).
- `refined/Requisitos/<feature>.md` (14) — adicionar bloco `wireframe` por tela `T-NN`;
  `Blocos:` → `Componentes:` (nomes genéricos).
- `build-navigator.py` — propagar o render; regenerar `refined-navigator.html`.

## Rollout

1. Método no spec-kit-v2 (template, skill, navigator, componentes, CONVENCOES).
2. Validar com 1 feature do knowledge_cob (ex. rating-classificacao) → abrir navigator.
3. Propagar às 14 telas; regenerar navigator.

## Verificação

- Smoke-test: navigator gera HTML; blocos `wireframe` viram `<svg>` (não code block cru).
- rough.js inline (sem requisição externa) → abrir offline e ver o sketch.
- Cada tela `T-NN` tem 1 bloco `wireframe` e linha `Componentes:` com nomes genéricos.
- `componentes.md` sem os 11 blocos bespoke; aponta p/ Material.

## Questões em aberto

Nenhuma. Gramática da DSL e pipeline fechados acima.
