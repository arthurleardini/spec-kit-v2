---
name: contrato-requisitos
description: Use quando o usuário quer gerar ou revisar os Requisitos e Cenários de Teste (Cap. 3) do contrato.md de uma feature no modelo wikiLLM.
---

# contrato-requisitos

Escreve e mantém o **Capítulo 3 — Requisitos & Cenários de Teste** do documento único `refined/contracts/<feature>/contrato.md` da Camada de Contrato. Não cria arquivo solto: o contrato de cada feature é **um só** (4 capítulos); esta skill é dona do Cap. 3.

Responde à pergunta-mãe *O que o produto deve cumprir — e como provar?* — formaliza os requisitos funcionais (o que o produto deve fazer) e não-funcionais (com que qualidade), rastreáveis a regras de negócio e histórias, **e** descreve os **cenários de teste** (Gherkin-like Dado/Quando/Então) que validam esses requisitos (BL-06).

**Regra de não-sobreposição** (ver bloco-intro do `contrato.md`): cada fato mora em UM lugar. O *o que o sistema deve fazer* + rastreio RN/US é a **tabela RF (3.1)** — não repetir como prosa no Cap. 2. O *como se prova* (Dado/Quando/Então) é o **3.3** — as User Stories não levam critérios de aceite. Invariantes de domínio são `RN-NN` na Visão, citados por ID; nunca reescrever o enunciado aqui.

## Quando usar
Quando o usuário pede para criar, escrever ou revisar os requisitos de uma feature — ou pede para listar requisitos funcionais e não-funcionais, definir critérios de qualidade, escrever cenários de teste / casos de teste, ou rastrear requisitos a regras e histórias.

## Eixo (`processo` | `classe`)
Ler `eixo` no frontmatter do `contrato.md` para focar os cenários de teste:
- **`eixo=processo`** — cobrir os caminhos do fluxo: caminho feliz, cada ramo de decisão (gateways do Cap. 1.1) e as exceções entre atividades.
- **`eixo=classe`** — cobrir o ciclo de cada formulário/classe: criação válida, validações de campo, edição e estados de borda.

## Entrada
A Camada de Intenção em `refined/intencao/visao.md` (especialmente Regras `RN-NN` e Métricas `IM-NN` do Cap. 3), a entidade da feature em `refined/entities/features/<feature>.md` e os **Caps. 1 e 2** já preenchidos no `contrato.md` da feature. Se a fonte for documento binário (PDF/DOCX/PPTX), converter com `markitdown` antes de ler.

## Processo
1. Ler `refined/intencao/visao.md`, a fonte da feature e os Caps. 1 e 2 do `contrato.md`. Conferir o `eixo`.
2. No mesmo `refined/contracts/<feature>/contrato.md`, preencher o **Cap. 3 — Requisitos & Cenários de Teste**, sem tocar nos Caps. 1, 2 e 4:
   - **3.1 Requisitos Funcionais:** tabela com um `RF-NN` por linha, cada um rastreável a regras de negócio (`RN-NN`) e a histórias (`US-NN` do Cap. 2).
   - **3.2 Requisitos Não-Funcionais:** agrupados por categoria — Performance, Segurança, Disponibilidade, Auditoria, Conformidade, Escalabilidade, Observabilidade. Incluir apenas as categorias aplicáveis; um marcador `RNF-<categoria>-NN` por requisito.
   - **3.3 Cenários de Teste:** um cenário Gherkin-like por caso (`CT-NN`), no formato **Dado / Quando / Então**, cada um rastreando o(s) `RF-NN` (e/ou `US-NN`) que verifica. Cobrir caminho feliz, exceções e estados de borda conforme o `eixo`.
3. Indicar a origem (Regras `RN` da Visão) e o horizonte (H1/H2/H3) no cabeçalho do capítulo.
4. IDs `RF-NN`, `RNF-*` e `CT-NN` estáveis — não renumerar. Marcar lacunas com `⚠ NÃO IDENTIFICADO — definir: <pergunta>` e inferências com `*(inferência)*`.
5. Salvar o `contrato.md`. Atualizar `refined/index.md` (linha da feature) e anexar entrada em `refined/log.md`.

## Saída
**Cap. 3** do `refined/contracts/<feature>/contrato.md` preenchido, com frontmatter `tipo: contract`, RFs rastreáveis a RN/US, RNFs por categoria e cenários de teste `CT-NN` (Dado/Quando/Então) rastreáveis aos requisitos.
