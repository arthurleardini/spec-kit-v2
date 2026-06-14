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
