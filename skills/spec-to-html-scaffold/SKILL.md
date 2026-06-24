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
2. Escrever `styles/prototipo.css` — apenas o que **não** vem do design system. A
   camada compartilhada é o ponto de alavanca: tudo de a11y/shell aqui propaga a todas
   as telas. Incluir:
   - o mecanismo de troca de tela (`.screen { display:none }` / `.screen.is-active`);
   - **Acessibilidade (baseline):** `:focus-visible` com outline visível; bloco
     `@media (prefers-reduced-motion: reduce)` zerando animações; **override de
     contraste** de qualquer token de texto fraco do design system para ≥ 4.5:1 (ex.:
     `body { --color-text-subtle: <valor mais escuro> }`) — corrige sem editar o
     design system;
   - **Shell por área e responsivo:** sidebar agrupada por área; em telas estreitas
     (`@media (max-width:900px)`) a sidebar vira **drawer off-canvas** (`transform`),
     **nunca `display:none`** — com `.skip-link`, botão hambúrguer (`.nav-toggle`) e
     scrim (`.nav-scrim`);
   - **Drawer lateral** para master-detail, reusando o modal: modificador
     `.popup-overlay--right` que ancora o `.popup-box` como folha à direita (herda
     foco/Esc do `app.js`, sem JS novo);
   - padrões de layout do protótipo (`.kpi-grid`/`.kpi-card`, `.timeline`, gráficos
     simples etc.).
   Estender o design system é permitido; redefinir componentes que já existem
   (`.btn`, `.card`, `.chip`, `.tabs`/`.tab`, `.alert`, tabelas), não. **Não** escrever
   dev-nav.
3. Escrever `shell.html` — a casca: `<head>` com fontes e os 4 CSS na ordem
   `tokens → components → screens → prototipo`; **`.skip-link`** ("Pular para o
   conteúdo") como 1º foco; topbar (nome textual + ícone Material, **sem ícones que não
   fazem nada** — só o que tiver comportamento) com o **hambúrguer** (`#navToggle`);
   **sidebar agrupada pelas áreas da tabela do plano** (um `side__group` por área; só as
   telas marcadas como item de menu entram aqui); `.nav-scrim`;
   `<main id="main-content" tabindex="-1"><div id="screens"><!--SCREENS--></div></main>`;
   `<script>` de `mock-data.js` e `app.js`. **Sem dev-nav.**
4. Escrever `build.py` — monta `index.html` a partir de `shell.html` +
   `screens/*.html` (ordem alfabética, no marcador `<!--SCREENS-->`) **e embute o CSS
   e o JS locais inline**, de modo que o `index.html` gerado seja autossuficiente
   (arquivo único, sem referências a `styles/` ou `js/`; só as fontes ficam via CDN).
5. Escrever `js/mock-data.js` — expõe `window.MOCK`, com uma coleção-array por
   entidade do domínio, dados fictícios plausíveis em pt-BR e IDs cruzados
   consistentes entre coleções. Valores **determinísticos** (sem `Math.random()`, que
   quebra a consistência entre telas). Nunca dados reais nem PII.
6. Escrever `js/app.js` — uma IIFE com o motor de navegação, expondo em `window.*` e já
   com a11y/segurança embutidas (assim toda tela herda de graça):
   - `show(id)` — troca a tela, **move o foco para o título da tela** (leitor de tela) e
     fecha o drawer mobile;
   - `switchTab(btnEl, targetId)` + `wireTabs()` no boot — abas com `role="tablist"`/
     `role="tab"`, `aria-selected`, e navegação por **setas ←/→**;
   - `openPopup(id)` / `closePopup(id)` — marcam `role="dialog"`/`aria-modal`, **movem o
     foco para dentro**, **prendem o Tab** (trap) e **restauram o foco ao gatilho** ao
     fechar; serve tanto para modal central quanto para o drawer `.popup-overlay--right`;
   - keydown global: **Esc** fecha o overlay/drawer aberto;
   - `toggleNav(force)` — abre/fecha a sidebar-drawer no mobile (+ `aria-expanded`);
   - `confirmAction(popupId, {requireText, then})` — **bloqueia a confirmação de ação
     auditável/irreversível enquanto a justificativa estiver vazia** (mensagem inline +
     `aria-invalid`), depois fecha e navega;
   - `initMockData()` — varre `[data-render="fn"]` e chama `window.fn(el, MOCK)`.
   O `app.js` é defensivo (nada quebra se tela/painel/função ainda não existir) e **não
   tem dev-nav** (`buildDevNav` não existe).

## Saída
O esqueleto do protótipo, pronto para receber as telas: `styles/` (4 CSS),
`shell.html`, `build.py`, `js/mock-data.js`, `js/app.js`.
