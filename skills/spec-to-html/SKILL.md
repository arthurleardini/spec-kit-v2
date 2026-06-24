---
name: spec-to-html
description: Use quando o usuário quer gerar um protótipo HTML navegável (sem backend) das telas de um produto a partir da Camada de Requisitos de um wiki wikiLLM, no design system EloGroup. Skill-índice da família spec-to-html.
---

# spec-to-html

Gera um **protótipo HTML navegável** — telas estáticas, sem backend, montadas num
arquivo único que abre com duplo-clique — a partir da Camada de Requisitos de um wiki
wikiLLM, no design system EloGroup.

Responde à pergunta *Como ficam, na prática, as telas que a spec descreve?* — dá
forma visual e navegável à Camada de Requisitos para validação com usuários e
stakeholders, sem escrever um produto de verdade.

Esta é a **skill-índice** da família `spec-to-html`. Ela não gera artefato: orienta
o uso das quatro sub-skills de fase, na ordem, com os dois checkpoints de revisão.

## Quando usar
Quando o usuário pede um protótipo navegável, mockup clicável ou demo de telas de um
produto — depois que a Camada de Requisitos já existe no wiki (em especial o Cap. 1,
Telas & Fluxos, dos `Requisitos/<feature>.md` das features e o catálogo `componentes.md`). Não usar antes de
a Camada de Requisitos estar escrita: o protótipo é uma renderização dela, não a fonte.

## Princípios transversais (UX/UI, simplificação, fluxo) — obrigatórios

Valem em todas as fases. Cada sub-skill aplica o subconjunto que lhe cabe; aqui fica a referência única (vêm de iterações reais de protótipo de cobrança).

**Simplificação / densidade — o protótipo é um sistema, não um slide.**
- Cada tela abre com **dado** (tabela, KPIs, board), não com parágrafo. Sem subtítulo que narra a tela, sem banner de ensino explicando o conceito, sem regra (`RN`/`RNF`) escrita como frase. IDs de regra entram como chip ou tooltip, não como texto corrido.
- Manter só texto que é **status acionável** ou **decisão do momento**. Cortar nota de jornada, ajuda redundante e adjetivo vazio.
- Não criar UI que promete e não cumpre (botão que não faz nada, ícone inerte). Em protótipo, isso lê como bug: remover ou tornar honesto.

**Organização do fluxo de informação.**
- Menu por **área**, não um item por tela: poucos grupos (ex.: Carteira · Operação · Analytics · Configurações). Subtelas viram **navegação interna** (clique na linha, drawer, modal), não item de menu.
- **Configuração separada do operacional**: tudo que é parâmetro vai para um grupo Configurações; telas operacionais só operam.
- **Master-detail como drawer lateral**, não nova tela: clicar numa linha abre painel lateral com o detalhe e preserva o contexto da lista.

**Acessibilidade (baseline, na camada compartilhada).**
- Contraste de texto ≥ 4.5:1 (subir tokens fracos via `prototipo.css`); `:focus-visible` visível; `prefers-reduced-motion`; `aria-label` em botão só-ícone.
- Modal com `role="dialog"`/`aria-modal`, foco que entra ao abrir, trap de Tab, Esc fecha, foco volta ao gatilho — centralizado em `openPopup`/`closePopup`.
- Linha/card clicável operável por teclado: `role="button"`, `tabindex="0"`, handler de Enter/Espaço. Trocar de tela move o foco ao título.
- Sidebar vira **drawer com hambúrguer** no mobile; nunca `display:none` sem alternativa.

**Segurança de ação.**
- Estado desabilitado por **atributo `disabled`**, não classe (classe não bloqueia teclado).
- Ação auditável/irreversível **valida a justificativa** antes de confirmar (helper `confirmAction`); não deixar campo obrigatório decorativo.

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
Protótipos de referência vivos do que esta família produz, com os princípios acima já aplicados — consultar antes de gerar:
`knowledge-mt/mt-produtos/2.6-cobranca/prototipo/` (multi-arquivo) e `knowledge_cob/cobranca-prototype/` (arquivo único). Aprendizados consolidados em `knowledge-mt/criticas/Aprendizados_Prototipo_Cobranca.md`.

## Saída
Um repo de protótipo navegável, no design system EloGroup, cujo `index.html` é
autossuficiente (CSS e JS embutidos inline; só fontes via CDN) e pode ser baixado e
compartilhado como um único arquivo:

```
<produto>-prototipo/
  index.html              # GERADO por build.py — autossuficiente, arquivo único
  build.py                # monta index.html: shell + screens + CSS/JS inline
  shell.html              # casca: skip-link + topbar + sidebar por área (drawer no mobile) + <main id="main-content"> + scripts
  styles/
    tokens.css  components.css  screens.css   # design system EloGroup (copiados, sem editar)
    prototipo.css                              # estilos só do protótipo (a11y, drawer lateral, responsivo)
  js/
    mock-data.js   # window.MOCK
    app.js         # IIFE: show (move foco), switchTab (ARIA+setas), openPopup/closePopup (foco+trap+Esc), toggleNav, confirmAction, initMockData
  screens/
    01-....html ... NN-....html   # uma <section class="screen"> por tela
  docs/
    spec-prototipo-v0.md  # opcional — escopo e decisões
  README.md
```
