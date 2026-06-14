---
name: contrato-telas-fluxos
description: Use quando o usuário quer gerar ou revisar as Telas e Fluxos (Cap. 1) do contrato.md de uma feature no modelo wikiLLM — inclui o diagrama Mermaid de navegação.
---

# contrato-telas-fluxos

Escreve e mantém o **Capítulo 1 — Telas & Fluxos** do documento único `refined/contracts/<feature>/contrato.md` da Camada de Contrato. Não cria arquivo solto: o contrato de cada feature é **um só** (4 capítulos); esta skill é dona do Cap. 1.

Responde à pergunta-mãe *Como o usuário interage com a feature?* — descreve o fluxo da feature em termos de informação e ações (agnóstico de UI), detalha cada tela e **emite um diagrama Mermaid de navegação** (BL-21). Também mantém o catálogo product-level de blocos de UI reutilizáveis.

**Regra de não-sobreposição** (ver bloco-intro do `contrato.md`): cada fato mora em UM lugar. Telas/fluxo são deste capítulo; não repetir aqui jornada da persona (Cap. 2), o que o sistema deve fazer (Cap. 3.1 RF) nem critérios de prova (Cap. 3.3 Cenários).

## Quando usar
Quando o usuário pede para criar, escrever ou revisar as telas e os fluxos de uma feature — ou pede para descrever a jornada de interação, as telas, os estados de tela, a navegação ou o diagrama de fluxo do produto.

## Eixo (`processo` | `classe`)
Ler `eixo` no frontmatter do `contrato.md` (defini-lo se ainda não existir, perguntando ao usuário ou inferindo: feature de fluxo/atividades → `processo`; feature de formulários/objetos → `classe`). O Cap. 1 sempre tem **dois** Mermaid: o de **fluxo** (1.1) e o de **navegação entre telas** (1.3). Não há mais subseção 1.4 separada.
- **`eixo=processo`** — a **1.1** funde fluxo e processo num único flowchart (estilo BPMN leve: atividades/informações como nós, gateways `{ }`, do gatilho às saídas).
- **`eixo=classe`** — a **1.1** é um flowchart simples do ciclo do formulário/registro (criar → validar → salvar → editar).

## Entrada
A Camada de Intenção consolidada em `refined/intencao/visao.md` (produto, personas, jobs, regras) e a fonte da feature: a entidade em `refined/entities/features/<feature>.md` mais qualquer conversa/brainstorm ou documento associado. Se a fonte for documento binário (PDF/DOCX/PPTX), converter com `markitdown` antes de ler.

## Processo
1. Ler `refined/intencao/visao.md` e a fonte da feature. Determinar/confirmar o `eixo`.
2. Abrir (ou criar a partir de `templates/contrato/contrato.md`) o `refined/contracts/<feature>/contrato.md` e preencher o **Cap. 1 — Telas & Fluxos**, sem tocar nos Caps. 2–4:
   - **1.1 Fluxo (Mermaid):** um flowchart Mermaid (não prosa em bullets). Nós = `<informação> → <ação> → <resultado>`; `{ }` = decisões; `([ ])` = gatilho/saídas; mais **uma** linha de legenda. Se `eixo=processo`, este flowchart funde fluxo e processo (BPMN leve, gatilho → atividades → saídas); se `eixo=classe`, é o ciclo simples do formulário/registro.
   - **1.2 Telas detalhadas:** uma subseção por tela, com objetivo, conteúdo, ações, estados, navegação e os blocos referenciados.
   - **1.3 Diagrama de navegação (Mermaid):** **obrigatório**. Bloco ` ```mermaid ` com `flowchart`; cada nó é uma tela (usar o `<id da tela>` do 1.2), cada aresta é uma transição rotulada com a ação que a dispara.
3. Manter o catálogo product-level `refined/contracts/_componentes.md` (template `templates/contrato/_componentes.md`): ao identificar um bloco de UI que se repete entre telas/features, adicionar ou atualizar a subseção correspondente. O catálogo fica na **raiz** de `refined/contracts/`, não dentro da pasta da feature. As telas do 1.2 referenciam estes blocos por nome (campo **Blocos:**) em vez de redescrevê-los.
4. Marcar inferências com `*(inferência)*` e lacunas com `⚠ NÃO IDENTIFICADO — definir: <pergunta>`.
5. Salvar o `contrato.md`. Atualizar `refined/index.md` (linha da feature) e anexar entrada em `refined/log.md`.

## Saída
- **Cap. 1** do `refined/contracts/<feature>/contrato.md` preenchido, com o Mermaid de fluxo (1.1) e o de navegação (1.3) e frontmatter `tipo: contract`.
- `refined/contracts/_componentes.md` criado ou atualizado com os blocos de UI da feature.
