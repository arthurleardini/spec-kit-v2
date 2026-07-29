---
titulo: Loop crítico do spec-kit
tipo: metodologia
criado_em: 2026-07-29
status: ativo
---

# Loop crítico

Gate de qualidade da **seção 7 (Features)** do `spec.md`. Não substitui template nem
skill de geração: entra depois delas, antes da entrega. Aceita também o wiki v2
(`refined/Requisitos/*.md`), sem migração — ver [`CONVENCOES-V3.md`](CONVENCOES-V3.md).

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
| Determinística | `scripts/lint_critico.py` | ~0 | forma EARS-PT, vocabulário proibido, singularidade, RF↔cenário, tetos por seção e global, ID, link, RNF local, Dados |
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
| `critico-rastreabilidade` | ID, fonte, rastreio falso, fato duplicado, RNF fora da §5 | `X*`, `N*`, `J-RAS-*` |

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
# a spec inteira, com ledger
python3 scripts/lint_critico.py caminho/spec.md --ledger criticas/

# só o que bloqueia, em JSON, para o loop consumir
python3 scripts/lint_critico.py caminho/spec.md --json --so-bloqueia

# wiki v2 (modo legado — sem spec.md, varre refined/Requisitos/)
python3 scripts/lint_critico.py caminho/refined

# regressão do próprio lint (5 asserções, nos dois formatos)
python3 scripts/testa_lint.py
```

Fixtures em `examples/lint/`: `spec-boa.md` sai limpa (prova que o ruleset é satisfazível
e serve de referência de redação); `spec-ruim.md` dispara as 20 regras de
`esperado-spec-ruim.txt`. As fixtures `refined/feature-*.md` cobrem o modo legado.

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
EARS-nativa `examples/lint/spec-boa.md`, cuja primeira feature cobre 9 RF, 9 cenários e
3 telas em **1106 palavras** — 42% da média do corpus (2607).

| Teto | corpus p50 | corpus máx | fixture EARS | teto | estouram no corpus |
|---|---|---|---|---|---|
| palavras/feature | 2667 | 3351 | 1106 | **2200** | 13 de 14 |
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
| Requisitos & cenários (hoje 7.N.3 / 7.N.4) | 49% |
| Telas & fluxos (hoje 7.N.1 / 7.N.2) | 23% |
| Dados (hoje 7.N.5) | 19% |
| RNF escrito por feature | 8% — some inteiro pela regra `N01` |
| Prosa instrucional herdada do template (linhas `>`) | 6% |

Duas conclusões: EARS-PT **alonga o RF** (p50 8 → 11-19 palavras) e **encurta o
artefato**, porque mata a prosa que explicava o que o enunciado não dizia. E 14% de cada
spec é peso que não é conteúdo da feature — RNF duplicado (8%) e instrução de template (6%).

## Tetos por seção

O documento único expôs o que o wiki escondia: no `knowledge_cob`, `visao.md` tinha
**15.086 palavras** — o maior artefato do conjunto, sem teto nenhum. Concentrar tudo num
arquivo obriga a orçar cada seção.

| Seção | Corpus v2 (palavras) | Teto |
|---|---|---|
| 1 Contexto | 15.086 (a Visão inteira) | **900** |
| 2 Glossário | — | sem teto (tabela de domínio) |
| 3 Regras de negócio | — | sem teto (tabela de domínio) |
| 4 Modelo de dados | 3.692 | **1.200** |
| 5 Requisitos transversais | 1.920 | **1.400** |
| 6 Arquétipos de tela | 1.996 | **1.400** |
| 7.N cada feature | 2.667 (p50) | **2.200** |
| spec inteira | 59.600 (soma do wiki) | **20.000** |

Glossário e Regras não têm teto porque ali volume é conteúdo, não prosa: 52 regras de
negócio são 52 fatos. Os demais têm, e a regra é sempre a mesma — estourou, **corta**.

Regras: `R08` (seção comum acima do teto), `R09` (spec acima do teto global), `R06`
(feature acima do teto). O teto global de 20.000 palavras é orçamento de contexto: acima
disso a spec deixa de caber confortavelmente numa sessão de trabalho, humana ou de agente.

## Fora desta rodada

- M6 (ficha de contrato por integração) e M7 (modelo canônico de programa) do
  [backlog](backlog-ajustes-metodologia.md). A §5.3 já pede a ficha ou o marcador de
  dependência, mas nenhuma regra do lint verifica o conteúdo dela; e não existe camada
  acima do produto para um programa multi-produto.
- **Crítica das seções 1 a 6.** O loop cobre a seção 7; o alicerce segue com `spec-audit`
  (CSD). Os críticos de redação e rastreabilidade se aplicariam bem à §3, mas hoje não são
  despachados para lá.
- **Apetite não vira teto.** A feature declara apetite (2 ou 6 semanas), e o lint exige a
  declaração (`S06`), mas o teto de telas e de RF é global — não deriva do apetite
  declarado. O certo seria 2 semanas comprarem menos tela que 6.
- **Registro por seção não é verificado.** A convenção diz §1 narrativa e §4+ estruturado;
  nenhuma regra confere.
- **Migração automática.** O roteiro de wiki → spec única em
  [`CONVENCOES-V3.md`](CONVENCOES-V3.md) é manual; não há script.

## Fechado nesta rodada

O que estava listado como furo e saiu:

- `constituicao.md` de 1ª classe → `templates/CLAUDE.md`, copiado pelo `spec-scaffold` e
  lido por toda skill antes de escrever.
- Apetite e no-gos no template → linha de metadados da feature, exigida por `S06`.
- Teto por capítulo → `[tetos.secoes]`, com `R08`/`R09`.
- Template gordo → `templates/spec.md` é esqueleto; a instrução mora nas skills, que o
  agente lê e não copia. Os 6% de prosa de template por spec somem.
- Visão e transversais sem gate → viraram seções 1 a 6, com teto.
- EARS-PT embutido na geração → `feature-requisitos` e `templates/CLAUDE.md` trazem a
  tabela dos 6 padrões, então a spec nasce na forma em vez de ser corrigida depois.
