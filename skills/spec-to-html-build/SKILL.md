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
