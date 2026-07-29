---
name: spec-fontes
description: Use quando o usuário quer integrar uma fonte nova na spec (ata, transcrição, apresentação, planilha) ou consultar o que a spec já diz sobre um tema. Substitui o antigo `spec-wiki`.
---

# spec-fontes

Manutenção contínua do `spec.md`: **integrar** fonte nova e **consultar** o que já está
especificado. Dois modos.

## Quando usar
Quando o usuário traz um documento novo, uma ata, uma transcrição de reunião ou uma
planilha e quer refletir isso na spec — ou pergunta o que a spec já diz sobre um tema.

## Modo `integrar`

1. Converter a fonte com `markitdown` se for binária (PDF/DOCX/PPTX/XLSX).
2. **Checar dado sensível** antes de qualquer coisa:
   `python3 scripts/check_sensivel.py <arquivo.md>`. Score ≥ 40 → anonimizar antes de
   versionar ou mandar para LLM externo. Fonte de órgão fiscal carrega sigilo (CTN art. 198).
3. Ler a fonte e classificar cada fato pelo lugar onde ele mora:

   | Natureza do fato | Vai para |
   |---|---|
   | Problema, objetivo, persona, não-objetivo | §1 (`spec-contexto`) |
   | Termo do domínio | §2 (`spec-contexto`) |
   | Invariante, obrigação, prazo, competência | §3 como `RN-NN` (`spec-contexto`) |
   | Entidade do domínio | §4 (`spec-transversais`) |
   | Qualidade, segurança, integração | §5 (`spec-transversais`) |
   | Padrão de tela | §6 (`spec-transversais`) |
   | Comportamento de uma feature | §7.N (`feature-*`) |

4. Delegar a escrita à skill dona da seção. Esta skill **não escreve** conteúdo de seção —
   ela roteia. Um fato, um dono.
5. Acrescentar a fonte na tabela da seção 9, com tipo e observação.
6. Fato que contradiz o que já está escrito: **não sobrescrever em silêncio**. Registrar a
   divergência na seção 8 (`⚠ NÃO IDENTIFICADO — definir: <qual das duas vale>`) e
   perguntar ao usuário.
7. Rodar o gate depois: `python3 scripts/lint_critico.py <spec.md>`.

## Modo `consultar`

1. Ler o `spec.md` e responder citando **número de seção e ID** (`§7.1, RF-04`), não
   caminho de arquivo.
2. Se a resposta não está na spec, dizer que não está — e oferecer registrar como lacuna
   na seção 8. Não completar de memória.

## Sobre histórico

Não existe `log.md`. O histórico da spec é o **git**: um commit por mudança, com o motivo
na mensagem. Ledger de crítica vive em `criticas/`.

## Saída
- `integrar`: a spec atualizada pelas skills donas, a fonte listada na §9, divergências na §8.
- `consultar`: resposta citando seção e ID, ou a declaração de que a spec não cobre aquilo.
