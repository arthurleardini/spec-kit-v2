---
titulo: Referências para o spec-kit v3
tipo: dossie-referencias
criado_em: 2026-07-29
origem: pesquisa web (ISO 29148, EARS, SBE, Insanely Simple, Maeda, Shape Up, Google Tech Writing, Amazon PR/FAQ, GitHub Spec Kit)
status: insumo
---

# Referências para o spec-kit v3

Base externa que o v3 vai internalizar. Cada bloco termina em **regra do kit** — o que
entra em template, skill ou lint. Referência sem regra derivada não entra.

Escopo: **requisitos funcionais**. Não-funcional aparece só onde o padrão citado obriga.

---

## A. Qualidade do requisito individual

### ISO/IEC/IEEE 29148 — características

O padrão lista as características de um requisito bem-formado: **necessário, apropriado,
não-ambíguo, completo, singular, factível, verificável, correto, conforme, rastreável**.
Duas mordem direto na brevidade e na auditabilidade:

- **Singular** — o requisito declara *uma* capacidade. Um `e` conectando duas capacidades
  é dois requisitos.
- **Verificável** — a realização é objetivamente verificável/mensurável. Sem isso, "está
  implementado?" é opinião.

### Wiegers — palavras fracas

Requisito não-ambíguo admite **uma** leitura. Wiegers ataca o vocabulário subjetivo:
`fácil, simples, rápido, eficiente, flexível, amigável, robusto, adequado, relevante,
tempo real, quando aplicável, se necessário, etc., e/ou, apoiar/suportar, minimizar,
maximizar, otimizar`. Regra dele: requisito que diz que o produto "shall support X" não é
verificável.

Formas de revelar ambiguidade: inspeção formal, **escrever o caso de teste a partir do
requisito** (se não dá para escrever, o requisito está furado), e cenários de usuário.

### Requirements smells (Femmer, Wagner, Méndez, Eder)

Catálogo de "cheiros" derivado do próprio ISO 29148, detectável de forma barata e
automática (precisão média ~59%, recall ~82% no estudo). Classes principais:

| Smell | O que é |
|---|---|
| Subjective language | "amigável", "adequado", "similar" |
| Ambiguous adverbs/adjectives | "quase sempre", "significativo" |
| Superlatives / comparatives | "o mais rápido", "melhor que" |
| Loopholes | "se possível", "quando aplicável", "conforme necessário" |
| Non-verifiable terms | "otimizado", "suficiente" |
| Vague pronouns | "isso", "o mesmo", "ele" sem antecedente |
| Incomplete references | "ver documentação", link sem ID |
| Negative statements | requisito só pelo que o sistema não faz |

Conclusão do estudo que interessa: smell-check **não substitui** revisão; é feedback
rápido *antes* dela.

> **Regra do kit.** (1) Lista fechada de palavras proibidas em RF, com verificação
> determinística no lint. (2) Gate de singularidade: RF com `e`/`ou` ligando capacidades é
> erro, não estilo. (3) Gate de testabilidade: RF sem cenário de teste correspondente é
> erro. Já era o M1/M3 do backlog do v2; no v3 vira lint bloqueante, não warning.

---

## B. Sintaxe de requisito funcional — EARS

EARS (*Easy Approach to Requirements Syntax*), de Alistair Mavin e colegas na Rolls-Royce,
publicado no RE'09. Restringe linguagem natural com um punhado de palavras estruturais e
uma ordem fixa de cláusulas. Resolve exatamente o problema de "redação técnica de RF":
não é linguagem formal, não é prosa solta.

**Forma geral:** `While <precondição>, When <gatilho>, o <sistema> shall <resposta>`

Os 5 padrões + o composto:

| # | Padrão | Template | Palavra-chave |
|---|---|---|---|
| 1 | Ubíquo | `O <sistema> deve <resposta>` | — |
| 2 | Dirigido por estado | `Enquanto <precondição>, o <sistema> deve <resposta>` | Enquanto |
| 3 | Dirigido por evento | `Quando <gatilho>, o <sistema> deve <resposta>` | Quando |
| 4 | Feature opcional | `Onde <feature existe>, o <sistema> deve <resposta>` | Onde |
| 5 | Comportamento indesejado | `Se <gatilho>, então o <sistema> deve <resposta>` | Se / então |
| 6 | Composto | `Enquanto <precondição>, quando <gatilho>, o <sistema> deve <resposta>` | — |

**Ruleset EARS** (o que dá para checar com script): cada requisito tem *zero ou muitas*
precondições, *zero ou um* gatilho, *um* nome de sistema, *uma ou muitas* respostas.

Ganhos práticos: o padrão #5 (`Se ... então`) força o autor a enumerar desvio e exceção —
o furo mais comum das specs auditadas no v2 (M2 do backlog: mínimo de ramos de exceção por
fluxo). O padrão #2 separa estado de gatilho, que em prosa solta viram a mesma frase
confusa.

> **Regra do kit.** RF do v3 é escrito em **EARS-PT** (tabela acima). O lint classifica
> cada RF num dos 6 padrões; RF que não casa com nenhum é erro de forma. Contagem de
> padrão #5 por feature é a métrica de cobertura de desvio (substitui a contagem de ramos
> Mermaid, que era frágil).

---

## C. Exemplo como especificação — Specification by Example

Gojko Adzic: em vez de documento estático longo, **exemplos concretos** ilustram e validam
o comportamento; viram teste executável e documentação viva. O ciclo é: derivar escopo do
objetivo → ilustrar com exemplos → refinar a especificação → automatizar validação →
validar com frequência → evoluir o sistema de documentação.

Dois conceitos aproveitáveis direto:

- **Key examples** — não todos os exemplos; o conjunto mínimo que ilustra a regra e seus
  limites. Antídoto contra a explosão de cenários Gherkin.
- **Living documentation** — o mesmo artefato serve negócio e time. Se RF e cenário dizem
  a mesma coisa duas vezes, um dos dois é redundante.

O v2 já matou "Histórias" por redundância com Requisitos. O mesmo argumento vale entre RF
e cenário: **o cenário é a verificação do RF, não a repetição narrativa dele.**

> **Regra do kit.** Cenário de teste do v3 é **key example**: 1 caminho feliz + os desvios
> que existem como RF padrão #5. Proibido cenário que só reescreve o RF em Gherkin. Lint
> checa relação 1:N RF → cenário e sinaliza cenário sem RF-pai.

---

## D. Simplicidade

### Insanely Simple (Ken Segall) — os 10 elementos

Os dez elementos, com a leitura aplicada a spec:

| Elemento | Original | Tradução p/ spec |
|---|---|---|
| Think Brutal | ser direto quando alguém desvia p/ complexidade | crítico do kit tem licença p/ reprovar; sem elogio, sem "poderia considerar" |
| Think Small | grupo pequeno de gente boa > grupo grande | poucos agentes especialistas, cada um com um mandato; nada de agente genérico |
| Think Minimal | uma mensagem por comunicação; 5 ideias ninguém lembra | um artefato por camada, um capítulo por assunto, um RF por frase |
| Think Motion | prazo apertado mantém foco | loop crítico tem número fixo de rodadas, não roda até "ficar bom" |
| Think Iconic | símbolo visual comunica melhor que texto | wireframe fat-marker + Mermaid em vez de parágrafo descrevendo tela |
| Think Phrasal | frase curta, vocabulário simples; inteligência vem da clareza | limite duro de palavras por RF e por capítulo |
| Think Casual | conversa gera ideia melhor que apresentação formal | levantamento é conversa dirigida, não formulário |
| Think Human | falar como o cliente fala, sem jargão de spec | glossário do domínio como guard-rail de linguagem |
| Think Skeptic | esperar resistência a "não dá" | lacuna explícita (`⚠ NÃO IDENTIFICADO`) em vez de RF vago para tapar buraco |
| Think War | tratar o essencial como batalha | o que não é mínimo comum é opcional e não é gerado |

Regras concretas do livro que viram mecanismo: **só quem tem motivo entra na sala**
(no kit: só o agente dono do capítulo escreve nele); **o decisor participa do começo ao
fim** (no kit: checkpoint humano por camada, não só no final); **nunca duas mensagens no
mesmo artefato**.

### The Laws of Simplicity (John Maeda)

Lei 1 **Reduce**, lei 2 **Organize**, lei 3 **Time**, lei 4 **Learn**; lei 10 **The One**:
"simplicidade é subtrair o óbvio e adicionar o significativo".

Dois frameworks táticos:

- **SHE** (reduzir): *Shrink, Hide, Embody* — encolher, esconder, incorporar.
- **SLIP** (organizar): *Sort, Label, Integrate, Prioritize*.

Mapeamento direto no que o v2 já faz por instinto: transversais = **Integrate**;
arquétipo de tela `A-NN` = **Label**; mínimo comum vs opcional = **Prioritize**; navigator
com submenu = **Sort**; capítulo opcional não gerado = **Hide**.

### Shape Up (Ryan Singer / Basecamp)

- **Appetite** — a pergunta não é "quanto tempo leva?", é "quanto tempo isso vale?". O
  apetite é a caixa; a solução se ajusta a ela.
- **Breadboarding** — lugares, affordances e conexões, sem desenho visual. É o Mermaid de
  navegação do v2, com nome melhor.
- **Fat marker sketch** — traço tão grosso que detalhe é impossível. Já é a DSL de
  wireframe do v2.
- **Rabbit holes** e **no-gos** — o pitch declara onde não entrar e o que está fora. O v2
  tem `fora-escopo` no arquivo; falta o no-go *dentro* da feature.

> **Regra do kit.** (1) **Apetite por feature** no frontmatter — a caixa que limita
> quantidade de tela e de RF. (2) Seção `No-gos / rabbit holes` no doc de feature,
> obrigatória. (3) Limite duro de tamanho por artefato (SHE/Think Minimal), verificado por
> lint: se passou, corta — não amplia o limite. (4) Toda regra nova do kit tem de matar
> outra ou justificar: **subtrair o óbvio**.

---

## E. Redação

### Google Technical Writing

Uma ideia por frase. Frase curta. Voz ativa — mais curta e mais precisa; boa frase técnica
diz **quem faz o que a quem**. Lista embutida em parágrafo é ruim: virar bullet ou lista
numerada. Tabela quebra monotonia e melhora leitura. Evitar idiomatismo.

Voz ativa + "quem faz o que a quem" é a mesma exigência do EARS (`o <sistema> deve
<resposta>`): as duas referências convergem.

### Amazon — narrativa, PR/FAQ, six-pager

Slide banido em documento de decisão. Seis páginas foi o ponto de equilíbrio achado por
tentativa: longo o bastante p/ profundidade, curto o bastante p/ **forçar clareza**.
Narrativa densa, sem bullet solto e sem enfeite. Trabalhar de trás p/ frente: escrever
primeiro o documento do lançamento (press release + FAQ), depois os que se aproximam da
implementação.

Tensão útil: Amazon prefere prosa narrativa; requisito quer tabela e frase-padrão. Resolve
por camada — **Visão é narrativa** (por quê / para quem), **Requisitos é tabela + EARS**
(o quê). Não misturar registro no mesmo capítulo.

> **Regra do kit.** (1) Cada capítulo declara seu registro: narrativa (Visão) ou
> estruturado (Requisitos). (2) Orçamento de palavras por artefato, no espírito das seis
> páginas: o teto existe p/ forçar corte. (3) Voz ativa obrigatória em RF, checada pelo
> lint via padrão EARS.

---

## F. Spec-driven development com agentes

### GitHub Spec Kit (referência homônima, útil como benchmark)

Loop de quatro fases, cada uma um markdown que a próxima lê: **Specify → Plan → Tasks →
Implement**. Dois recursos que miram governança e compliance: **constitution** (princípios
invioláveis do projeto, lidos por todas as fases) e **checklist**. Extensões de review
(security, architecture guard) rodam como gate. Agent-agnostic, 30+ agentes suportados.

O que o v2 já tem de equivalente: `templates/wiki/CLAUDE.md` ≈ constitution;
`spec-lint`/`spec-audit` ≈ checklist + gate. O que falta: a **constitution como artefato
de primeira classe**, lida por toda skill, e o gate como *bloqueio*, não relatório.

### Custo de contexto

Restrição prática: artefato longo é caro e degrada o próprio agente que o lê depois.
Brevidade no v3 não é gosto estético — é orçamento de contexto. Artefato menor = mais
rodadas de crítica pelo mesmo custo.

> **Regra do kit.** (1) `constituicao.md` na raiz do wiki: princípios + limites duros +
> vocabulário proibido; toda skill lê antes de escrever. (2) Gate bloqueante entre camadas
> (`spec-lint` com exit code), não relatório opcional. (3) Fase de crítica é loop com
> número fixo de rodadas e critério de saída declarado.

---

## G. Síntese — o que muda no v3

| Referência | Regra derivada | Onde vive |
|---|---|---|
| ISO 29148 (singular, verificável) | 1 capacidade por RF; RF sem CT = erro | lint + skill de requisitos |
| Wiegers (palavras fracas) | lista fechada de proibidos | `constituicao.md` + lint |
| Requirements smells | 8 classes de smell em check determinístico | lint |
| EARS | RF em EARS-PT, 6 padrões, ruleset checável | template + lint + skill |
| SBE (key examples) | cenário = verificação, nunca repetição do RF | skill de requisitos + lint |
| Insanely Simple | agentes pequenos e especialistas; 1 assunto por artefato; crítico brutal | arquitetura de skills |
| Maeda (SHE/SLIP) | transversais, arquétipos, mínimo vs opcional | estrutura do wiki |
| Shape Up | apetite por feature; no-gos; fat marker | frontmatter + template + DSL |
| Google Tech Writing | voz ativa, 1 ideia/frase, tabela > parágrafo | `constituicao.md` |
| Amazon | registro por camada; teto de palavras | template + lint |
| GitHub Spec Kit | constitution de 1ª classe; gate bloqueante | novo artefato + lint |
| Custo de contexto | orçamento de tamanho por artefato | lint |

---

## Fontes

- [Easy Approach to Requirements Syntax — guia oficial (Alistair Mavin)](https://alistairmavin.com/ears/)
- [EARS — Wikipedia](https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax)
- [EARS (RE'09) — PDF](https://ccy05327.github.io/SDD/08-PDF/Easy%20Approach%20to%20Requirements%20Syntax%20(EARS).pdf)
- [FAQ sobre a notação EARS — Jama Software](https://www.jamasoftware.com/requirements-management-guide/writing-requirements/frequently-asked-questions-about-the-ears-notation-and-jama-connect-requirements-advisor/)
- [ISO/IEC/IEEE 29148:2018 — amostra](https://cdn.standards.iteh.ai/samples/72089/62bb2ea1ef8b4f33a80d984f826267c1/ISO-IEC-IEEE-29148-2018.pdf)
- [ISO/IEC/IEEE 29148:2011 — norma](https://www.iso.org/standard/45171.html)
- [Karl Wiegers, *Writing Quality Requirements*](https://www.processimpact.com/articles/qualreqs.pdf)
- [Karl Wiegers, *Watch Out for Ambiguous Requirements*](https://www.linkedin.com/pulse/watch-out-ambiguous-requirements-karl-wiegers)
- [Rapid quality assurance with Requirements Smells (JSS 2017)](https://www.sciencedirect.com/science/article/abs/pii/S0164121216000789)
- [Requirements Quality Defect Detection with the Qualicen Requirements Scout](https://ceur-ws.org/Vol-2075/NLP4RE_paper2.pdf)
- [Gojko Adzic, *Specification by Example*](https://gojko.net/books/specification-by-example/)
- [Specification by Example, 10 years later](https://gojko.net/2020/03/17/sbe-10-years.html)
- [Ken Segall, *Insanely Simple* — os 10 elementos](https://www.danielscrivner.com/insanely-simple-the-obsession-that-drives-steve-jobs-and-apples-success-by-ken-segall/)
- [Ken Segall — livros](https://kensegall.com/books/)
- [John Maeda, *The Laws of Simplicity*](https://mitpress.mit.edu/9780262539470/the-laws-of-simplicity/)
- [The Laws of Simplicity — resumo](https://readingraphics.com/book-summary-the-laws-of-simplicity/)
- [Shape Up — Find the Elements (breadboarding, fat marker)](https://basecamp.com/shapeup/1.3-chapter-04)
- [Shape Up — Write the Pitch](https://basecamp.com/shapeup/1.5-chapter-06)
- [Shape Up — livro completo](https://basecamp.com/shapeup)
- [Google Technical Writing One](https://developers.google.com/tech-writing/one)
- [Google — Active voice vs. passive voice](https://developers.google.com/tech-writing/one/active-voice)
- [Amazon writing culture — PRFAQ](https://www.theprfaq.com/articles/amazon-writing-culture)
- [Working Backwards — 10 insights](https://www.agile-academy.com/en/agile-leader/the-10-important-insights-from-working-backwards-by-colin-bryar/)
- [GitHub Spec Kit — documentação](https://github.github.com/spec-kit/)
- [Spec-Driven Development with AI: 2026 guide to GitHub Spec Kit](https://www.fundesk.io/spec-driven-development-github-spec-kit-guide)
