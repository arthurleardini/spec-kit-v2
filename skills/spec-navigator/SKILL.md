---
name: spec-navigator
description: Use quando o usuário quer (re)gerar o artefato HTML navegável do wiki — o navigator. Rodar após qualquer mudança no wiki.
---

# spec-navigator

(Re)gera o artefato HTML navegável do wiki rodando o script do spec-kit:
- `refined-navigator.html` — navegador single-file da Camada de Intenção e da Camada de Requisitos. Inclui o `blueprint.md` renderizado como tela de cadeia de valor.

Deve rodar **após qualquer mudança no wiki** — sempre que os `.md` do `refined/` mudarem, o HTML fica desatualizado.

## Quando usar
Quando o usuário pede para atualizar/regenerar a navegação, gerar o HTML, ou após qualquer skill que tenha alterado o conteúdo do `refined/`.

## Entrada
- O diretório `<wiki>` que contém `refined/`.

## Processo
1. Identificar o `<wiki>` (diretório que contém `refined/`) e o caminho do `spec-kit`.
2. Rodar o navigator:
   ```bash
   python3 <spec-kit>/scripts/build-navigator.py <wiki>
   ```
   Gera `<wiki>/refined-navigator.html` varrendo a Camada de Intenção e a de Requisitos. Se existir `refined/blueprint.md`, ele aparece como uma tela de cadeia de valor dentro do navegador (não precisa de gerador separado).
3. Confirmar que o arquivo foi (re)criado e mostrar o caminho.

## Saída
- `<wiki>/refined-navigator.html` regenerado (com o blueprint embutido como tela, se `blueprint.md` existir).

## Identidade visual
O navegador gerado segue a identidade visual EloGroup — cores institucionais (azul
`#0C1BA8`, fundo `#F9F9F9`, tinta `#272727`), fontes Outfit + Roboto Mono e o logotipo
EloGroup. Toda essa identidade está embutida no `build-navigator.py` (CSS e logo SVG
inline no `HTML_TEMPLATE`); não há arquivos externos nem configuração adicional.
