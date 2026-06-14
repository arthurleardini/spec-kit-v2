---
name: spec-to-html-scaffold
description: Use na fase de scaffold de um protótipo HTML navegável — copia o design system EloGroup e escreve o esqueleto invariável (prototipo.css, shell.html, build.py, mock-data.js, app.js).
---

# spec-to-html-scaffold

Segunda fase da geração de um protótipo HTML navegável. Escreve o **esqueleto
invariável** do protótipo — tudo que não são as telas em si: design system, estilos
do protótipo, casca, montador e o motor JS.

Faz parte da família `spec-to-html`. Roda depois de `spec-to-html-plano` (com a
tabela de telas já validada) e antes de `spec-to-html-telas`. Não tem checkpoint — é
boilerplate determinístico.

## Quando usar
Depois que `spec-to-html-plano` criou o repo e a tabela de telas foi validada.

## Entrada
- O repositório do protótipo criado por `spec-to-html-plano`.
- A tabela de telas validada (para dimensionar o mock-data).
- O design system EloGroup, versionado em `<spec-kit>/assets/elogroup-design-system/`.

## Processo
1. Copiar o design system EloGroup de `<spec-kit>/assets/elogroup-design-system/`
   (`tokens.css`, `components.css`, `screens.css`) para `styles/` do repo do
   protótipo, **sem editar**. Esse design system é determinístico — não improvisar
   nem regenerar CSS.
2. Escrever `styles/prototipo.css` — apenas o que **não** vem do design system:
   - o mecanismo de troca de tela (`.screen { display:none }` / `.screen.is-active`);
   - o dev-nav (painel fixo de salto entre telas);
   - padrões de layout do protótipo (`.kpi-grid`/`.kpi-card`, `.timeline`,
     `.master-detail`, gráficos simples etc.).
   Estender o design system é permitido; redefinir componentes que já existem
   (`.btn`, `.card`, `.chip`, `.tabs`/`.tab`, `.alert`, tabelas), não.
3. Escrever `shell.html` — a casca: `<head>` com fontes e os 4 CSS na ordem
   `tokens → components → screens → prototipo`; topbar do design system (sem logo
   EloGroup na UI — nome textual + ícone Material); `<nav id="dev-nav"></nav>` vazio;
   `<main id="screens"><!--SCREENS--></main>`; `<script>` de `mock-data.js` e `app.js`.
4. Escrever `build.py` — monta `index.html` a partir de `shell.html` +
   `screens/*.html` (ordem alfabética, no marcador `<!--SCREENS-->`) **e embute o CSS
   e o JS locais inline**, de modo que o `index.html` gerado seja autossuficiente
   (arquivo único, sem referências a `styles/` ou `js/`; só as fontes ficam via CDN).
5. Escrever `js/mock-data.js` — expõe `window.MOCK`, com uma coleção-array por
   entidade do domínio, dados fictícios plausíveis em pt-BR e IDs cruzados
   consistentes entre coleções. Nunca dados reais nem PII.
6. Escrever `js/app.js` — uma IIFE com o motor de navegação, expondo as funções em
   `window.*`: `show(id)`, `switchTab(btnEl, targetId)`, `openPopup(id)` /
   `closePopup(id)`, montagem dinâmica do dev-nav a partir das `.screen` do DOM, e
   `initMockData()` (varre `[data-render="nomeDaFuncao"]` e chama
   `window.nomeDaFuncao(el, MOCK)`). O `app.js` deve ser defensivo: nada quebra se
   uma tela, painel ou função de render ainda não existir.

## Saída
O esqueleto do protótipo, pronto para receber as telas: `styles/` (4 CSS),
`shell.html`, `build.py`, `js/mock-data.js`, `js/app.js`.
