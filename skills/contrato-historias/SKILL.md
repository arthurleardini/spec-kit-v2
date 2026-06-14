---
name: contrato-historias
description: Use quando o usuário quer gerar ou revisar as Histórias (user stories, Cap. 2) do doc de Requisitos de uma feature no modelo wikiLLM.
---

# contrato-historias

Escreve e mantém o **Capítulo 2 — Histórias** do documento único `refined/Requisitos/<feature>.md` da Camada de Requisitos. Não cria arquivo solto: o doc de requisitos de cada feature é **um só** (4 capítulos); esta skill é dona do Cap. 2.

Responde à pergunta-mãe *O que a feature entrega, do ponto de vista do usuário?* — quebra a feature em histórias (`US-NN`) com épico, backlog priorizado e detalhamento de cada história.

**Regra de não-sobreposição** (ver bloco-intro do `Requisitos/<feature>.md`): cada fato mora em UM lugar. Este capítulo é dono da jornada da persona (Objetivo + Passos). As User Stories **não** levam critérios de aceite — a prova (Dado/Quando/Então) vive no Cap. 3.3. O Epic cita o `JTBD-NN` da Visão **por ID**, sem reparafrasear o enunciado. Não repetir aqui, como prosa, o que o sistema deve fazer (isso é a tabela RF do Cap. 3.1).

## Quando usar
Quando o usuário pede para criar, escrever ou revisar as histórias / user stories de uma feature — ou pede para detalhar o backlog ou a jornada da persona.

## Eixo (`processo` | `classe`)
Ler `eixo` no frontmatter do `Requisitos/<feature>.md` para alinhar o detalhamento das histórias:
- **`eixo=processo`** — as histórias tendem a acompanhar as **atividades** do fluxo (Cap. 1.1); cada passo relevante do processo vira uma ou mais histórias.
- **`eixo=classe`** — as histórias tendem a girar em torno dos **formulários/objetos** (criar, editar, listar, validar cada classe).
As **Telas acionadas** de cada história devem referenciar os ids de tela do Cap. 1.

## Entrada
A Camada de Intenção em `refined/visao.md` (personas, jobs, regras, métricas), a fonte da feature (brainstorm/documento associado), o **Cap. 1** já preenchido no `Requisitos/<feature>.md` da feature (para referenciar telas) e qualquer conversa/brainstorm associada. Se a fonte for documento binário (PDF/DOCX/PPTX), converter com `markitdown` antes de ler.

## Processo
1. Ler `refined/visao.md`, a fonte da feature e o Cap. 1 do `Requisitos/<feature>.md` (se já existir). Conferir o `eixo`.
2. No mesmo `refined/Requisitos/<feature>.md`, preencher o **Cap. 2 — Histórias**, sem tocar nos Caps. 1, 3 e 4: épico (citando o `JTBD-NN` por ID, sem reparafrasear), métricas relevantes, tabela-resumo de backlog e as subseções de user stories.
3. Cada história deve ter os **5 itens**: Persona, Objetivo (formato "Como… quero… para…"), Passos da jornada, Telas acionadas (ids de tela do Cap. 1) e Capacidades de IA (`RN-AI-NN`, se aplicável). **Sem** critérios de aceite — eles vivem como cenários no Cap. 3.3.
4. IDs `US-NN` estáveis — não renumerar. Se o capítulo já existir, revisar garantindo que toda história tem os 5 itens completos e detalhados e remover qualquer "Critérios de aceite" remanescente.
5. Marcar inferências com `*(inferência)*` e lacunas com `⚠ NÃO IDENTIFICADO — definir: <pergunta>`.
6. Salvar o `Requisitos/<feature>.md`. Atualizar `refined/index.md` (linha da feature) e anexar entrada em `refined/log.md`.

## Saída
**Cap. 2** do `refined/Requisitos/<feature>.md` preenchido, com frontmatter `tipo: contract` e cada história com os 5 itens (sem critérios de aceite).
