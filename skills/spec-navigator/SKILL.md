---
name: spec-navigator
description: Use quando o usuário quer gerar ou atualizar o HTML navegável da spec — roda o build-navigator.py, que fatia o `spec.md` por seção e renderiza Mermaid e wireframe num arquivo único offline.
---

# spec-navigator

Gera o `refined-navigator.html` — a spec navegável num arquivo único, que abre com
duplo-clique, sem servidor. É o formato de leitura e de entrega; a fonte continua sendo o
`spec.md`.

O script fatia o `spec.md` por seção `##`: cada seção vira uma entrada de navegação e as
features (subseções `###` da seção 7) viram um grupo. Blocos ` ```mermaid ` e
` ```wireframe ` são renderizados — o wireframe como SVG fat marker, só-layout.

## Quando usar
Depois de qualquer mudança no `spec.md`. O HTML é derivado: mudou a spec, ele está velho.

## Entrada
O diretório que contém o `spec.md`.

## Processo
1. Identificar o diretório da spec e o caminho do `spec-kit`.
2. Rodar:

   ```bash
   python3 <spec-kit>/scripts/build-navigator.py <dir-da-spec>
   ```

3. Conferir a contagem de documentos na saída do script — ela tem de bater com o número de
   seções mais as features.

O script também aceita o **wiki legado** (v2): se não achar `spec.md`, procura
`refined/` com `visao.md` e `Requisitos/`, e monta a navegação a partir dos arquivos.
Não é necessário migrar um wiki existente só para gerar o HTML.

## Saída
`<dir-da-spec>/refined-navigator.html` regenerado — arquivo único, offline, com Mermaid e
wireframe renderizados no padrão visual EloGroup.
