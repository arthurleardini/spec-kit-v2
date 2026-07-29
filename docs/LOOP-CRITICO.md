---
titulo: Loop crítico do spec-kit
tipo: metodologia
criado_em: 2026-07-29
status: ativo
---

# Loop crítico

Gate de qualidade da Camada de Requisitos. Roda sobre a estrutura do v2 — não substitui
template nem skill de geração; entra depois deles, antes da entrega.

Base externa e derivação de cada regra: [`referencias-v3.md`](referencias-v3.md).

## Por que existe

O [backlog de ajustes](backlog-ajustes-metodologia.md) mostrou que os 7 padrões de furo
achados nas specs do Knowledge-MT não eram erro de quem escreveu: eram lacuna do kit. Se
o template não pede, o agente não gera. E se a verificação é relatório opcional, a lacuna
passa. O loop fecha as duas pontas: a regra existe num arquivo só, e a verificação tem
exit code.

## Duas camadas

| Camada | Quem roda | Custo | O que pega |
|---|---|---|---|
| Determinística | `scripts/lint_critico.py` | ~0 | forma EARS-PT, vocabulário proibido, singularidade, RF↔cenário, tetos, ID, link, RNF local, cap. 3 |
| Julgamento | 6 agentes críticos | alto | ambiguidade real, rastreio falso, desvio não modelado, corte de escopo, promoção de entidade |

A ordem importa: o script roda primeiro e barato, e o crítico recebe os achados dele
para **não repetir**. Crítico gastando contexto no que um regex resolve é desperdício.

## Os críticos

Um por hard skill de levantamento. Cada um lê só o seu bloco de regras.

| Crítico | Mandato | Regras |
|---|---|---|
| `critico-redacao` | forma EARS-PT, ambiguidade, vocabulário, brevidade | `R*`, `J-RED-*` |
| `critico-testabilidade` | RF↔cenário, key example, resultado observável | `T*`, `J-TST-*` |
| `critico-simplicidade` | corte de tela/RF/conceito, escopo, implementação disfarçada | `S*`, `J-SMP-*` |
| `critico-fluxos` | desvio, exceção, contradição fluxo↔RF, estado órfão | `F*`, `J-FLX-*` |
| `critico-dados` | entidade canônica, fonte da verdade, suporte aos RF | `D*`, `J-DAD-*` |
| `critico-rastreabilidade` | ID, fonte, rastreio falso, fato duplicado, RNF fora do transversal | `X*`, `N*`, `J-RAS-*` |

Seis mandatos estreitos em vez de um auditor genérico: *Think Small* — grupo pequeno com
motivo para estar na sala. Cada crítico tem teto de **10 achados**; estourou, prioriza.

## Ciclo

```
lint ──► críticos em paralelo ──► ledger ──► correção ──► lint
   ▲                                                        │
   └──────────────── até rodadas_max (2) ───────────────────┘
```

1. `lint_critico.py` com `--json --ledger criticas/`.
2. `spec-critico` despacha os críticos relevantes ao artefato, em paralelo, numa só mensagem.
3. Achados de lint + críticos entram no ledger, deduplicados por `(regra, alvo)`.
4. O autor corrige. Cada edição referencia o ID do achado. Recusa exige justificativa escrita.
5. Re-lint.

**Gate abre** com lint exit 0 e nenhum `bloqueia` em aberto. **Gate fecha** quando as
rodadas acabam — entrega o ledger com o resto e escala ao humano. Não existe rodada
extra "até ficar bom": loop sem fim é o que fazia a crítica virar reescrita infinita.

## Severidade

| Severidade | Exit | Significado |
|---|---|---|
| `bloqueia` | 2 | não entrega assim |
| `corrige` | 1 | trata ou justifica no ledger |
| `off` | — | regra desligada por decisão do usuário |

Severidade é configuração, não opinião do agente: muda no `regras/criticas.toml`.

## Formato do achado

Um só formato, para lint e crítico — é o que permite juntar tudo num ledger.

```
<arquivo>:<linha>: [<REGRA>/<severidade>] <alvo>: <problema>. → <correção proposta>
```

O ledger sai em `criticas/<alvo>-<AAAA-MM-DD>.md`, com uma linha por achado e a coluna
**Tratamento**: `⬜` aberto · `✅` corrigido · `🚫` recusado com motivo. É esse arquivo
que torna a spec auditável: mostra o que foi apontado, o que foi corrigido e o que foi
recusado **com justificativa** — não só o resultado final.

## Como rodar

```bash
# uma feature
python3 scripts/lint_critico.py caminho/refined/Requisitos/minha-feature.md

# o wiki inteiro, com ledger
python3 scripts/lint_critico.py caminho/refined --ledger criticas/

# só o que bloqueia, em JSON, para o loop consumir
python3 scripts/lint_critico.py caminho/refined --json --so-bloqueia

# regressão do próprio lint
python3 scripts/testa_lint.py
```

Fixtures em `examples/lint/`: `feature-boa.md` sai limpa (prova que o ruleset é
satisfazível e serve de referência de redação); `feature-ruim.md` dispara as 27 regras
listadas em `examples/lint/esperado-ruim.txt`.

## Regras de escrita que o loop passou a cobrar

Resumo do que muda na prática para quem escreve requisito. Detalhe e origem em
[`referencias-v3.md`](referencias-v3.md).

1. **RF em EARS-PT.** Um dos 6 padrões, sempre com `deve`. Nada de infinitivo solto
   ("Permitir cadastrar…").
2. **Um RF, uma capacidade.** `e`/`e/ou` ligando duas ações = dois RF.
3. **Vocabulário fechado.** Palavra subjetiva, brecha, superlativo e verbo oco são erro,
   não estilo. Lacuna honesta usa `⚠ NÃO IDENTIFICADO`.
4. **Desvio é RF.** Exceção se declara no padrão #5 (`Se <gatilho>, então …`), não em
   parágrafo. Feature sem nenhum padrão #5 bloqueia.
5. **Cenário prova, não repete.** Key example com dado concreto; `Então` observável.
6. **RNF só no transversal.** A feature cita `RNF-T-*` por ID e nunca define RNF local.
7. **Teto corta conteúdo.** Estourou palavras/telas/RF? corta — não sobe o teto.

## Concisão — o que morde e o que não morde

Brevidade aqui é orçamento, não gosto: artefato longo custa contexto e degrada o agente
que o lê depois. O que a torna verificável é o teto — e teto só vale se **alguém estoura**.

Os tetos foram calibrados no corpus real de 14 features (`knowledge_cob`) e na fixture
EARS-nativa `examples/lint/refined/Requisitos/feature-boa.md`, que cobre 9 RF, 9 cenários
e 3 telas em **1106 palavras** — 42% da média do corpus (2607).

| Teto | corpus p50 | corpus máx | fixture EARS | teto | estouram no corpus |
|---|---|---|---|---|---|
| palavras/artefato | 2667 | 3351 | 1106 | **2200** | 13 de 14 |
| palavras/cenário | 41 | 80 | 44 | **50** | 29 cenários |
| RF/feature | 13 | 18 | 9 | **14** | 5 features |
| palavras/RF | 8 | 23 | 19 | **20** | 1 RF |
| telas/feature | 4 | 5 | 3 | **5** | 0 |

Critério: **teto ≈ mediana do corpus** — a metade mais gorda corta. A primeira versão
destas regras usava tetos redondos (3500 / 20 / 7 / 25 / 80), todos acima do **máximo**
do corpus: nenhuma regra de tamanho disparava. Teto folgado é regra decorativa.

Onde as palavras estão hoje, no corpus:

| Parte | Fatia |
|---|---|
| Cap. 2 (Requisitos & Cenários) | 49% |
| Cap. 1 (Telas & Fluxos) | 23% |
| Cap. 3 (Dados) | 19% |
| §2.3 (RNF por feature) | 8% — some inteira pela regra `N01` |
| Prosa instrucional herdada do template (linhas `>`) | 6% |

Duas conclusões: EARS-PT **alonga o RF** (p50 8 → 11-19 palavras) e **encurta o
artefato**, porque mata a prosa que explicava o que o enunciado não dizia. E 14% de cada
spec é peso que não é conteúdo da feature — RNF duplicado (8%) e instrução de template (6%).

## Fora desta rodada

Registrado para o kit v3 propriamente dito (esta rodada entregou só o loop):

- `constituicao.md` como artefato de 1ª classe do wiki, lido por toda skill de geração.
- **Apetite** por feature no frontmatter e seção **No-gos / rabbit holes** no template
  (Shape Up) — hoje o loop cobra teto, mas o teto não vem do apetite declarado.
- EARS-PT embutido nos templates e nas skills `contrato-*`, para a spec **nascer** na
  forma em vez de ser corrigida depois.
- M6 (ficha de contrato por integração) e M7 (modelo canônico de programa) do
  [backlog](backlog-ajustes-metodologia.md) — dependem de artefato novo.
- Crítica da Camada de Intenção: hoje o loop cobre só a Camada de Requisitos; a Visão
  segue com `spec-audit` (CSD).

Furos que sobram na parte de **concisão**, todos dependentes de mexer no template:

- **Emagrecer `templates/contrato/contrato.md`** (225 linhas, das quais a maioria é
  blockquote de instrução). Hoje 6% de cada spec gerada é prosa de template copiada. A
  instrução tem de viver na skill, que o agente lê e não copia — não no template, que o
  agente copia e não relê.
- **Teto por capítulo**, não só por artefato. O Cap. 2 come 49% das palavras e nada
  impede que ele coma 70%.
- **Sem teto na Visão nem nos transversais.** O loop mede só `Requisitos/<feature>.md`;
  a Visão pode inflar sem gate.
- **Registro por capítulo** (narrativa na Visão × estruturado nos Requisitos) está
  documentado em `referencias-v3.md` §E, mas não é verificado por nenhuma regra.
