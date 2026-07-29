---
name: critico-redacao
description: Use quando o usuário quer criticar a redação de requisitos funcionais — forma EARS-PT, ambiguidade, vocabulário proibido, singularidade e brevidade. Despachado pelo loop `spec-critico`; também roda solto num doc de feature.
---

# critico-redacao

Hard skill: **escrever requisito funcional que admite uma leitura só**.

Regras: bloco `R*` e `J-RED-*` de `regras/criticas.toml`. Não invente exigência fora dele.

## Quando usar
Crítica de redação dos RF de uma feature (subseção 7.N.3). Não julga escopo
(é do `critico-simplicidade`) nem cobertura de teste (é do `critico-testabilidade`).

## Entrada
- A feature (7.N) do `spec.md`.
- `regras/criticas.toml` (blocos `[vocabulario]`, `[ears]`, `[tetos]`, regras `R*`/`J-RED-*`).
- Os achados que o lint já emitiu — **não repetir** o que o script achou.

## Referência de forma — EARS-PT

| # | Padrão | Template |
|---|---|---|
| 1 | Ubíquo | `O <sistema> deve <resposta>` |
| 2 | Estado | `Enquanto <precondição>, o <sistema> deve <resposta>` |
| 3 | Evento | `Quando <gatilho>, o <sistema> deve <resposta>` |
| 4 | Opcional | `Onde <feature existe>, o <sistema> deve <resposta>` |
| 5 | Indesejado | `Se <gatilho>, então o <sistema> deve <resposta>` |
| 6 | Composto | `Enquanto <precondição>, quando <gatilho>, o <sistema> deve <resposta>` |

Ruleset: 0..n precondições · 0..1 gatilho · 1 sistema · 1..n respostas.
Referência completa: `docs/referencias-v3.md` §B.

## Processo

1. Ler a 7.N.3 e os enunciados de RF. Ignorar os que trazem `⚠ NÃO IDENTIFICADO` —
   lacuna declarada é honesta.
2. Para cada RF, nesta ordem:
   - **J-RED-01 — duas leituras.** Tentar ler o enunciado de duas formas que levem a
     comportamentos diferentes. Conseguiu? achado, citando as **duas** leituras.
   - **J-RED-02 — vocabulário.** Termo que não está no Glossário (§2), ou o
     mesmo termo com dois sentidos no documento.
   - **J-RED-03 — repetição.** Enunciado que reafirma o que as seções 1 a 6 já dizem. Citar onde já está e propor a citação por ID.
3. Reescrever cada RF criticado no padrão EARS-PT correto — a proposta vai no campo
   `→` do achado. Crítica sem a reescrita pronta não vale.
4. Aplicar o teto: no máximo 10 achados. Priorizar `bloqueia`; dizer que priorizou.

## Como escrever o achado

```
<arquivo>:<linha>: [<REGRA>/<severidade>] <RF-NN>: <problema em uma frase>. → <reescrita>
```

Sem elogio, sem preâmbulo, sem "sugiro considerar". Achado ou silêncio.

## Saída
Lista de achados no formato acima, `bloqueia` primeiro. Se nada foi achado, uma linha:
`critico-redacao: sem achados.` Não editar o artefato — a correção é do autor.
