---
name: critico-rastreabilidade
description: Use quando o usuário quer auditar rastreio e procedência de uma spec — rastreio falso, fato afirmado em dois lugares, afirmação de negócio sem fonte, RNF escrito fora do transversal. Despachado pelo loop `spec-critico`.
---

# critico-rastreabilidade

Hard skill: **provar de onde veio**. É a diferença entre spec auditável e spec plausível.

Regras: blocos `X*`, `N*` e `J-RAS-*` de `regras/criticas.toml`.

## Quando usar
Crítica de procedência de uma feature. Roda depois dos outros críticos — depende
do texto já estabilizado.

## Entrada
- A feature (7.N) do `spec.md`.
- As seções 1 a 3 (`RN-*`, `RN-AI-*`, `JTBD-*`), a seção 5 (`RF-T-*`, `RNF-T-*`) e a
  seção 6 (`A-*`).
- `regras/criticas.toml` (regras `X*`/`N*`/`J-RAS-*`).
- Achados do lint (ID inexistente, ID duplicado, link quebrado, RF sem RN, RNF local,
  ausência de citação transversal). **Não repetir.**

## Princípio

O lint verifica que o ID **existe**. Este crítico verifica que o rastreio é **verdadeiro**.
`RF-04 | RN-12` passa no script mesmo quando a RN-12 nada tem a ver com o RF-04.

## Processo

1. **Rastreio falso — J-RAS-01.** Para cada par RF → RN citada: ler a RN na seção 3 e
   decidir se ela **justifica** aquele RF. Não justifica → achado, propondo a RN correta
   ou a criação da RN que falta na seção 3.
2. **Fato duplicado — J-RAS-02.** Procurar o mesmo fato afirmado em dois lugares
   (feature × seção transversal, feature × seção 3, feature × outra feature). Apontar qual é o lugar
   canônico pela regra de **um fato, um lugar** e propor a citação por ID no outro.
3. **Sem fonte — J-RAS-03.** Afirmação de negócio (prazo, teto, competência, obrigação
   legal, nome de sistema) sem RN, sem entrada na seção 9 (Fontes) e sem marcador
   `⚠ NÃO IDENTIFICADO`. Achado: citar a fonte ou marcar a lacuna.
4. **Não-funcional.** Conferir que nenhum RNF é **definido** na feature: RNF vive só na
   seção 5 e a feature cita por ID. O lint pega a definição local
   (`N01`); aqui interessa o RNF disfarçado de RF (enunciado que fala de latência,
   throughput, disponibilidade, segurança) — achado `J-RAS-01` propondo promoção a
   `RNF-T-*`.
5. Teto: 10 achados.

## Como escrever o achado

```
<arquivo>:<linha>: [<REGRA>/<severidade>] <alvo>: <problema de procedência>. → <fonte, ID correto ou marcador de lacuna>
```

## Saída
Achados no formato acima. Nada achado → `critico-rastreabilidade: sem achados.`
Não editar o artefato.
