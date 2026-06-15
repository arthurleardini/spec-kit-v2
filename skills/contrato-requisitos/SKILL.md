---
name: contrato-requisitos
description: Use quando o usuário quer gerar ou revisar os Requisitos e Cenários de Teste (Cap. 2) do doc de Requisitos de uma feature no modelo wikiLLM — inclui personas & objetivos (intenção do usuário), RF/RNF e cenários.
---

# contrato-requisitos

Escreve e mantém o **Capítulo 2 — Requisitos & Cenários de Teste** do documento único `refined/Requisitos/<feature>.md` da Camada de Requisitos. Não cria arquivo solto: o doc de requisitos de cada feature é **um só** (3 capítulos — Telas & Fluxos, Requisitos & Cenários, Dados); esta skill é dona do Cap. 2.

> **Não há mais capítulo de Histórias.** Histórias e Requisitos eram redundantes — a intenção do usuário (persona → objetivo) foi **absorvida** por este capítulo, na subseção **2.1 Personas & objetivos**. Os requisitos descrevem o que o produto deve cumprir de forma **detalhada**, ancorados nas personas, sem duplicar uma camada de user stories.

Responde à pergunta-mãe *Para quem, o que o produto deve cumprir — e como provar?* — captura as personas e seus objetivos (intenção), formaliza os requisitos funcionais (o que o produto deve fazer) e não-funcionais (com que qualidade), rastreáveis a regras de negócio, **e** descreve os **cenários de teste** (Gherkin-like Dado/Quando/Então) que validam esses requisitos.

**Pense transversalmente.** Antes de escrever qualquer requisito, leia `refined/requisitos-transversais.md`: os requisitos comuns a várias features (`RNF-T-*`, `RF-T-*`) **não** se reescrevem na feature — só se **citam por ID** (ex.: "Segurança: aplica-se `RNF-T-SEG-01`, `RNF-T-SEG-02`"). O capítulo reserva-se ao que é **genuinamente próprio** da feature (thresholds próprios, regras exclusivas, CTs particulares).

**Regra de não-sobreposição** (ver bloco-intro do `Requisitos/<feature>.md`): cada fato mora em UM lugar. Persona + objetivo é a **2.1**. O *o que o sistema deve fazer* + rastreio RN é a **tabela RF (2.2)**. O *como se prova* (Dado/Quando/Então) é a **2.4**. Requisitos comuns a várias features são `RNF-T-*` / `RF-T-*` em `requisitos-transversais.md`, citados por ID; invariantes de domínio são `RN-NN` na Visão, citados por ID — nunca reescrever o enunciado aqui.

## Quando usar
Quando o usuário pede para criar, escrever ou revisar os requisitos de uma feature — ou pede para listar personas e objetivos da feature, requisitos funcionais e não-funcionais, definir critérios de qualidade, escrever cenários de teste / casos de teste, ou rastrear requisitos a regras e a transversais.

## Eixo (`processo` | `classe`)
Ler `eixo` no frontmatter do `Requisitos/<feature>.md` para focar os cenários de teste:
- **`eixo=processo`** — cobrir os caminhos do fluxo: caminho feliz, cada ramo de decisão (gateways do Cap. 1.1) e as exceções entre atividades.
- **`eixo=classe`** — cobrir o ciclo de cada formulário/classe: criação válida, validações de campo, edição e estados de borda.

## Entrada
A Camada de Intenção em `refined/visao.md` (personas e jobs do Cap. 1; Regras `RN-NN` e Métricas `IM-NN` do Cap. 3), os **transversais** `refined/requisitos-transversais.md` (para citar `RNF-T-*`/`RF-T-*`), a fonte da feature (brainstorm/documento associado) e o **Cap. 1** já preenchido no `Requisitos/<feature>.md` (para referenciar telas nas personas). Se a fonte for documento binário (PDF/DOCX/PPTX), converter com `markitdown` antes de ler.

## Processo
1. Ler `refined/visao.md`, `refined/requisitos-transversais.md`, a fonte da feature e o Cap. 1 do `Requisitos/<feature>.md`. Conferir o `eixo`.
2. No mesmo `refined/Requisitos/<feature>.md`, preencher o **Cap. 2 — Requisitos & Cenários de Teste**, sem tocar nos Caps. 1 e 3:
   - **2.1 Personas & objetivos:** tabela persona → objetivo → `JTBD-NN`. As personas são as da Visão §1, citadas por nome; aqui captura-se a intenção do usuário sem montar uma camada de user stories separada.
   - **2.2 Requisitos Funcionais:** tabela com um `RF-NN` por linha, cada um rastreável a regras de negócio (`RN-NN`) e à(s) persona(s) que serve. Listar os `RF-T-NN` aplicáveis (de `requisitos-transversais.md`) no bloco "Transversais aplicáveis", **sem** reescrever os enunciados.
   - **2.3 Requisitos Não-Funcionais:** apenas os RNF **próprios** da feature, agrupados por categoria (Performance, Segurança, Disponibilidade, Auditoria, Conformidade, Escalabilidade, Observabilidade); um marcador `RNF-<categoria>-NN` por requisito. Listar os `RNF-T-*` aplicáveis no bloco "Transversais aplicáveis"; só detalhar o que **diverge** ou **acrescenta** ao transversal.
   - **2.4 Cenários de Teste:** um cenário Gherkin-like por caso (`CT-NN`), no formato **Dado / Quando / Então**, cada um rastreando o(s) `RF-NN` (ou `RF-T-NN`/`RNF-T-*`) que verifica. Cobrir caminho feliz, exceções e estados de borda conforme o `eixo`.
3. Indicar a origem (Regras `RN` da Visão) e o horizonte (H1/H2/H3) no cabeçalho do capítulo.
4. IDs `RF-NN`, `RNF-*` e `CT-NN` estáveis — não renumerar. Marcar lacunas com `⚠ NÃO IDENTIFICADO — definir: <pergunta>` e inferências com `*(inferência)*`.
5. Salvar o `Requisitos/<feature>.md`. Atualizar `refined/index.md` (linha da feature) e anexar entrada em `refined/log.md`.

## Saída
**Cap. 2** do `refined/Requisitos/<feature>.md` preenchido, com frontmatter `tipo: contract`: a tabela de personas & objetivos (2.1), RFs rastreáveis a RN/persona com transversais citados (2.2), RNFs próprios por categoria com transversais citados (2.3) e cenários de teste `CT-NN` (Dado/Quando/Então) rastreáveis aos requisitos (2.4).
