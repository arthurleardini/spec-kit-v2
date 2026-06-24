---
name: spec-to-html-telas
description: Use na fase de telas de um protótipo HTML navegável — gera um partial screens/NN-nome.html por tela da tabela validada, a partir do bloco de telas detalhadas da Camada de Requisitos.
---

# spec-to-html-telas

Terceira fase da geração de um protótipo HTML navegável. Gera **uma tela por
partial** em `screens/`, a partir da Camada de Requisitos.

Faz parte da família `spec-to-html`. Roda depois de `spec-to-html-scaffold` e antes
de `spec-to-html-build`. Abre o segundo checkpoint: as telas devem ser validadas
pelo usuário antes do build final.

## Quando usar
Depois que `spec-to-html-scaffold` escreveu o esqueleto do protótipo.

## Entrada
- A tabela de telas validada em `spec-to-html-plano`.
- Por tela, a subseção `### 1.2 Telas detalhadas` do Cap. 1 do `Requisitos/<feature>.md` da feature-fonte.
- O ponteiro `refined/componentes.md` para os componentes genéricos referenciados (campo **Componentes:** + bloco ` ```wireframe ` de cada tela).

## Processo
1. Para cada linha da tabela de telas, criar `screens/NN-nome.html` — `NN` é a ordem
   da tela na navegação (`01`, `02`, …).
2. Cada tela é uma
   `<section class="screen" id="tela-x" data-title="..." data-grupo="...">`,
   construída a partir da subseção `### 1.2 Telas detalhadas` da feature-fonte: objetivo,
   conteúdo, ações, estados, navegação, o bloco ` ```wireframe ` e os componentes
   referenciados pelo nome genérico (campo **Componentes:**, vocabulário em
   `componentes.md`).
3. **Densidade e fluxo (Princípios transversais em `spec-to-html`) — aplicar em cada tela:**
   - **Abrir com dado, não com texto.** O cabeçalho é `eyebrow` + `<h1>` curto; **sem
     subtítulo que narra a tela** ("parece slide"), sem banner de ensino, sem `RN`/`RNF`
     escrita como frase. Liderar com a tabela/KPIs/board. IDs de regra só como chip ou
     `title` (tooltip).
   - **Texto só quando é status acionável ou decisão do momento.** Cortar ajuda
     redundante, nota de jornada e adjetivo vazio.
   - **Configuração não entra em tela operacional** — parâmetros ficam nas telas do grupo
     Configurações (conforme a coluna "área" da tabela do plano).
   - **Master-detail é drawer lateral, não nova tela:** clicar numa linha abre
     `openPopup('<id>')` num `.popup-overlay.popup-overlay--right` com o detalhe; a lista
     não some. Só usar `show('outra-tela')` para troca real de área.
   - **Nada de UI que promete e não cumpre:** botão/ícone sem comportamento é removido.
4. Convenções de markup:
   - navegação entre telas: `onclick="show('tela-x')"` em cards, botões e links;
   - **linha/card clicável é operável por teclado:** além do `onclick`, pôr
     `role="button" tabindex="0"` e disparar a ação no `keydown` de Enter/Espaço;
   - abas: `.tabs` com botões `.tab` + `.tab-panel`, acionadas por `switchTab` (ARIA e
     setas já vêm do `wireTabs` do scaffold);
   - modais e drawers: `.popup-overlay` (central) ou `.popup-overlay--right` (lateral),
     abertos/fechados por `openPopup`/`closePopup` (foco/trap/Esc já embutidos);
   - **ação auditável/irreversível** (publicar versão imutável, registrar ato auditado,
     ato com efeito jurídico): confirmar via `confirmAction('<popup>', {requireText:true})`
     e usar o **atributo `disabled`** (não classe) em botão bloqueado;
   - dados de mock: pontos com `data-render="nomeDaFuncao"`, renderizados por
     `initMockData`.
5. **Checkpoint:** apresentar as telas ao usuário (rodando `build.py` para uma
   prévia, se útil) e aguardar validação antes de `spec-to-html-build`. Conferir a
   densidade (cada tela abre com dado) e o fluxo (config fora do operacional, detalhe em
   drawer) junto.

## Saída
`screens/NN-nome.html` — um partial por tela da tabela, cada um uma
`<section class="screen">`.
