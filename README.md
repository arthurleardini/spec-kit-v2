# Spec Kit (v3)

Kit de skills para especificar um produto num **arquivo único** — `spec.md` — com gate de
qualidade automático.

## O que é

Um produto, uma spec. Seções numeradas, IDs estáveis, requisito funcional em forma fixa, e
um loop crítico que reprova o que não passa. Não é wiki: não há índice em arquivo, log de
edição nem página por assunto.

Três coisas compõem o kit:

1. **O formato** — `templates/spec.md`, 9 seções + 2 anexos. Convenções em
   [`docs/CONVENCOES-V3.md`](docs/CONVENCOES-V3.md).
2. **As skills** — uma por seção, especialistas, que escrevem no `spec.md`.
3. **O loop crítico** — lint determinístico com exit code + 6 agentes críticos.
   Metodologia em [`docs/LOOP-CRITICO.md`](docs/LOOP-CRITICO.md).

## Estrutura da spec

```
<dir>/
  spec.md                  # a especificação — arquivo único
  CLAUDE.md                # regras de escrita do projeto
  criticas/                # ledgers do loop crítico
  refined-navigator.html   # derivado (build-navigator.py)
```

| Seção | Conteúdo |
|---|---|
| 1 | Contexto — problema, objetivo, personas (`JTBD-NN`), não-objetivos |
| 2 | Glossário |
| 3 | Regras de negócio (`RN-NN`, `RN-AI-NN`) |
| 4 | Modelo de dados canônico (`erDiagram`) |
| 5 | Requisitos transversais (`RNF-T-*`, `RF-T-NN`, integrações) |
| 6 | Arquétipos de tela (`A-NN` + wireframe) |
| 7 | Features — `7.N` por feature, cinco subseções fixas |
| 8 | Questões em aberto |
| 9 | Fontes |
| Anexo A | Vocabulário de componentes |
| Anexo B | Cadeia de valor |

Cada feature: metadados (**eixo**, **apetite**, **no-gos**) + fluxo e navegação em Mermaid
+ telas com arquétipo e wireframe + RF em EARS-PT + cenários + dados.

## Regras de escrita que o kit cobra

1. **RF em EARS-PT** — um dos 6 padrões (`O sistema deve…` · `Enquanto…` · `Quando…` ·
   `Onde…` · `Se…, então…` · composto). Nada de infinitivo solto.
2. **Uma capacidade por RF** — `e` / `e/ou` ligando ações = dois RF.
3. **Vocabulário fechado** — sem palavra subjetiva, brecha, superlativo ou verbo oco.
   Lacuna se declara: `⚠ NÃO IDENTIFICADO — definir: <pergunta>`.
4. **Desvio é RF** — exceção vira padrão #5, não parágrafo. Feature sem nenhum não passa.
5. **Cenário prova, não repete** — key example com dado concreto e resultado observável.
6. **RNF só na §5** — a feature cita `RNF-T-*` por ID e nunca define RNF local.
7. **Um fato, um lugar** — o que aparece em ≥2 features sobe para §4/§5/§6.
8. **Teto corta conteúdo** — estourou palavras, telas ou RF? corta. Subir teto é decisão
   do usuário.

Origem de cada regra, com fonte: [`docs/referencias-v3.md`](docs/referencias-v3.md).

## Fluxo de uso

```bash
# 1. criar a spec
skill spec-scaffold                       # spec.md + CLAUDE.md + criticas/

# 2. preencher (uma skill por seção)
skill spec-contexto                       # §1 §2 §3
skill spec-audit                          # CSD sobre §1-3, antes de avançar
skill spec-transversais                   # §4 §5 §6
skill feature-telas-fluxos                # §7.N.1 §7.N.2   (por feature)
skill feature-requisitos                  # §7.N.3 §7.N.4
skill feature-dados                       # §7.N.5
skill spec-cadeia-valor                   # Anexo B

# 3. gate
python3 scripts/lint_critico.py spec.md   # exit 2 = não entrega
skill spec-critico                        # lint + 6 críticos + ledger

# 4. entregar
python3 scripts/build-navigator.py .      # HTML navegável offline
skill spec-to-html                        # protótipo clicável (opcional)
```

## Portas de entrada

O kit aceita qualquer fonte, com ou sem pipeline de dados:

1. **Conversa / brainstorm** — o agente conduz e destila direto para as seções.
2. **Acervo de documentos** — PDF/DOCX/PPTX/XLSX convertidos com `markitdown` antes de ler.
3. **Pipeline `raw/`/`trusted/`** (opcional) — quando existe, o `trusted/` alimenta as seções.

Fonte de órgão público pode carregar PII e sigilo fiscal (CTN art. 198): rodar
`python3 scripts/check_sensivel.py <arquivo>.md` antes de versionar ou mandar para LLM
externo; score ≥ 40 exige anonimizar.

## As skills

### Escrita (7)

| Skill | Escreve |
| --- | --- |
| `spec-scaffold` | cria `spec.md`, `CLAUDE.md` e `criticas/` a partir dos templates |
| `spec-contexto` | §1 Contexto · §2 Glossário · §3 Regras de negócio |
| `spec-transversais` | §4 Modelo de dados · §5 Requisitos transversais · §6 Arquétipos |
| `feature-telas-fluxos` | §7.N.1 Fluxo e navegação · §7.N.2 Telas |
| `feature-requisitos` | §7.N.3 Requisitos funcionais · §7.N.4 Cenários de teste |
| `feature-dados` | §7.N.5 Dados |
| `spec-cadeia-valor` | Anexo B Cadeia de valor |

### Loop crítico (7)

Gate da seção 7. Um crítico por hard skill de levantamento; nenhum edita a spec — acham e
assinam, a correção é do autor. Ver [`docs/LOOP-CRITICO.md`](docs/LOOP-CRITICO.md).

| Skill | O que faz |
| --- | --- |
| `spec-critico` | orquestra: lint → críticos em paralelo → ledger → correção → re-lint, com rodadas fixas |
| `critico-redacao` | forma EARS-PT, ambiguidade, vocabulário, brevidade |
| `critico-testabilidade` | RF↔cenário, key example, fronteira da regra, resultado observável |
| `critico-simplicidade` | corta tela, RF, conceito e escopo; pega RF que descreve implementação |
| `critico-fluxos` | desvio e exceção não modelados, contradição fluxo↔RF, estado inalcançável |
| `critico-dados` | entidade que deveria ser canônica, fonte da verdade, modelo que não sustenta os RF |
| `critico-rastreabilidade` | ID e link, rastreio falso, fato duplicado, RNF fora da §5 |

### Operacionais (3)

| Skill | O que faz |
| --- | --- |
| `spec-audit` | auditoria CSD (Certezas, Suposições, Dúvidas) das §1-3, antes de escrever feature |
| `spec-fontes` | integra fonte nova (roteia o fato para a seção dona) e consulta a spec |
| `spec-navigator` | roda o `build-navigator.py` e regenera o HTML navegável |

### Protótipo (5)

Família `spec-to-html` — transforma a seção 7 num protótipo HTML navegável (sem backend),
arquivo único que abre com duplo-clique: `spec-to-html` (índice), `-plano`, `-scaffold`,
`-telas`, `-build`.

## Scripts

Python 3.11+, sem dependência externa.

- **`scripts/lint_critico.py <spec.md>`** — gate determinístico. 30 regras lidas de
  `regras/criticas.toml`: forma EARS-PT, vocabulário proibido, singularidade, RF↔cenário,
  cobertura de desvio, tetos por seção e global, RNF local, ID/link, Dados.
  Flags: `--json`, `--ledger <dir>`, `--so-bloqueia`, `--regras <toml>`.
  Exit `0` limpo · `1` só «corrige» · `2` há «bloqueia».
- **`scripts/testa_lint.py`** — regressão do lint (5 asserções, nos dois formatos).
- **`scripts/build-navigator.py <dir>`** — fatia o `spec.md` por seção e embute tudo num
  `refined-navigator.html` offline, com Mermaid e wireframe renderizados.

## Regras e configuração

**`regras/criticas.toml`** é a fonte única: tetos, padrões EARS, vocabulário proibido,
severidade de cada regra e as regras de julgamento dos críticos. Regra que não está lá não
existe — nem o script nem o crítico inventam exigência. Severidade `off` desliga uma regra.

## Wireframe e componentes

Cada tela traz um bloco ` ```wireframe ` (DSL line-based) renderizado como SVG **fat
marker, só-layout** — formas sem texto legível. Gramática em
[`docs/CONVENCOES-V3.md`](docs/CONVENCOES-V3.md) e na skill `feature-telas-fluxos`.
Componentes usam vocabulário genérico de front (toolbar, card, table, list, button, input,
select, tabs, dialog, chart), agnóstico de framework — Anexo A da spec.

## Compatibilidade com o wiki v2

`lint_critico.py` e `build-navigator.py` aceitam os dois formatos: sem `spec.md`, procuram
`refined/` com `visao.md` e `Requisitos/`. Wiki existente continua funcionando sem
migração. Roteiro de migração e o que morreu do v2:
[`docs/CONVENCOES-V3.md`](docs/CONVENCOES-V3.md).

## Documentos de referência

- **[`docs/CONVENCOES-V3.md`](docs/CONVENCOES-V3.md)** — o formato, o que morreu do v2, migração.
- **[`docs/LOOP-CRITICO.md`](docs/LOOP-CRITICO.md)** — as duas camadas de crítica, ciclo, severidade, ledger, concisão.
- **[`docs/referencias-v3.md`](docs/referencias-v3.md)** — dossiê externo (ISO/IEC/IEEE 29148, EARS, Wiegers, requirements smells, Specification by Example, *Insanely Simple*, Maeda, Shape Up, Google Technical Writing, Amazon PR/FAQ, GitHub Spec Kit) com a regra derivada de cada bloco.
- **[`docs/checklist-levantamento-negocial.md`](docs/checklist-levantamento-negocial.md)** — grade de cobertura de levantamento de demanda negocial.
- **[`docs/backlog-ajustes-metodologia.md`](docs/backlog-ajustes-metodologia.md)** — os 7 ajustes (M1–M7) achados na análise do Knowledge-MT.
- **[`docs/CONVENCOES-V2.md`](docs/CONVENCOES-V2.md)** — convenções do v2 (histórico).

## Exemplos

`examples/lint/` — fixtures do lint, que também servem de referência de redação:

| Arquivo | Para que serve |
|---|---|
| `spec-boa.md` | spec única que sai limpa no gate — 2 features, 9 seções, 2156 palavras |
| `spec-ruim.md` | dispara as 20 regras de `esperado-spec-ruim.txt` |
| `refined/` | wiki no formato v2, para a regressão do modo legado |
