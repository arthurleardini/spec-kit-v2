---
name: feature-telas-fluxos
description: Use quando o usuário quer escrever ou revisar o fluxo e as telas de uma feature — subseções 7.N.1 (fluxo e navegação em Mermaid) e 7.N.2 (telas com arquétipo e wireframe) do `spec.md`.
---

# feature-telas-fluxos

Dona das subseções **7.N.1 (Fluxo e navegação)** e **7.N.2 (Telas)** de uma feature.

Responde: *como o usuário atravessa a feature?*

## Quando usar
Quando o usuário pede o fluxo, o processo, as telas, a navegação ou o wireframe de uma
feature.

## Entrada
Seções 1 a 6 do `spec.md` (personas, regras, entidades, arquétipos) e a fonte da feature.

## Metadados da feature

A primeira linha da feature declara, obrigatoriamente:

```
**Eixo:** processo | classe · **Apetite:** <2 semanas | 6 semanas> · **Fora desta feature:** <no-gos>
```

- **Eixo** — `processo` (fluxo/atividades) ou `classe` (formulários/objetos). Orienta o
  fluxo e o modelo de dados.
- **Apetite** — quanto tempo o problema vale, não quanto a solução leva. É a caixa: a
  quantidade de tela e de RF se ajusta a ela.
- **Fora desta feature** — os no-gos. O que alguém razoavelmente esperaria aqui e não vai
  ter. Declarar evita a discussão na entrega.

## Processo

1. **7.N.1 — dois diagramas Mermaid.**
   - **Fluxo.** `eixo=processo`: flowchart de atividades estilo BPMN leve, do gatilho às
     saídas, com losango `{}` em cada decisão. `eixo=classe`: ciclo do registro
     (criar → validar → salvar → editar). Nós `[ ]` = informação/ação/resultado,
     `{ }` = decisão, `([ ])` = gatilho e saída.
   - **Navegação.** Flowchart entre as telas: cada nó é uma tela (`T-NN`), cada aresta é a
     ação que dispara a transição.
   - Todo ramo de exceção do fluxo tem de existir também como RF padrão #5
     (`Se <gatilho>, então …`) na 7.N.3. Ramo desenhado e não especificado é furo.

2. **7.N.2 — uma subseção por tela**, com id `T-NN` (contínuo no spec inteiro, não por
   feature). Para cada tela: `**Arquétipo:**` (`A-NN` de §6, ou `—`), objetivo, bloco
   ` ```wireframe `, conteúdo, ações, estados, componentes.

3. **Minimizar tela.** Antes de criar uma tela nova: existe arquétipo em §6 que resolve?
   dá para fundir em aba, drawer ou painel lateral? Padrão que aparece em ≥2 features vai
   para §6, não se duplica. Teto de telas por feature em `[tetos]`.

4. **Wireframe (DSL line-based).** Render é fat marker, só-layout — mostra formas, não
   texto legível. Os rótulos servem ao autor.

   | Sintaxe | Componente |
   |---|---|
   | `# Texto` | toolbar (barra de título) |
   | `## Texto` | cabeçalho de seção |
   | `[[ a \| b \| c ]]` | linha de N colunas iguais |
   | `card "Título":` + linhas indentadas (2 espaços) | card com filhos |
   | `[Rótulo____]` (≥2 underscores finais) | input |
   | `[~ legenda ~]` | chart |
   | `[Texto]` | button |
   | `(!) texto` | banner |
   | `- item` | list |
   | `\| a \| b \|` | table (1ª linha = cabeçalho) |

   Desambiguação: `[x]` → botão · `[x____]` → input · `[~x~]` → gráfico. Card só via
   `card "...":` + indentação.

5. **Componentes** pelo nome genérico do Anexo A (toolbar, card, table, list, button,
   input, select, tabs, dialog, chart), agnóstico de framework.

## Saída
Subseções 7.N.1 e 7.N.2 preenchidas, com a linha de metadados, dois Mermaid, e cada tela
etiquetada com arquétipo e wireframe.
