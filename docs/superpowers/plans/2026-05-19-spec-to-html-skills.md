# Família de skills `spec-to-html` — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Substituir a skill monolítica `contrato-prototipo` do spec-kit por uma família `spec-to-html` — 1 orquestradora + 4 sub-skills de fase — e versionar o design system EloGroup como ativo do kit.

**Architecture:** Cada sub-skill é um diretório `spec-kit/skills/spec-to-html-<fase>/` com um `SKILL.md` (frontmatter `name`+`description`). A orquestradora `spec-to-html/SKILL.md` descreve o fluxo das 4 fases. O design system vira `spec-kit/assets/elogroup-design-system/`. README do spec-kit, README do `cobranca-prototipo` e a memória `project_spec_kit.md` são atualizados.

**Tech Stack:** Markdown (skills), CSS (design system copiado), Git.

**Nota sobre commits:** o CLAUDE.md do usuário proíbe commit sem pedido explícito. Os passos de commit abaixo só devem rodar após o usuário autorizar. Em execução subagent-driven, pedir autorização uma vez antes do primeiro commit.

---

## File Structure

- Create: `spec-kit/assets/elogroup-design-system/tokens.css` — token CSS EloGroup (cópia)
- Create: `spec-kit/assets/elogroup-design-system/components.css` — componentes EloGroup (cópia)
- Create: `spec-kit/assets/elogroup-design-system/screens.css` — estilos de tela EloGroup (cópia)
- Create: `spec-kit/skills/spec-to-html/SKILL.md` — orquestradora/índice
- Create: `spec-kit/skills/spec-to-html-plano/SKILL.md` — fase plano
- Create: `spec-kit/skills/spec-to-html-scaffold/SKILL.md` — fase scaffold
- Create: `spec-kit/skills/spec-to-html-telas/SKILL.md` — fase telas
- Create: `spec-kit/skills/spec-to-html-build/SKILL.md` — fase build
- Delete: `spec-kit/skills/contrato-prototipo/` — skill monolítica substituída
- Modify: `spec-kit/README.md` — contagem 16→20, tabela contrato 6→5, nova subseção, passo de fluxo
- Modify: `cobranca-prototipo/README.md` — refletir `index.html` autossuficiente e nome da skill
- Modify: `/home/coder/.claude/projects/-home-coder/memory/project_spec_kit.md` — 16→20 skills, nova família

Caminhos absolutos: spec-kit = `/home/coder/projects/spec-kit`, cobranca-prototipo = `/home/coder/projects/cobranca-prototipo`.

---

## Task 1: Versionar o design system EloGroup como ativo do kit

**Files:**
- Create: `spec-kit/assets/elogroup-design-system/tokens.css`
- Create: `spec-kit/assets/elogroup-design-system/components.css`
- Create: `spec-kit/assets/elogroup-design-system/screens.css`

- [ ] **Step 1: Copiar os 3 CSS canônicos do design system**

Os 3 arquivos são a cópia limpa do design system EloGroup já presente em `cobranca-prototipo/styles/`. NÃO copiar `prototipo.css` (esse é específico do protótipo, gerado pelo scaffold).

Run:
```bash
mkdir -p /home/coder/projects/spec-kit/assets/elogroup-design-system
cp /home/coder/projects/cobranca-prototipo/styles/tokens.css \
   /home/coder/projects/cobranca-prototipo/styles/components.css \
   /home/coder/projects/cobranca-prototipo/styles/screens.css \
   /home/coder/projects/spec-kit/assets/elogroup-design-system/
```

- [ ] **Step 2: Verificar que os 3 arquivos foram copiados byte a byte**

Run:
```bash
for f in tokens components screens; do
  diff /home/coder/projects/cobranca-prototipo/styles/$f.css \
       /home/coder/projects/spec-kit/assets/elogroup-design-system/$f.css \
    && echo "$f.css OK"
done
```
Expected: `tokens.css OK`, `components.css OK`, `screens.css OK` — sem diffs.

- [ ] **Step 3: Commit**

```bash
cd /home/coder/projects/spec-kit
git add assets/elogroup-design-system/
git commit -m "feat: versiona design system EloGroup como ativo do kit"
```

---

## Task 2: Criar `spec-to-html-plano/SKILL.md`

**Files:**
- Create: `spec-kit/skills/spec-to-html-plano/SKILL.md`

- [ ] **Step 1: Criar o diretório e o SKILL.md**

Criar `/home/coder/projects/spec-kit/skills/spec-to-html-plano/SKILL.md` com este conteúdo exato:

```markdown
---
name: spec-to-html-plano
description: Use quando o usuário quer iniciar um protótipo HTML navegável de um produto a partir da Camada de Contrato — fase de plano: cria o repo do protótipo e seleciona o conjunto 80/20 de telas.
---

# spec-to-html-plano

Primeira fase da geração de um protótipo HTML navegável a partir da Camada de
Contrato de um wiki wikiLLM. Cria o repositório do protótipo e decide **quais telas
prototipar** — o recorte 80/20 da jornada — emitindo a tabela de telas que as fases
seguintes consomem.

Faz parte da família `spec-to-html` (ver a skill `spec-to-html` para o fluxo
completo). É a fase que abre o primeiro checkpoint: a tabela de telas deve ser
validada pelo usuário antes de construir qualquer coisa.

## Quando usar
Quando o usuário pede um protótipo navegável de um produto e a Camada de Contrato já
existe no wiki. Sempre a primeira das skills `spec-to-html-*` a rodar.

## Entrada
- A Camada de Contrato do wiki: `refined/contracts/<feature>/06-telas-fluxos.md` por
  feature e o catálogo `refined/contracts/_componentes.md`.
- A Camada de Intenção (`refined/intencao/`) para conhecer as personas e priorizar.

## Processo
1. Criar o repositório do protótipo num diretório separado do wiki —
   `<produto>-prototipo/`. Rodar `git init`, criar `.gitignore` e um `README.md`
   stub de uma linha (o `spec-to-html-build` finaliza o README depois).
   Opcionalmente registrar `docs/spec-prototipo-v0.md` com escopo e decisões fixadas.
2. Ler os `06-telas-fluxos.md` das features e as personas da Camada de Intenção.
3. Selecionar o conjunto 80/20 de telas — ~10-12 telas que cobrem a maior parte do
   valor. Priorizar a jornada da persona primária de ponta a ponta; incluir telas de
   setup e pontes entre personas só quando necessárias para a jornada fazer sentido.
4. Emitir a tabela de telas: uma linha por tela, colunas `id` · tela · persona ·
   feature-fonte. O `id` segue o padrão `tela-<slug>`.
5. **Checkpoint:** apresentar a tabela ao usuário e aguardar validação antes de
   passar para `spec-to-html-scaffold`.

## Saída
- O repositório `<produto>-prototipo/` inicializado (git, `.gitignore`, README stub,
  `docs/` opcional).
- A tabela de telas validada — entrada das fases `scaffold` e `telas`.
```

- [ ] **Step 2: Verificar o frontmatter**

Run:
```bash
head -4 /home/coder/projects/spec-kit/skills/spec-to-html-plano/SKILL.md
```
Expected: bloco de frontmatter com `name: spec-to-html-plano` e uma linha `description:`.

- [ ] **Step 3: Commit**

```bash
cd /home/coder/projects/spec-kit
git add skills/spec-to-html-plano/
git commit -m "feat: skill spec-to-html-plano"
```

---

## Task 3: Criar `spec-to-html-scaffold/SKILL.md`

**Files:**
- Create: `spec-kit/skills/spec-to-html-scaffold/SKILL.md`

- [ ] **Step 1: Criar o diretório e o SKILL.md**

Criar `/home/coder/projects/spec-kit/skills/spec-to-html-scaffold/SKILL.md` com este conteúdo exato:

```markdown
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
```

- [ ] **Step 2: Verificar o frontmatter**

Run:
```bash
head -4 /home/coder/projects/spec-kit/skills/spec-to-html-scaffold/SKILL.md
```
Expected: frontmatter com `name: spec-to-html-scaffold` e linha `description:`.

- [ ] **Step 3: Commit**

```bash
cd /home/coder/projects/spec-kit
git add skills/spec-to-html-scaffold/
git commit -m "feat: skill spec-to-html-scaffold"
```

---

## Task 4: Criar `spec-to-html-telas/SKILL.md`

**Files:**
- Create: `spec-kit/skills/spec-to-html-telas/SKILL.md`

- [ ] **Step 1: Criar o diretório e o SKILL.md**

Criar `/home/coder/projects/spec-kit/skills/spec-to-html-telas/SKILL.md` com este conteúdo exato:

```markdown
---
name: spec-to-html-telas
description: Use na fase de telas de um protótipo HTML navegável — gera um partial screens/NN-nome.html por tela da tabela validada, a partir do bloco de telas detalhadas da Camada de Contrato.
---

# spec-to-html-telas

Terceira fase da geração de um protótipo HTML navegável. Gera **uma tela por
partial** em `screens/`, a partir da Camada de Contrato.

Faz parte da família `spec-to-html`. Roda depois de `spec-to-html-scaffold` e antes
de `spec-to-html-build`. Abre o segundo checkpoint: as telas devem ser validadas
pelo usuário antes do build final.

## Quando usar
Depois que `spec-to-html-scaffold` escreveu o esqueleto do protótipo.

## Entrada
- A tabela de telas validada em `spec-to-html-plano`.
- Por tela, o bloco `## B. Telas detalhadas` do `06-telas-fluxos.md` da feature-fonte.
- O catálogo `refined/contracts/_componentes.md` para os blocos de UI referenciados.

## Processo
1. Para cada linha da tabela de telas, criar `screens/NN-nome.html` — `NN` é a ordem
   da tela na navegação (`01`, `02`, …).
2. Cada tela é uma
   `<section class="screen" id="tela-x" data-title="..." data-grupo="...">`,
   construída a partir do bloco `## B. Telas detalhadas` da feature-fonte: objetivo,
   conteúdo, ações, estados, navegação e blocos referenciados (puxados de
   `_componentes.md`).
3. Convenções de markup:
   - navegação entre telas: `onclick="show('tela-x')"` em cards, botões e links;
   - abas: `.tabs` com botões `.tab` + `.tab-panel`, acionadas por `switchTab`;
   - modais: `.popup-overlay` / `.popup-box`, abertos/fechados por
     `openPopup`/`closePopup`;
   - dados de mock: pontos com `data-render="nomeDaFuncao"`, renderizados por
     `initMockData`.
4. **Checkpoint:** apresentar as telas ao usuário (rodando `build.py` para uma
   prévia, se útil) e aguardar validação antes de `spec-to-html-build`.

## Saída
`screens/NN-nome.html` — um partial por tela da tabela, cada um uma
`<section class="screen">`.
```

- [ ] **Step 2: Verificar o frontmatter**

Run:
```bash
head -4 /home/coder/projects/spec-kit/skills/spec-to-html-telas/SKILL.md
```
Expected: frontmatter com `name: spec-to-html-telas` e linha `description:`.

- [ ] **Step 3: Commit**

```bash
cd /home/coder/projects/spec-kit
git add skills/spec-to-html-telas/
git commit -m "feat: skill spec-to-html-telas"
```

---

## Task 5: Criar `spec-to-html-build/SKILL.md`

**Files:**
- Create: `spec-kit/skills/spec-to-html-build/SKILL.md`

- [ ] **Step 1: Criar o diretório e o SKILL.md**

Criar `/home/coder/projects/spec-kit/skills/spec-to-html-build/SKILL.md` com este conteúdo exato:

```markdown
---
name: spec-to-html-build
description: Use na fase de build de um protótipo HTML navegável — roda build.py para montar o index.html autossuficiente (arquivo único), finaliza o README e verifica o protótipo.
---

# spec-to-html-build

Quarta e última fase da geração de um protótipo HTML navegável. Monta o protótipo
num **arquivo único** autossuficiente, finaliza a documentação e verifica que tudo
funciona.

Faz parte da família `spec-to-html`. Roda depois de `spec-to-html-telas` (com as
telas já validadas).

## Quando usar
Depois que `spec-to-html-telas` gerou as telas e elas foram validadas.

## Entrada
O repositório do protótipo completo: `shell.html`, `build.py`, `styles/`, `js/`,
`screens/*.html`.

## Processo
1. Rodar `python3 build.py` para gerar `index.html`. O `build.py` (escrito pelo
   `spec-to-html-scaffold`) embute o CSS e o JS locais inline — o `index.html`
   resultante é autossuficiente: abre sem servidor, sem referências a `styles/` ou
   `js/`. Só as fontes (Google Fonts / Material Symbols) ficam via CDN.
2. Finalizar o `README.md` do repo: o que é o protótipo, como abrir (duplo-clique no
   `index.html`, sem servidor), a tabela das telas, como reconstruir (`build.py`), o
   design system e a dependência de CDN das fontes.
3. Verificar o protótipo abrindo `index.html` sem servidor:
   - a tela inicial aparece;
   - todas as telas da tabela estão presentes;
   - o dev-nav salta para qualquer tela;
   - os links entre telas (`show()`) funcionam;
   - não há erro óbvio de console.

## Saída
O protótipo navegável pronto — `index.html` autossuficiente, que pode ser baixado e
compartilhado como um único arquivo, mais o `README.md` finalizado.
```

- [ ] **Step 2: Verificar o frontmatter**

Run:
```bash
head -4 /home/coder/projects/spec-kit/skills/spec-to-html-build/SKILL.md
```
Expected: frontmatter com `name: spec-to-html-build` e linha `description:`.

- [ ] **Step 3: Commit**

```bash
cd /home/coder/projects/spec-kit
git add skills/spec-to-html-build/
git commit -m "feat: skill spec-to-html-build"
```

---

## Task 6: Criar `spec-to-html/SKILL.md` (orquestradora)

**Files:**
- Create: `spec-kit/skills/spec-to-html/SKILL.md`

- [ ] **Step 1: Criar o diretório e o SKILL.md**

Criar `/home/coder/projects/spec-kit/skills/spec-to-html/SKILL.md` com este conteúdo exato:

````markdown
---
name: spec-to-html
description: Use quando o usuário quer gerar um protótipo HTML navegável (sem backend) das telas de um produto a partir da Camada de Contrato de um wiki wikiLLM, no design system EloGroup. Skill-índice da família spec-to-html.
---

# spec-to-html

Gera um **protótipo HTML navegável** — telas estáticas, sem backend, montadas num
arquivo único que abre com duplo-clique — a partir da Camada de Contrato de um wiki
wikiLLM, no design system EloGroup.

Responde à pergunta *Como ficam, na prática, as telas que a spec descreve?* — dá
forma visual e navegável à Camada de Contrato para validação com usuários e
stakeholders, sem escrever um produto de verdade.

Esta é a **skill-índice** da família `spec-to-html`. Ela não gera artefato: orienta
o uso das quatro sub-skills de fase, na ordem, com os dois checkpoints de revisão.

## Quando usar
Quando o usuário pede um protótipo navegável, mockup clicável ou demo de telas de um
produto — depois que a Camada de Contrato já existe no wiki (em especial os
`06-telas-fluxos.md` das features e o catálogo `_componentes.md`). Não usar antes de
a Camada de Contrato estar escrita: o protótipo é uma renderização dela, não a fonte.

## As quatro fases
Rodar as sub-skills nesta ordem:

1. **`spec-to-html-plano`** — cria o repo do protótipo e seleciona o conjunto 80/20
   de telas, emitindo a tabela de telas. **⟵ Checkpoint:** o usuário valida a tabela
   antes de construir.
2. **`spec-to-html-scaffold`** — copia o design system EloGroup e escreve o esqueleto
   invariável (`prototipo.css`, `shell.html`, `build.py`, `mock-data.js`, `app.js`).
3. **`spec-to-html-telas`** — gera um partial `screens/NN-nome.html` por tela da
   tabela. **⟵ Checkpoint:** o usuário valida as telas antes do build.
4. **`spec-to-html-build`** — roda `build.py`, monta o `index.html` autossuficiente
   (arquivo único), finaliza o README e verifica o protótipo.

## Exemplo de referência
O protótipo `cobranca-prototipo` (`/home/coder/projects/cobranca-prototipo/`) é o
exemplo de referência vivo do que esta família produz — consultar antes de gerar.

## Saída
Um repo de protótipo navegável, no design system EloGroup, cujo `index.html` é
autossuficiente (CSS e JS embutidos inline; só fontes via CDN) e pode ser baixado e
compartilhado como um único arquivo:

```
<produto>-prototipo/
  index.html              # GERADO por build.py — autossuficiente, arquivo único
  build.py                # monta index.html: shell + screens + CSS/JS inline
  shell.html              # casca: topbar + dev-nav vazio + <main id="screens"> + scripts
  styles/
    tokens.css  components.css  screens.css   # design system EloGroup (copiados)
    prototipo.css                              # estilos só do protótipo
  js/
    mock-data.js   # window.MOCK
    app.js         # IIFE: show, switchTab, openPopup/closePopup, dev-nav, initMockData
  screens/
    01-....html ... NN-....html   # uma <section class="screen"> por tela
  docs/
    spec-prototipo-v0.md  # opcional — escopo e decisões
  README.md
```
````

- [ ] **Step 2: Verificar o frontmatter**

Run:
```bash
head -4 /home/coder/projects/spec-kit/skills/spec-to-html/SKILL.md
```
Expected: frontmatter com `name: spec-to-html` e linha `description:`.

- [ ] **Step 3: Commit**

```bash
cd /home/coder/projects/spec-kit
git add skills/spec-to-html/
git commit -m "feat: skill orquestradora spec-to-html"
```

---

## Task 7: Remover a skill monolítica `contrato-prototipo`

**Files:**
- Delete: `spec-kit/skills/contrato-prototipo/`

- [ ] **Step 1: Remover o diretório**

Run:
```bash
cd /home/coder/projects/spec-kit
git rm -r skills/contrato-prototipo
```
Expected: `rm 'skills/contrato-prototipo/SKILL.md'`.

- [ ] **Step 2: Verificar que as 5 skills novas existem e a antiga não**

Run:
```bash
ls /home/coder/projects/spec-kit/skills/ | grep -E 'prototipo|spec-to-html'
```
Expected: `spec-to-html`, `spec-to-html-build`, `spec-to-html-plano`, `spec-to-html-scaffold`, `spec-to-html-telas` — e NENHUM `contrato-prototipo`.

- [ ] **Step 3: Commit**

```bash
cd /home/coder/projects/spec-kit
git commit -m "refactor: remove skill monolítica contrato-prototipo (substituída por spec-to-html-*)"
```

---

## Task 8: Atualizar o README do spec-kit

**Files:**
- Modify: `spec-kit/README.md`

- [ ] **Step 1: Atualizar a contagem de skills (linha ~31)**

Substituir, em `/home/coder/projects/spec-kit/README.md`:

```
- **Um agente que suporte skills** — p.ex. Claude Code. As 16 skills deste kit são
  acionadas pelo agente conforme a tarefa.
```
por:
```
- **Um agente que suporte skills** — p.ex. Claude Code. As 20 skills deste kit são
  acionadas pelo agente conforme a tarefa.
```

- [ ] **Step 2: Adicionar passo de protótipo ao "Fluxo de uso ponta a ponta"**

Substituir o item 6 atual:
```
6. **Manutenção contínua** — `spec-lint` para o health-check (links quebrados, órfãs,
   lacunas) e `spec-wiki` para integrar fontes novas (`ingest`) ou consultar o wiki
   (`query`).
```
por:
```
6. **`spec-to-html`** — gerar um protótipo HTML navegável das telas a partir da
   Camada de Contrato (opcional, depois que ela existe). Roda as 4 sub-skills de
   fase: `plano`, `scaffold`, `telas`, `build`.
7. **Manutenção contínua** — `spec-lint` para o health-check (links quebrados,
   órfãs, lacunas) e `spec-wiki` para integrar fontes novas (`ingest`) ou consultar
   o wiki (`query`).
```

- [ ] **Step 3: Corrigir a tabela "Camada de Contrato" (6→5, remove contrato-prototipo)**

Substituir o bloco:
```
### Camada de Contrato (6)

| Skill | O que faz |
| --- | --- |
| `contrato-telas-fluxos` | Telas e fluxos de cada feature. |
| `contrato-historias` | Histórias de usuário e critérios de aceite por feature. |
| `contrato-requisitos` | Requisitos funcionais e não-funcionais por feature. |
| `contrato-dados` | Modelo de dados e API por feature. |
| `contrato-blueprint` | Blueprint product-level — features na cadeia de valor. |
| `contrato-prototipo` | Protótipo HTML navegável (sem backend) das telas, no design system EloGroup. |
```
por:
```
### Camada de Contrato (5)

| Skill | O que faz |
| --- | --- |
| `contrato-telas-fluxos` | Telas e fluxos de cada feature. |
| `contrato-historias` | Histórias de usuário e critérios de aceite por feature. |
| `contrato-requisitos` | Requisitos funcionais e não-funcionais por feature. |
| `contrato-dados` | Modelo de dados e API por feature. |
| `contrato-blueprint` | Blueprint product-level — features na cadeia de valor. |
```

- [ ] **Step 4: Adicionar a subseção "Geração de protótipo (5)"**

Inserir, logo após a tabela "### Operacionais (5)" e antes de "## Scripts", este bloco:

```
### Geração de protótipo (5)

Família `spec-to-html` — transforma a Camada de Contrato num protótipo HTML
navegável (sem backend), que abre com duplo-clique como arquivo único.

| Skill | O que faz |
| --- | --- |
| `spec-to-html` | Orquestradora/índice — descreve as 4 fases e os 2 checkpoints. |
| `spec-to-html-plano` | Cria o repo do protótipo e seleciona o conjunto 80/20 de telas. |
| `spec-to-html-scaffold` | Copia o design system EloGroup e escreve o esqueleto invariável. |
| `spec-to-html-telas` | Gera um partial `screens/NN-*.html` por tela da tabela. |
| `spec-to-html-build` | Monta o `index.html` autossuficiente, finaliza o README e verifica. |
```

- [ ] **Step 5: Verificar as mudanças**

Run:
```bash
cd /home/coder/projects/spec-kit
grep -n '20 skills\|Camada de Contrato (5)\|Geração de protótipo (5)\|spec-to-html`' README.md
```
Expected: linhas correspondentes a "20 skills", "Camada de Contrato (5)", "Geração de protótipo (5)" e o passo 6 do fluxo.

- [ ] **Step 6: Commit**

```bash
cd /home/coder/projects/spec-kit
git add README.md
git commit -m "docs: README reflete família spec-to-html (16→20 skills)"
```

---

## Task 9: Corrigir o README do `cobranca-prototipo`

**Files:**
- Modify: `cobranca-prototipo/README.md`

- [ ] **Step 1: Corrigir a descrição do `index.html` no bloco "Estrutura do repositório"**

Substituir, em `/home/coder/projects/cobranca-prototipo/README.md`, a linha:
```
  index.html                             # GERADO — não editar; resultado de build.py
```
por:
```
  index.html                             # GERADO — autossuficiente (CSS+JS inline); não editar
```

- [ ] **Step 2: Corrigir a nota após o bloco de estrutura**

Substituir:
```
`index.html` é gerado automaticamente. Não edite manualmente — edite os partials em `screens/` e rode `python3 build.py`.
```
por:
```
`index.html` é gerado automaticamente e é **autossuficiente** — `build.py` embute o CSS de `styles/` e o JS de `js/` inline, então o arquivo abre sozinho e pode ser baixado/compartilhado isoladamente. Só as fontes (Google Fonts / Material Symbols) ficam via CDN. Não edite `index.html` manualmente — edite os partials em `screens/` (ou os CSS/JS) e rode `python3 build.py`.
```

- [ ] **Step 3: Corrigir a seção "Como reconstruir (build.py)"**

Substituir:
```
Script concatena `shell.html` + `screens/*.html` (ordem alfabética) em `index.html`. 
```
por:
```
Script concatena `shell.html` + `screens/*.html` (ordem alfabética) e embute o CSS de `styles/` e o JS de `js/` inline, gerando um `index.html` autossuficiente.
```

- [ ] **Step 4: Atualizar a referência à skill no fim do arquivo**

Substituir:
```
Este protótipo é produto direto da **Camada de Contrato** do wiki `knowledge_cob` (features de cobrança tributária). A skill `contrato-prototipo` (no repo `spec-kit`) replica esse processo: lê a Camada de Contrato de uma feature, gera as 11 telas usando o design system EloGroup, e monta o `build.py` + `shell.html` automaticamente.
```
por:
```
Este protótipo é produto direto da **Camada de Contrato** do wiki `knowledge_cob` (features de cobrança tributária). A família de skills `spec-to-html` (no repo `spec-kit`) replica esse processo em 4 fases — `plano`, `scaffold`, `telas`, `build`: lê a Camada de Contrato, seleciona o recorte 80/20 de telas, escreve o esqueleto no design system EloGroup e monta o `index.html` autossuficiente. Este repo é o exemplo de referência vivo dessa família.
```

- [ ] **Step 5: Verificar as mudanças**

Run:
```bash
cd /home/coder/projects/cobranca-prototipo
grep -n 'autossuficiente\|spec-to-html\|contrato-prototipo' README.md
```
Expected: ocorrências de "autossuficiente" e "spec-to-html"; NENHUMA ocorrência de "contrato-prototipo".

- [ ] **Step 6: Commit**

```bash
cd /home/coder/projects/cobranca-prototipo
git add README.md
git commit -m "docs: README reflete index.html autossuficiente e família spec-to-html"
```

---

## Task 10: Atualizar a memória `project_spec_kit.md`

**Files:**
- Modify: `/home/coder/.claude/projects/-home-coder/memory/project_spec_kit.md`

- [ ] **Step 1: Atualizar a contagem e a composição das skills**

Substituir, no parágrafo do `spec-kit`:
```
**16 skills** modulares (5 Intenção + 6 Contrato, incl. `contrato-prototipo` + 5 operacionais)
```
por:
```
**20 skills** modulares (5 Intenção + 5 Contrato + 5 operacionais + família `spec-to-html` de 5: orquestradora + plano/scaffold/telas/build)
```

- [ ] **Step 2: Atualizar a frase sobre a skill que replica o protótipo**

Substituir, no parágrafo do `cobranca-prototipo`:
```
A skill `contrato-prototipo` do spec-kit replica esse processo.
```
por:
```
A família de skills `spec-to-html` do spec-kit replica esse processo em 4 fases, com `index.html` autossuficiente (arquivo único) como saída.
```

- [ ] **Step 3: Verificar**

Run:
```bash
grep -n '20 skills\|spec-to-html' /home/coder/.claude/projects/-home-coder/memory/project_spec_kit.md
```
Expected: linhas com "20 skills" e "spec-to-html".

- [ ] **Step 4: (sem commit)** A memória não é versionada — nada a commitar.

---

## Self-Review

**Spec coverage:**
- "5 skills `spec-to-html`" → Tasks 2-6. ✓
- "Decomposição por fase / 2 checkpoints" → checkpoints descritos nos SKILL.md de `plano` e `telas` (Tasks 2, 4). ✓
- "`contrato-prototipo` removida" → Task 7. ✓
- "Design system determinístico versionado no kit" → Task 1; consumido pelo `scaffold` (Task 3). ✓
- "Build de arquivo único" → descrito no `scaffold` (passo 4) e no `build` (passo 1). ✓
- "README do spec-kit: 16→20, tabela 6→5, nova subseção, passo de fluxo" → Task 8. ✓
- "Exemplo de referência: corrigir README do cobranca-prototipo" → Task 9. ✓
- "Memória project_spec_kit.md atualizada" → Task 10. ✓
- "Design doc commitado no repo do spec-kit" → o design doc já está em `spec-kit/docs/superpowers/specs/`; será incluído num commit (autorização do usuário).

**Placeholder scan:** sem "TBD"/"TODO"/"implementar depois". Conteúdo completo de cada SKILL.md embutido. ✓

**Type consistency:** nomes de skill (`spec-to-html`, `spec-to-html-plano/-scaffold/-telas/-build`) e funções JS (`show`, `switchTab`, `openPopup`/`closePopup`, `initMockData`) usados de forma idêntica em todas as tasks. ✓
