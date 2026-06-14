# Design — Família de skills `spec-to-html`

**Data:** 2026-05-19
**Repo:** `spec-kit`
**Status:** aprovado para planejamento

## Problema

O spec-kit tem hoje uma skill monolítica, `contrato-prototipo` — 8 passos que vão
de "criar repo" até "montar e verificar" o protótipo HTML navegável. A skill é
grande demais para o agente seguir com fidelidade, não oferece pontos de revisão
intermediários, não permite reaproveitar fases isoladas e destoa do resto do kit,
que é decomposto em famílias de skills focadas (5 `intencao-*`, 6 `contrato-*`,
5 `spec-*`), cada uma produzindo um artefato.

## Objetivo

Substituir a `contrato-prototipo` monolítica por uma **família `spec-to-html`** —
uma skill orquestradora/índice e quatro sub-skills de fase, com dois checkpoints de
revisão. Cada sub-skill produz um artefato revisável e pode ser acionada isolada.

## Decisões fixadas

- **5 skills**: `spec-to-html` (orquestradora) + `spec-to-html-plano`,
  `spec-to-html-scaffold`, `spec-to-html-telas`, `spec-to-html-build`.
- **Decomposição por fase** do ciclo de vida, não por artefato avulso.
- **Dois checkpoints**: após `plano` (usuário valida a lista de telas) e após
  `telas` (usuário valida as telas) — antes de avançar.
- **`contrato-prototipo` é removida**; seu conteúdo se redistribui pelas 5 skills.
- **Nomenclatura** `spec-to-html-*` (kebab-case, prefixo herdado da orquestradora).
- **Design system EloGroup é determinístico** — ativo fixo versionado no próprio
  spec-kit; o `scaffold` o copia verbatim, não improvisa nem regenera CSS.
- **Build de arquivo único** — o `build.py` gerado embute CSS e JS inline; o
  `index.html` final é autossuficiente (só fontes via CDN), para baixar e
  compartilhar como um arquivo.

## Arquitetura

```
spec-kit/skills/
  spec-to-html/            orquestradora/índice — não gera artefato
  spec-to-html-plano/      repo + seleção 80/20 + tabela de telas   ⟵ CHECKPOINT
  spec-to-html-scaffold/   design system + prototipo.css + shell.html
                           + build.py + mock-data.js + app.js
  spec-to-html-telas/      screens/NN-*.html (uma <section> por tela) ⟵ CHECKPOINT
  spec-to-html-build/      monta index.html (arquivo único) + README + verifica
```

Total do kit: 16 → **20 skills** (família `contrato-*` cai de 6 p/ 5; +5 da nova
família).

## As skills

### `spec-to-html` — orquestradora/índice

Porta de entrada quando o usuário pede um protótipo navegável. Descreve as 4 fases,
os 2 checkpoints e quando usar; aponta `cobranca-prototipo` como exemplo de
referência vivo. Não gera artefato e não duplica os passos detalhados das
sub-skills. Análoga ao papel que o README do kit cumpre para as outras famílias,
mas materializada como skill por ser a porta de entrada da fase de protótipo.

### `spec-to-html-plano` — seleção e plano

- **Entrada:** Camada de Contrato do wiki (`contracts/<feature>/06-telas-fluxos.md`,
  `contracts/_componentes.md`) + Camada de Intenção (personas).
- **Faz:** cria o repo `<produto>-prototipo/` separado (`git init`, `.gitignore`,
  `README.md` stub, `docs/spec-prototipo-v0.md` opcional); seleciona o conjunto
  **80/20** de telas (~10-12) priorizando a jornada da persona primária de ponta a
  ponta; emite a **tabela de telas** (`id · tela · persona · feature-fonte`).
- **Saída:** repo inicializado + tabela de telas.
- **⟵ CHECKPOINT:** o usuário valida a lista de telas antes de construir.

### `spec-to-html-scaffold` — esqueleto invariável

- **Faz:**
  - copia o design system EloGroup de `spec-kit/assets/elogroup-design-system/`
    (`tokens.css`, `components.css`, `screens.css`) para `styles/`, sem editar;
  - escreve `styles/prototipo.css` — só o que **não** vem do design system:
    troca de tela (`.screen`/`.screen.is-active`), dev-nav, padrões de layout do
    protótipo (`.kpi-grid`, `.timeline`, `.master-detail` etc.). Estender o DS é
    permitido; redefinir componentes existentes, não;
  - escreve `shell.html` — casca: `<head>` com fontes + 4 CSS na ordem
    `tokens → components → screens → prototipo`, topbar do DS (sem logo EloGroup
    na UI), `<nav id="dev-nav">` vazio, `<main id="screens"><!--SCREENS--></main>`,
    scripts;
  - escreve `build.py` — concatena `screens/*.html` no marcador `<!--SCREENS-->`
    **e embute CSS e JS inline**, gerando `index.html` autossuficiente;
  - escreve `js/mock-data.js` — `window.MOCK`, uma coleção-array por entidade do
    domínio, dados fictícios plausíveis em pt-BR, IDs cruzados consistentes, zero
    PII;
  - escreve `js/app.js` — IIFE com `show`, `switchTab`, `openPopup`/`closePopup`,
    montagem dinâmica do dev-nav, `initMockData`; defensivo (nada quebra se uma
    tela/painel/função de render ainda não existe).
- **Saída:** tudo menos as telas. Sem checkpoint (boilerplate determinístico).

### `spec-to-html-telas` — as telas

- **Faz:** uma `screens/NN-nome.html` por linha da tabela de telas, construída a
  partir do bloco `## B. Telas detalhadas` do `06-telas-fluxos.md` da feature-fonte
  (objetivo, conteúdo, ações, estados, navegação, blocos referenciados puxados de
  `_componentes.md`). Convenções de markup: navegação via `onclick="show('tela-x')"`;
  abas `.tabs`/`.tab` + `switchTab`; modais `.popup-overlay`/`.popup-box` com
  `openPopup`/`closePopup`; pontos de dados com `data-render="nomeDaFuncao"`.
- **Saída:** `screens/*.html`.
- **⟵ CHECKPOINT:** o usuário valida as telas antes do build final.

### `spec-to-html-build` — montar e entregar

- **Faz:** roda `python3 build.py` → `index.html` autossuficiente (CSS+JS inline,
  só fontes via CDN); finaliza o `README.md`; verifica que o `index.html` abre sem
  servidor, mostra a tela inicial, contém todas as telas da tabela, o dev-nav salta
  para qualquer uma, os links entre telas funcionam e não há erro óbvio de console.
- **Saída:** protótipo navegável pronto para baixar e compartilhar como **um único
  arquivo**.

## Itens transversais

1. **README do spec-kit** — nova subseção "Geração de protótipo (5)" na seção "As
   skills" com a tabela das 5 skills; contagem `16 skills` → `20 skills` em todas as
   menções; passo 7 no "Fluxo de uso ponta a ponta" (após `spec-navigator`, rodar
   `spec-to-html`).
2. **Design system como ativo do kit** — criar
   `spec-kit/assets/elogroup-design-system/` com `tokens.css`, `components.css`,
   `screens.css` copiados de `cobranca-prototipo/styles/` (cópia limpa do DS).
   Fonte única e determinística para o `scaffold`.
3. **Exemplo de referência** — `cobranca-prototipo` segue como exemplo vivo citado
   pelas 5 skills; já está com o `build.py` de arquivo único. Seu `README.md`
   descreve a estrutura de arquivos separados — corrigir para refletir o
   `index.html` autossuficiente.
4. **Memória** — atualizar `project_spec_kit.md`: 16 → 20 skills, nova família
   `spec-to-html-*`, `contrato-prototipo` removida.

## Fora de escopo

- Reescrever as telas do `cobranca-prototipo`.
- Mexer nas skills `contrato-*` de documento de spec.
- Tocar no wiki `knowledge_cob`.

## Critério de aceite

- `spec-kit/skills/contrato-prototipo/` removida; existem os 5 diretórios
  `spec-to-html*` cada um com um `SKILL.md` válido (frontmatter `name` +
  `description`).
- `spec-kit/assets/elogroup-design-system/` contém os 3 CSS canônicos.
- README do spec-kit reflete 20 skills, a nova subseção e o passo 7 do fluxo.
- `project_spec_kit.md` (memória) atualizado.
- Design doc commitado no repo do spec-kit.
