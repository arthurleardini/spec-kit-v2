---
name: contrato-dados
description: Use quando o usuário quer gerar ou revisar o modelo de Dados (Cap. 4) do doc de Requisitos de uma feature no modelo wikiLLM — modelo derivado do eixo, não paralelo.
---

# contrato-dados

Escreve e mantém o **Capítulo 4 — Dados** do documento único `refined/Requisitos/<feature>.md` da Camada de Requisitos. Não cria arquivo solto: o doc de requisitos de cada feature é **um só** (4 capítulos); esta skill é dona do Cap. 4.

Responde à pergunta-mãe *Que informação a feature manipula?* — descreve o modelo de dados conceitual: entidades, campos e relações. O modelo é **derivado, não paralelo** (BL-08): nasce do eixo da feature, não é um artefato independente.

**Regra de não-sobreposição** (ver bloco-intro do `Requisitos/<feature>.md`): cada fato mora em UM lugar. Este capítulo é o modelo conceitual; invariantes de domínio permanecem como `RN-NN` na Visão (citados por ID, nunca reescritos aqui), e o que o sistema deve fazer fica na tabela RF do Cap. 3.1.

## Quando usar
Quando o usuário pede para criar, escrever ou revisar o modelo de dados de uma feature — ou pede para listar as entidades, os campos ou as relações de informação do produto.

## Eixo (`processo` | `classe`) — como derivar
Ler `eixo` no frontmatter do `Requisitos/<feature>.md`. O Cap. 4 **deriva** do que já foi escrito nos capítulos anteriores:
- **`eixo=classe`** — cada formulário/objeto do Cap. 1 **é** uma entidade; os campos do formulário são os campos da classe. A classe já é o modelo de dados (formulário ≈ classe). Não inventar entidades paralelas às telas.
- **`eixo=processo`** — derivar as entidades das **atividades** do fluxo (Cap. 1.1): cada informação processada ou produzida ao longo das atividades vira entidade ou campo.
Anotar a origem de cada entidade (ex.: `<!-- deriva de: formulário X | atividade Y -->`).

## Entrada
A Camada de Intenção em `refined/visao.md` (especialmente o Glossário do Cap. 2 para o vocabulário e as Regras do Cap. 3), a fonte da feature (brainstorm/documento associado) e os **Caps. 1, 2 e 3** já preenchidos no `Requisitos/<feature>.md` da feature. Se a fonte for documento binário (PDF/DOCX/PPTX), converter com `markitdown` antes de ler.

## Processo
1. Ler `refined/visao.md` e a fonte da feature. Conferir o `eixo` e reler os Caps. 1–3 do `Requisitos/<feature>.md` (deles vem o modelo).
2. No mesmo `refined/Requisitos/<feature>.md`, preencher o **Cap. 4 — Dados**, sem tocar nos Caps. 1, 2 e 3, **derivando** conforme o `eixo`:
   - **4.1 Entidades:** uma subseção por entidade, com tabela de campos. O tipo de cada campo é **simples e agnóstico** — `texto`, `número`, `data`, `booleano`, `referência`.
   - **4.2 Relações:** cardinalidade entre entidades (`1:N` / `N:N` / `1:1`) com descrição.
3. **Proibido** neste capítulo: endpoints, contratos de API, métodos HTTP, DDL/SQL, tipos de banco específicos e diagramas. Apenas o modelo conceitual — entidades, campos e relações.
4. Usar a terminologia do Glossário (Cap. 2 de `visao.md`). Marcar lacunas com `⚠ NÃO IDENTIFICADO — definir: <pergunta>` e inferências com `*(inferência)*`.
5. Salvar o `Requisitos/<feature>.md`. Atualizar `refined/index.md` (linha da feature) e anexar entrada em `refined/log.md`.

## Saída
**Cap. 4** do `refined/Requisitos/<feature>.md` preenchido, com frontmatter `tipo: contract` — somente entidades, campos (tipos agnósticos) e relações, **derivados** do eixo da feature.
