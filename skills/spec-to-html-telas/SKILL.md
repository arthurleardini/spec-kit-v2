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
