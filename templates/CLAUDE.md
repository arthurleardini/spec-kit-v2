# <Produto> — regras de escrita da spec

Copiado pelo `spec-scaffold`. Todo agente lê este arquivo **antes** de tocar no `spec.md`.
Regra que não está aqui nem em `regras/criticas.toml` não existe.

## A spec é um arquivo

`spec.md`. Um produto, uma spec. Não criar `index.md`, `log.md`, `overview.md`,
`blueprint.md`, pasta `Requisitos/` nem página nova para "organizar melhor".

- Sumário = a numeração das seções.
- Histórico = git (um commit por mudança, com o motivo na mensagem).
- Crítica = `criticas/<spec>-<data>.md`, gerado pelo loop.

## Um fato, um lugar

| Fato | Onde mora | Como as outras seções o usam |
|---|---|---|
| Problema, objetivo, persona | §1 | citam `JTBD-NN` |
| Termo do domínio | §2 | usam o termo, não redefinem |
| Invariante, obrigação, prazo | §3 como `RN-NN` | citam o ID |
| Entidade do domínio | §4 | referenciam por nome |
| Requisito não-funcional | §5 como `RNF-T-*` | citam o ID |
| Requisito comum a ≥2 features | §5 como `RF-T-NN` | citam o ID |
| Padrão de tela | §6 como `A-NN` | declaram `**Arquétipo:**` |
| Comportamento de uma feature | §7.N | — |

Escrever o mesmo fato duas vezes é erro, não redundância defensiva. Se aparece em duas
features, sobe para §4/§5/§6 e as features passam a citar.

## Requisito funcional em EARS-PT

| # | Padrão | Template |
|---|---|---|
| 1 | Ubíquo | `O <sistema> deve <resposta>` |
| 2 | Estado | `Enquanto <precondição>, o <sistema> deve <resposta>` |
| 3 | Evento | `Quando <gatilho>, o <sistema> deve <resposta>` |
| 4 | Opcional | `Onde <feature existe>, o <sistema> deve <resposta>` |
| 5 | Indesejado | `Se <gatilho>, então o <sistema> deve <resposta>` |
| 6 | Composto | `Enquanto <precondição>, quando <gatilho>, o <sistema> deve <resposta>` |

- Uma capacidade por RF. `e` / `e/ou` ligando ações = dois RF.
- Voz ativa: quem faz o que a quem.
- Sem palavra subjetiva, brecha, superlativo ou verbo oco (lista em `regras/criticas.toml`).
- Desvio e exceção existem como RF padrão #5, não como parágrafo.
- Sem informação? `⚠ NÃO IDENTIFICADO — definir: <pergunta>`, e a pergunta entra na §8.
  Nunca inventar RF vago para tapar buraco.
- RNF não se escreve na feature. Se o enunciado fala de latência, throughput,
  disponibilidade ou segurança, ele é `RNF-T-*` na §5.

## Cenário prova, não repete

`Dado` com valor concreto · `Quando` a ação · `Então` resultado **observável**. Cenário que
reescreve o RF em Gherkin não verifica nada.

## IDs

Contínuos no documento inteiro (`RF-01`…`RF-40`, `T-01`…, `CT-01`…), não por feature.
Estáveis: não renumerar; ao remover um item, deixar o número vago.

## Tetos

Estourou o teto de palavras, de tela ou de RF? **corta conteúdo.** Subir teto é decisão do
usuário, não do agente. Os valores estão em `regras/criticas.toml`.

## Antes de entregar

```bash
python3 <spec-kit>/scripts/lint_critico.py spec.md
```

Exit 2 = não entrega. Para a crítica completa (lint + os 6 críticos), usar a skill
`spec-critico`.

## Fonte com dado sensível

Fonte de órgão público pode carregar PII e sigilo fiscal (CTN art. 198). Antes de
versionar ou mandar para LLM externo:

```bash
python3 scripts/check_sensivel.py <arquivo>.md
```

Score ≥ 40 → anonimizar (pseudônimo determinístico, ex.: `⟨CPF-01⟩`) antes de seguir.
