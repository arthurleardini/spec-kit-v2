---
name: contrato-telas-fluxos
description: Use quando o usuário quer gerar ou revisar as Telas e Fluxos (Cap. 1) do doc de Requisitos de uma feature no modelo wikiLLM — inclui o diagrama Mermaid de navegação.
---

# contrato-telas-fluxos

Escreve e mantém o **Capítulo 1 — Telas & Fluxos** do documento único `refined/Requisitos/<feature>.md` da Camada de Requisitos. Não cria arquivo solto: o doc de requisitos de cada feature é **um só** (3 capítulos — Telas & Fluxos, Requisitos & Cenários, Dados); esta skill é dona do Cap. 1.

Responde à pergunta-mãe *Como o usuário interage com a feature?* — descreve o fluxo da feature em termos de informação e ações (agnóstico de UI), detalha cada tela (com **wireframe fat-marker** na DSL `wireframe`) e **emite um diagrama Mermaid de navegação** (BL-21). Também mantém o ponteiro fino de vocabulário de componentes em `componentes.md`.

## Princípio: minimizar telas
O objetivo é o **menor número de telas e a menor complexidade**. Pense telas
**transversalmente**, não por feature:
- **Reutilize arquétipos.** Antes de criar uma tela, verifique se um **arquétipo** de
  `refined/telas-comuns.md` (`A-NN`) já a resolve. Cada tela `T-NN` deve declarar
  `**Arquétipo:** A-NN` (ou `—` se for genuinamente específica) e descrever **só o que muda**
  (colunas, filtros, ações, estados), em vez de re-desenhar o wireframe do zero.
- **Funda em vez de multiplicar.** Prefira **abas, drawers e painéis laterais** a telas
  separadas (ex.: um detalhe que absorve o histórico como aba; um painel com tabs por
  status). Reaproveitar 1 editor/canvas parametrizável vale mais que vários.
- **Promova ao transversal.** Se o mesmo padrão de tela aparece em ≥ 2 features, ele deve
  virar um arquétipo em `telas-comuns.md` (skill `spec-transversais`), não nascer duplicado.

**Regra de não-sobreposição** (ver bloco-intro do `Requisitos/<feature>.md`): cada fato mora em UM lugar. Telas/fluxo são deste capítulo; não repetir aqui persona & objetivo (Cap. 2.1), o que o sistema deve fazer (Cap. 2.2 RF) nem critérios de prova (Cap. 2.4 Cenários). O contrato tem **3 capítulos** (Telas & Fluxos, Requisitos & Cenários, Dados) — não há mais capítulo de Histórias.

## Quando usar
Quando o usuário pede para criar, escrever ou revisar as telas e os fluxos de uma feature — ou pede para descrever a jornada de interação, as telas, os estados de tela, a navegação ou o diagrama de fluxo do produto.

## Eixo (`processo` | `classe`)
Ler `eixo` no frontmatter do `Requisitos/<feature>.md` (defini-lo se ainda não existir, perguntando ao usuário ou inferindo: feature de fluxo/atividades → `processo`; feature de formulários/objetos → `classe`). O Cap. 1 sempre tem **dois** Mermaid: o de **fluxo** (1.1) e o de **navegação entre telas** (1.3). Não há mais subseção 1.4 separada.
- **`eixo=processo`** — a **1.1** funde fluxo e processo num único flowchart (estilo BPMN leve: atividades/informações como nós, gateways `{ }`, do gatilho às saídas).
- **`eixo=classe`** — a **1.1** é um flowchart simples do ciclo do formulário/registro (criar → validar → salvar → editar).

## Entrada
A Camada de Intenção consolidada em `refined/visao.md` (produto, personas, jobs, regras), o catálogo de arquétipos `refined/telas-comuns.md` (para reusar `A-NN`), o ponteiro `refined/componentes.md` e a fonte da feature: qualquer conversa/brainstorm ou documento associado à feature. Se a fonte for documento binário (PDF/DOCX/PPTX), converter com `markitdown` antes de ler.

## Processo
1. Ler `refined/visao.md`, `refined/telas-comuns.md` e a fonte da feature. Determinar/confirmar o `eixo`.
2. Abrir (ou criar a partir de `templates/contrato/contrato.md`) o `refined/Requisitos/<feature>.md` e preencher o **Cap. 1 — Telas & Fluxos**, sem tocar nos Caps. 2–4:
   - **1.1 Fluxo (Mermaid):** um flowchart Mermaid (não prosa em bullets). Nós = `<informação> → <ação> → <resultado>`; `{ }` = decisões; `([ ])` = gatilho/saídas; mais **uma** linha de legenda. Se `eixo=processo`, este flowchart funde fluxo e processo (BPMN leve, gatilho → atividades → saídas); se `eixo=classe`, é o ciclo simples do formulário/registro.
   - **1.2 Telas detalhadas:** uma subseção por tela, com objetivo, conteúdo, ações, estados, navegação. **Para cada tela `T-NN`:** começar pela linha **Arquétipo:** declarando o `A-NN` de `telas-comuns.md` que a tela segue (ou `—` se específica); descrever só o que muda em relação ao arquétipo. Logo após **Objetivo**, gerar um bloco ` ```wireframe ` (DSL abaixo) representando o layout, e a linha **Componentes:** listando nomes genéricos (toolbar, card, table, list, button, input, chart…). **Antes de criar uma tela nova**, checar se um arquétipo existente resolve, e preferir fundir vistas (abas/drawers) a multiplicar telas.
   - **1.3 Diagrama de navegação (Mermaid):** **obrigatório**. Bloco ` ```mermaid ` com `flowchart`; cada nó é uma tela (usar o `<id da tela>` do 1.2), cada aresta é uma transição rotulada com a ação que a dispara.
3. Manter o ponteiro fino `refined/componentes.md` (template `templates/contrato/_componentes.md`): é um **vocabulário genérico de front** (button, input, table, card, toolbar, chart…), agnóstico de framework — **não** um catálogo bespoke de blocos. Fica na **raiz** de `refined/`. As telas do 1.2 referenciam os componentes pelo **nome genérico** (campo **Componentes:**).
4. Marcar inferências com `*(inferência)*` e lacunas com `⚠ NÃO IDENTIFICADO — definir: <pergunta>`.
5. Salvar o `Requisitos/<feature>.md`. Atualizar `refined/index.md` (linha da feature) e anexar entrada em `refined/log.md`.

## DSL `wireframe` (por tela)
Bloco ` ```wireframe ` line-based, processado de cima p/ baixo num stack vertical;
2 espaços de indentação aninham dentro de um `card`. O autor escreve rótulos normalmente
(servem à prosa), mas o render do navegador é **fat marker, só-layout** — mostra apenas as
formas (sem texto legível); a **forma** indica o tipo de componente.

| Sintaxe | Nó |
|---|---|
| `# Texto` | barra de título (toolbar) |
| `## Texto` | subtítulo |
| `[[ a \| b \| c ]]` | linha de N colunas iguais |
| `card "Título":` + linhas indentadas (2 espaços) | card/região com filhos |
| `[Rótulo____]` (≥2 underscores finais) | input |
| `[~ legenda ~]` | placeholder de gráfico (chart) |
| `[Texto]` (curto, sem underscores) | botão |
| `(!) texto` | alerta/banner |
| `- item` | item de lista (linhas `-` consecutivas = uma lista) |
| `\| a \| b \|` (linhas consecutivas) | tabela (1ª linha = cabeçalho) |
| texto livre | label |

Desambiguação: `[token]` sem `____`/`~` → botão; `[token____]` → input; `[~...~]` → gráfico;
card só via `card "...":` + indentação. Mapa completo DSL → componente genérico em
`componentes.md`. Exemplo:

```wireframe
# Painel do Modelo
[[ v7 | 82% acc | drift OK ]]
[~ tendência de acurácia ~]
(!) 312 créditos sem rating
[Configurar] [Precision/Recall] [Recalcular]
```

## Saída
- **Cap. 1** do `refined/Requisitos/<feature>.md` preenchido, com o Mermaid de fluxo (1.1), o de navegação (1.3), e por tela a linha **Arquétipo:** (`A-NN` de `telas-comuns.md`) + bloco ` ```wireframe ` + linha **Componentes:** (nomes genéricos), com telas minimizadas (arquétipos reusados, vistas fundidas em abas/drawers). Frontmatter `tipo: contract`.
- `refined/componentes.md` mantido como ponteiro fino do vocabulário genérico de componentes.
