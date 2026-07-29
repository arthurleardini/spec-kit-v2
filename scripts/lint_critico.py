#!/usr/bin/env python3
"""Lint crítico determinístico do spec-kit — gate do loop crítico.

Verifica o que dá para verificar por script num doc de feature
(`refined/Requisitos/<feature>.md`): forma EARS-PT do RF, vocabulário proibido,
singularidade, RF↔cenário, cobertura de desvio, tetos de tamanho, RNF local,
rastreabilidade de ID/link e capítulo de Dados.

Regras e listas vêm de `regras/criticas.toml` — não há regra hardcoded aqui.

Uso:
    python3 scripts/lint_critico.py <wiki>/refined
    python3 scripts/lint_critico.py refined/Requisitos/minha-feature.md
    python3 scripts/lint_critico.py refined --json
    python3 scripts/lint_critico.py refined --ledger criticas/

Exit codes:  0 = limpo · 1 = só achados "corrige" · 2 = há achado "bloqueia"
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
import tomllib
from dataclasses import dataclass, asdict
from pathlib import Path

EXIT_LIMPO, EXIT_CORRIGE, EXIT_BLOQUEIA = 0, 1, 2

RAIZ_KIT = Path(__file__).resolve().parent.parent
REGRAS_PADRAO = RAIZ_KIT / "regras" / "criticas.toml"

STOPWORDS = {
    "a", "à", "ao", "aos", "as", "às", "com", "como", "da", "das", "de", "do",
    "dos", "e", "em", "na", "nas", "no", "nos", "o", "os", "ou", "para", "por",
    "que", "se", "sem", "um", "uma", "deve", "deverá", "ser", "the",
}


# ---------------------------------------------------------------------------
# Achado
# ---------------------------------------------------------------------------
@dataclass
class Achado:
    regra: str
    severidade: str
    critico: str
    arquivo: str
    linha: int
    alvo: str
    msg: str

    def linha_texto(self) -> str:
        alvo = f"{self.alvo}: " if self.alvo else ""
        return (f"{self.arquivo}:{self.linha}: [{self.regra}/{self.severidade}] "
                f"{alvo}{self.msg}")


# ---------------------------------------------------------------------------
# Utilidades de texto
# ---------------------------------------------------------------------------
def tokens(txt: str) -> set[str]:
    brutos = re.findall(r"[0-9a-zà-ÿ]+", txt.lower())
    return {t for t in brutos if t not in STOPWORDS and len(t) > 2}


def jaccard(a: str, b: str) -> float:
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def sem_blocos_codigo(linhas: list[str]) -> list[str]:
    """Remove blocos ``` (mermaid, wireframe, código) da contagem de palavras."""
    fora, dentro = [], False
    for ln in linhas:
        if ln.lstrip().startswith("```"):
            dentro = not dentro
            continue
        if not dentro:
            fora.append(ln)
    return fora


def _variante_padding(cid: str, definidos: set[str]) -> str | None:
    """`RN-9` vs `RN-09`: aponta a variante existente em vez de só dizer «não existe»."""
    m = re.match(r"^(.*?)(\d+)$", cid)
    if not m:
        return None
    prefixo, num = m.group(1), int(m.group(2))
    for largura in (1, 2, 3):
        cand = f"{prefixo}{num:0{largura}d}"
        if cand != cid and cand in definidos:
            return cand
    return None


def contem_termo(txt: str, termo: str) -> bool:
    """Casamento por palavra quando o termo é uma só palavra; substring quando frase."""
    baixo = txt.lower()
    if " " in termo:
        return termo.lower() in baixo
    return re.search(rf"(?<![0-9a-zà-ÿ]){re.escape(termo.lower())}(?![0-9a-zà-ÿ])",
                     baixo) is not None


# ---------------------------------------------------------------------------
# Parsing do documento
# ---------------------------------------------------------------------------
RE_RF_LINHA = re.compile(r"^\s*\|\s*(RF-\d+)\s*\|")
RE_CT_TITULO = re.compile(r"^####\s*(CT-\d+)\s*[—–-]\s*(.*)$")
RE_TELA_TITULO = re.compile(r"^####\s+(?!CT-)(\S+)\s*[—–-]\s*(.*)$")
RE_ARQUETIPO = re.compile(r"\*\*Arquétipo:\*\*\s*(\S+)")
RE_RNF_LOCAL_DEF = re.compile(r"^\s*[-*]\s*\*\*(RNF-(?!T-)[A-ZÀ-Ý]+-\d+)\*\*")
RE_ENTIDADE_PROPRIA = re.compile(r"^####\s+(.+?)\s*(?:<!--|$)")
RE_LINK_MD = re.compile(r"\]\(([^)#\s]+\.md)")
RE_H2 = re.compile(r"^##\s+(.*)$")
RE_H3 = re.compile(r"^###\s+(.*)$")

IDS_CITAVEIS = {
    "RN": re.compile(r"\bRN-\d+\b"),
    "RN-AI": re.compile(r"\bRN-AI-\d+\b"),
    "JTBD": re.compile(r"\bJTBD-\d+\b"),
    "RF-T": re.compile(r"\bRF-T-\d+\b"),
    "RNF-T": re.compile(r"\bRNF-T-[A-ZÀ-Ý]+-\d+\b"),
    "A": re.compile(r"\bA-\d+\b"),
}


@dataclass
class RF:
    id: str
    enunciado: str
    prioridade: str
    refs: str
    linha: int


@dataclass
class CT:
    id: str
    titulo: str
    corpo: str
    rfs: list[str]
    linha: int


@dataclass
class Tela:
    id: str
    nome: str
    arquetipo: str
    tem_wireframe: bool
    linha: int


@dataclass
class Doc:
    caminho: Path
    linhas: list[str]
    frontmatter: dict
    rfs: list[RF]
    cts: list[CT]
    telas: list[Tela]
    rnf_locais: list[tuple[str, int]]
    mermaids: list[tuple[str, str]]          # (secao, conteudo)
    entidades_proprias: list[tuple[str, int]]
    campos_sem_tipo: list[tuple[str, int]]
    links: list[tuple[str, int]]
    ids_citados: dict[str, set[str]]
    cap3_texto: str
    cap3_inicio: int
    referencia_canonica: bool
    palavras: int


def _frontmatter(linhas: list[str]) -> dict:
    if not linhas or linhas[0].strip() != "---":
        return {}
    fim = next((i for i, ln in enumerate(linhas[1:], 1) if ln.strip() == "---"), None)
    if fim is None:
        return {}
    fm: dict = {}
    for ln in linhas[1:fim]:
        if ":" in ln and not ln.startswith((" ", "-")):
            k, _, v = ln.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def _tabelas(linhas: list[str]) -> list[tuple[int, list[str], list[list[str]]]]:
    """Devolve (linha_inicial, cabecalho, linhas_de_dados) de cada tabela markdown."""
    saida, i = [], 0
    while i < len(linhas):
        if linhas[i].lstrip().startswith("|"):
            ini = i
            bloco = []
            while i < len(linhas) and linhas[i].lstrip().startswith("|"):
                bloco.append(linhas[i])
                i += 1
            if len(bloco) >= 2:
                cab = [c.strip().lower() for c in bloco[0].strip().strip("|").split("|")]
                dados = [[c.strip() for c in b.strip().strip("|").split("|")]
                         for b in bloco[2:]]
                saida.append((ini, cab, dados))
        else:
            i += 1
    return saida


def _idx_coluna(cab: list[str], *chaves: str) -> int | None:
    for i, h in enumerate(cab):
        if any(k in h for k in chaves):
            return i
    return None


def _secao_de(linha_idx: int, marcos: list[tuple[int, str]]) -> str:
    atual = ""
    for idx, titulo in marcos:
        if idx <= linha_idx:
            atual = titulo
        else:
            break
    return atual


def parse_doc(caminho: Path) -> Doc:
    texto = caminho.read_text(encoding="utf-8")
    linhas = texto.splitlines()
    fm = _frontmatter(linhas)

    marcos_h2 = [(i, m.group(1)) for i, ln in enumerate(linhas) if (m := RE_H2.match(ln))]
    marcos_h3 = [(i, m.group(1)) for i, ln in enumerate(linhas) if (m := RE_H3.match(ln))]

    # --- RF (tabela dentro do cap. 2) --------------------------------------
    rfs: list[RF] = []
    for ini, cab, dados in _tabelas(linhas):
        i_id = _idx_coluna(cab, "id")
        i_en = _idx_coluna(cab, "enunciado", "requisito")
        if i_id is None or i_en is None:
            continue
        i_pr = _idx_coluna(cab, "prioridade")
        i_rf = _idx_coluna(cab, "rn", "ref", "origem", "regra")
        for off, cels in enumerate(dados):
            if i_id >= len(cels) or not re.fullmatch(r"RF-\d+", cels[i_id]):
                continue
            rfs.append(RF(
                id=cels[i_id],
                enunciado=cels[i_en] if i_en < len(cels) else "",
                prioridade=cels[i_pr] if i_pr is not None and i_pr < len(cels) else "",
                refs=cels[i_rf] if i_rf is not None and i_rf < len(cels) else "",
                linha=ini + 3 + off,
            ))

    # --- Cenários de teste --------------------------------------------------
    cts: list[CT] = []
    for i, ln in enumerate(linhas):
        m = RE_CT_TITULO.match(ln)
        if not m:
            continue
        corpo = []
        for nxt in linhas[i + 1:]:
            if nxt.startswith(("####", "###", "##")):
                break
            corpo.append(nxt)
        corpo_txt = "\n".join(corpo)
        cts.append(CT(
            id=m.group(1),
            titulo=m.group(2),
            corpo=corpo_txt,
            rfs=sorted(set(re.findall(r"\b(?:RF-T-\d+|RF-\d+|RNF-T-[A-ZÀ-Ý]+-\d+)\b",
                                      m.group(2) + " " + corpo_txt))),
            linha=i + 1,
        ))

    # --- Telas (cap. 1) -----------------------------------------------------
    telas: list[Tela] = []
    for i, ln in enumerate(linhas):
        m = RE_TELA_TITULO.match(ln)
        if not m:
            continue
        if not _secao_de(i, marcos_h2).startswith("1."):
            continue
        bloco = []
        for nxt in linhas[i + 1:]:
            if nxt.startswith(("####", "###", "##")):
                break
            bloco.append(nxt)
        bloco_txt = "\n".join(bloco)
        arq = RE_ARQUETIPO.search(bloco_txt)
        telas.append(Tela(
            id=m.group(1),
            nome=m.group(2),
            arquetipo=(arq.group(1) if arq else ""),
            tem_wireframe="```wireframe" in bloco_txt,
            linha=i + 1,
        ))

    # --- RNF local ----------------------------------------------------------
    rnf_locais = [(m.group(1), i + 1) for i, ln in enumerate(linhas)
                  if (m := RE_RNF_LOCAL_DEF.match(ln))]

    # --- Mermaid por seção --------------------------------------------------
    mermaids: list[tuple[str, str]] = []
    i = 0
    while i < len(linhas):
        if linhas[i].lstrip().startswith("```mermaid"):
            sec = _secao_de(i, marcos_h3) or _secao_de(i, marcos_h2)
            corpo = []
            i += 1
            while i < len(linhas) and not linhas[i].lstrip().startswith("```"):
                corpo.append(linhas[i])
                i += 1
            mermaids.append((sec, "\n".join(corpo)))
        i += 1

    # --- Capítulo 3 (Dados) -------------------------------------------------
    cap3_ini, cap3_fim = None, len(linhas)
    for idx, titulo in marcos_h2:
        if titulo.strip().startswith("3."):
            cap3_ini = idx
        elif cap3_ini is not None and idx > cap3_ini:
            cap3_fim = idx
            break
    cap3 = linhas[cap3_ini:cap3_fim] if cap3_ini is not None else []
    cap3_texto = "\n".join(cap3)

    entidades_proprias: list[tuple[str, int]] = []
    campos_sem_tipo: list[tuple[str, int]] = []
    if cap3_ini is not None:
        # A seção de entidades próprias é achada pelo TÍTULO, não pelo número —
        # os wikis divergem na numeração (3.1 ou 3.2 "Entidades próprias").
        dentro_proprias = False
        for off, ln in enumerate(cap3):
            if m3 := RE_H3.match(ln):
                titulo = m3.group(1).lower()
                dentro_proprias = ("própri" in titulo or "propri" in titulo) \
                    and "relaç" not in titulo
                continue
            if dentro_proprias and (m := RE_ENTIDADE_PROPRIA.match(ln)):
                entidades_proprias.append((m.group(1).strip(), cap3_ini + off + 1))
        for ini, cab, dados in _tabelas(cap3):
            i_campo = _idx_coluna(cab, "campo")
            i_tipo = _idx_coluna(cab, "tipo")
            if i_campo is None:
                continue
            for off, cels in enumerate(dados):
                nome = cels[i_campo] if i_campo < len(cels) else ""
                tipo = cels[i_tipo] if i_tipo is not None and i_tipo < len(cels) else ""
                if nome and not nome.startswith("<") and not tipo.strip(" <>—-"):
                    campos_sem_tipo.append((nome, cap3_ini + ini + 3 + off))

    referencia_canonica = "modelo-dados.md" in cap3_texto

    # --- Links e IDs citados -----------------------------------------------
    links = [(m.group(1), i + 1) for i, ln in enumerate(linhas)
             for m in RE_LINK_MD.finditer(ln)]
    ids_citados = {k: set(rx.findall(texto)) for k, rx in IDS_CITAVEIS.items()}

    palavras = sum(len(ln.split()) for ln in sem_blocos_codigo(linhas))

    return Doc(caminho=caminho, linhas=linhas, frontmatter=fm, rfs=rfs, cts=cts,
               telas=telas, rnf_locais=rnf_locais, mermaids=mermaids,
               entidades_proprias=entidades_proprias, campos_sem_tipo=campos_sem_tipo,
               links=links, ids_citados=ids_citados, cap3_texto=cap3_texto,
               cap3_inicio=(cap3_ini or 0) + 1, referencia_canonica=referencia_canonica,
               palavras=palavras)


# ---------------------------------------------------------------------------
# Contexto do wiki (fontes dos IDs citáveis)
# ---------------------------------------------------------------------------
@dataclass
class Contexto:
    raiz: Path
    ids_definidos: dict[str, set[str]]
    transversais: dict[str, str]     # ID -> enunciado
    entidades_canonicas: set[str]


def carrega_contexto(raiz: Path) -> Contexto:
    definidos: dict[str, set[str]] = {k: set() for k in IDS_CITAVEIS}
    transversais: dict[str, str] = {}
    entidades: set[str] = set()

    def le(nome: str) -> str:
        p = raiz / nome
        return p.read_text(encoding="utf-8") if p.is_file() else ""

    visao = le("visao.md")
    for k in ("RN", "RN-AI", "JTBD"):
        definidos[k] |= set(IDS_CITAVEIS[k].findall(visao))

    transv = le("requisitos-transversais.md")
    definidos["RF-T"] |= set(IDS_CITAVEIS["RF-T"].findall(transv))
    definidos["RNF-T"] |= set(IDS_CITAVEIS["RNF-T"].findall(transv))
    for ln in transv.splitlines():
        m = re.search(r"\b(RF-T-\d+|RNF-T-[A-ZÀ-Ý]+-\d+)\b", ln)
        if not m:
            continue
        # Guarda só o enunciado, sem o ID e sem marcação — o ID poluiria a
        # comparação de similaridade que detecta RF duplicado (regra S04).
        enunciado = re.sub(r"^\s*[-*]?\s*\**\s*" + re.escape(m.group(1)) + r"\**\s*[—–-]?\s*",
                           "", ln).strip(" *")
        if m.group(1) not in transversais or len(enunciado) > len(transversais[m.group(1)]):
            transversais[m.group(1)] = enunciado

    telas_comuns = le("telas-comuns.md")
    definidos["A"] |= set(IDS_CITAVEIS["A"].findall(telas_comuns))

    modelo = le("modelo-dados.md")
    for ln in modelo.splitlines():
        if m := re.match(r"^###\s+(.+?)\s*$", ln):
            entidades.add(m.group(1).strip())
        elif m := re.match(r"^\s*[-*]\s*\*\*(.+?)\*\*", ln):
            entidades.add(m.group(1).strip())
    for m in re.finditer(r"^\s{2,}(\w+)\s*\{", modelo, re.MULTILINE):
        entidades.add(m.group(1))

    return Contexto(raiz=raiz, ids_definidos=definidos, transversais=transversais,
                    entidades_canonicas={e for e in entidades if e and not e.startswith("<")})


# ---------------------------------------------------------------------------
# Regras
# ---------------------------------------------------------------------------
class Lint:
    def __init__(self, regras: dict):
        self.cfg = regras
        self.tetos = regras["tetos"]
        self.vocab = regras["vocabulario"]
        self.ears = {k: re.compile(v, re.IGNORECASE)
                     for k, v in regras["ears"]["padroes"].items()}
        self.meta_regras = regras["regras"]

    # -- helpers -----------------------------------------------------------
    def _novo(self, regra: str, doc: Doc, linha: int, alvo: str, msg: str) -> Achado | None:
        meta = self.meta_regras.get(regra)
        if meta is None or meta.get("severidade") == "off":
            return None
        return Achado(regra=regra, severidade=meta["severidade"],
                      critico=meta.get("critico", ""), arquivo=str(doc.caminho),
                      linha=linha, alvo=alvo, msg=msg)

    def classifica_ears(self, enunciado: str) -> str | None:
        alvo = enunciado.strip().lower()
        for nome, rx in self.ears.items():
            if rx.match(alvo):
                return nome
        return None

    # -- execução ----------------------------------------------------------
    def roda(self, doc: Doc, ctx: Contexto) -> list[Achado]:
        out: list[Achado] = []
        add = lambda *a: out.append(x) if (x := self._novo(*a)) else None  # noqa: E731

        self._redacao(doc, add)
        self._testabilidade(doc, add)
        self._fluxos(doc, add)
        self._simplicidade(doc, ctx, add)
        self._nao_funcional(doc, add)
        self._rastreabilidade(doc, ctx, add)
        self._dados(doc, ctx, add)
        return out

    # --- R: redação --------------------------------------------------------
    def _redacao(self, doc: Doc, add) -> None:
        lacuna = self.vocab["marcador_lacuna"]
        rx_passiva = re.compile(self.vocab["passiva"], re.IGNORECASE)

        for rf in doc.rfs:
            en = rf.enunciado
            if lacuna in en:
                continue                      # lacuna declarada é honesta, não erro

            if self.classifica_ears(en) is None:
                add("R01", doc, rf.linha, rf.id,
                    "reescrever em EARS-PT (Enquanto/Quando/Onde/Se … o <sistema> deve …)")

            if self._nao_singular(en):
                add("R02", doc, rf.linha, rf.id,
                    "mais de uma capacidade na frase — quebrar em RFs separados")

            for classe, termos in self.vocab.items():
                if not isinstance(termos, list) or classe in ("sinais_excecao",
                                                              "desvios_canonicos",
                                                              "proibido_dados"):
                    continue
                achados = [t for t in termos if contem_termo(en, t)]
                if achados:
                    add("R03", doc, rf.linha, rf.id,
                        f"smell «{classe}»: {', '.join(achados[:3])}")

            if re.match(r"^\s*(não|nunca|impedir que|evitar que)\b", en, re.IGNORECASE) \
                    or re.search(r"\bnão\s+(deve|deverá|permitir|usar|exibir)\b", en, re.I):
                add("R04", doc, rf.linha, rf.id,
                    "enunciado negativo — reformular como padrão #5 (Se <gatilho>, então …)")

            n = len(en.split())
            if n > self.tetos["palavras_por_rf"]:
                add("R05", doc, rf.linha, rf.id,
                    f"{n} palavras (teto {self.tetos['palavras_por_rf']}) — cortar")

            if rx_passiva.search(en):
                add("R07", doc, rf.linha, rf.id,
                    "voz passiva — dizer quem faz o que a quem")

        if doc.palavras > self.tetos["palavras_por_artefato"]:
            add("R06", doc, 1, "",
                f"{doc.palavras} palavras (teto {self.tetos['palavras_por_artefato']}) "
                "— mover o comum p/ transversal ou cortar")

    @staticmethod
    def _nao_singular(en: str) -> bool:
        limpo = re.sub(r"\([^)]*\)", "", en)
        limpo = re.sub(r"`[^`]*`", "", limpo)
        if re.search(r"\be/ou\b", limpo, re.IGNORECASE):
            return True
        # dois verbos de resposta ligados por "e"/","/";" → duas capacidades
        verbos = re.findall(r"\b\w{4,}(?:ar|er|ir)\b", limpo.lower())
        if len(verbos) >= 2 and re.search(r"(,|;|\be\b)", limpo, re.IGNORECASE):
            return True
        return False

    # --- T: testabilidade --------------------------------------------------
    def _testabilidade(self, doc: Doc, add) -> None:
        cobertos: set[str] = set()
        for ct in doc.cts:
            cobertos |= set(ct.rfs)

            if not ct.rfs:
                add("T02", doc, ct.linha, ct.id,
                    "declarar o RF verificado — «(verifica RF-NN)»")

            corpo_baixo = ct.corpo.lower()
            if not all(p in corpo_baixo for p in ("dado", "quando", "então")):
                add("T03", doc, ct.linha, ct.id, "faltam passos Dado/Quando/Então")

            n = len((ct.titulo + " " + ct.corpo).split())
            if n > self.tetos["palavras_por_cenario"]:
                add("T06", doc, ct.linha, ct.id,
                    f"{n} palavras (teto {self.tetos['palavras_por_cenario']})")

            # T05 compara o RF com o «Então» do cenário: se o resultado esperado é o
            # próprio enunciado reescrito, o cenário não é key example — não prova nada.
            entao = " ".join(re.findall(r"\*\*Então\*\*(.*)", ct.corpo))
            for rf in doc.rfs:
                if rf.id in ct.rfs and entao and \
                        jaccard(rf.enunciado, entao) >= self.tetos["similaridade_cenario"]:
                    add("T05", doc, ct.linha, ct.id,
                        f"só reescreve {rf.id} — usar key example com dado concreto")

        for rf in doc.rfs:
            if rf.id not in cobertos:
                add("T01", doc, rf.linha, rf.id, "nenhum cenário de teste o verifica")

        sinais = self.vocab["sinais_excecao"]
        tem_borda = any(any(contem_termo(ct.titulo + " " + ct.corpo, s) for s in sinais)
                        for ct in doc.cts)
        if doc.cts and not tem_borda:
            add("T04", doc, doc.cts[0].linha, "",
                "todos os cenários são caminho feliz — falta exceção/borda")

    # --- F: fluxo e desvio -------------------------------------------------
    def _fluxos(self, doc: Doc, add) -> None:
        tem_indesejado = any(self.classifica_ears(rf.enunciado) == "indesejado"
                             for rf in doc.rfs)
        if doc.rfs and not tem_indesejado:
            add("F01", doc, doc.rfs[0].linha, "",
                "nenhum RF de comportamento indesejado (Se <gatilho>, então …)")

        fluxo = next((c for s, c in doc.mermaids if s.strip().startswith("1.1")), None)
        if fluxo is not None and "{" not in fluxo:
            add("F02", doc, 1, "", "fluxo 1.1 sem nó de decisão — sem ramo de exceção")

        if not any(s.strip().startswith("1.3") for s, _ in doc.mermaids):
            add("F03", doc, 1, "", "sem diagrama de navegação (1.3)")

        texto = "\n".join(doc.linhas).lower()
        faltando = [d for d in self.vocab["desvios_canonicos"] if d not in texto]
        if faltando and doc.rfs:
            add("F04", doc, 1, "",
                f"desvio canônico não endereçado: {', '.join(faltando)}")

    # --- S: simplicidade ---------------------------------------------------
    def _simplicidade(self, doc: Doc, ctx: Contexto, add) -> None:
        if len(doc.telas) > self.tetos["telas_por_feature"]:
            add("S01", doc, doc.telas[0].linha, "",
                f"{len(doc.telas)} telas (teto {self.tetos['telas_por_feature']}) "
                "— fundir em abas/drawers ou reusar arquétipo")

        for t in doc.telas:
            if not t.arquetipo or t.arquetipo.strip("<>—-") == "":
                add("S02", doc, t.linha, t.id, "declarar **Arquétipo:** (A-NN ou «—»)")
            if not t.tem_wireframe:
                add("S05", doc, t.linha, t.id, "sem bloco ```wireframe")

        if len(doc.rfs) > self.tetos["rf_por_feature"]:
            add("S03", doc, doc.rfs[0].linha, "",
                f"{len(doc.rfs)} RF (teto {self.tetos['rf_por_feature']}) "
                "— promover o comum a RF-T-* ou cortar escopo")

        for rf in doc.rfs:
            for tid, enunciado in ctx.transversais.items():
                if jaccard(rf.enunciado, enunciado) >= self.tetos["similaridade_duplicata"]:
                    add("S04", doc, rf.linha, rf.id,
                        f"duplica {tid} do transversal — citar por ID")
                    break

    # --- N: não-funcional --------------------------------------------------
    def _nao_funcional(self, doc: Doc, add) -> None:
        for rid, linha in doc.rnf_locais:
            add("N01", doc, linha, rid,
                "RNF vive só em requisitos-transversais.md — promover a RNF-T-* e citar por ID")
        if doc.rfs and not doc.ids_citados["RNF-T"]:
            add("N02", doc, 1, "", "nenhum RNF-T-* citado — declarar os aplicáveis")

    # --- X: rastreabilidade ------------------------------------------------
    def _rastreabilidade(self, doc: Doc, ctx: Contexto, add) -> None:
        for rf in doc.rfs:
            if not re.search(r"\b(RN-\d+|RN-AI-\d+|RF-T-\d+|JTBD-\d+)\b",
                             rf.refs + " " + rf.enunciado):
                add("X01", doc, rf.linha, rf.id, "sem RN/JTBD de origem")

        vistos: dict[str, int] = {}
        for rf in doc.rfs:
            if rf.id in vistos:
                add("X02", doc, rf.linha, rf.id, f"já definido na linha {vistos[rf.id]}")
            vistos[rf.id] = rf.linha
        vistos_ct: dict[str, int] = {}
        for ct in doc.cts:
            if ct.id in vistos_ct:
                add("X02", doc, ct.linha, ct.id, f"já definido na linha {vistos_ct[ct.id]}")
            vistos_ct[ct.id] = ct.linha

        for tipo, citados in doc.ids_citados.items():
            definidos = ctx.ids_definidos.get(tipo, set())
            if not definidos:
                continue                       # fonte ausente: X04 já reporta
            for cid in sorted(citados - definidos):
                linha = next((i + 1 for i, ln in enumerate(doc.linhas) if cid in ln), 1)
                dica = ""
                if variante := _variante_padding(cid, definidos):
                    dica = f" — existe «{variante}» (padding do número)"
                add("X03", doc, linha, cid, f"não existe na fonte de {tipo}{dica}")

        for destino, linha in doc.links:
            if (doc.caminho.parent / destino).resolve().is_file():
                continue
            add("X04", doc, linha, "", f"link quebrado: {destino}")

    # --- D: dados ----------------------------------------------------------
    def _dados(self, doc: Doc, ctx: Contexto, add) -> None:
        if not doc.cap3_texto:
            return
        canon_baixo = {e.lower() for e in ctx.entidades_canonicas}
        for nome, linha in doc.entidades_proprias:
            if nome.lower() in canon_baixo:
                add("D01", doc, linha, nome,
                    "entidade canônica — referenciar modelo-dados.md, não remodelar")

        if not doc.referencia_canonica:
            add("D02", doc, doc.cap3_inicio, "",
                "cap. 3 não referencia modelo-dados.md — declarar as entidades canônicas usadas")

        for campo, linha in doc.campos_sem_tipo:
            add("D03", doc, linha, campo, "campo sem tipo")

        for termo in self.vocab["proibido_dados"]:
            if contem_termo(doc.cap3_texto, termo):
                linha = next((doc.cap3_inicio + i
                              for i, ln in enumerate(doc.cap3_texto.splitlines())
                              if contem_termo(ln, termo)), doc.cap3_inicio)
                add("D04", doc, linha, "", f"detalhe técnico no cap. 3: «{termo.strip()}»")


# ---------------------------------------------------------------------------
# Saída
# ---------------------------------------------------------------------------
def resumo(achados: list[Achado]) -> str:
    if not achados:
        return "lint crítico: limpo."
    por_regra: dict[str, int] = {}
    for a in achados:
        por_regra[f"{a.regra}/{a.severidade}"] = por_regra.get(f"{a.regra}/{a.severidade}", 0) + 1
    bloq = sum(1 for a in achados if a.severidade == "bloqueia")
    corr = sum(1 for a in achados if a.severidade == "corrige")
    linhas = [f"{bloq} bloqueia · {corr} corrige", ""]
    for k in sorted(por_regra):
        linhas.append(f"  {k:22} {por_regra[k]}")
    return "\n".join(linhas)


def ledger(achados: list[Achado], destino: Path, alvo: str) -> Path:
    destino.mkdir(parents=True, exist_ok=True)
    hoje = _dt.date.today().isoformat()
    arq = destino / f"{alvo}-{hoje}.md"
    linhas = [
        "---", f"tipo: ledger-critica", f"alvo: {alvo}", f"data: {hoje}",
        f"achados: {len(achados)}", "---", "",
        f"# Críticas — {alvo} ({hoje})", "",
        "Achados do lint determinístico. Cada correção referencia o ID do achado.", "",
        "| # | Regra | Sev | Arquivo:linha | Alvo | Achado | Tratamento |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, a in enumerate(achados, 1):
        arq_curto = Path(a.arquivo).name
        linhas.append(f"| {i} | {a.regra} | {a.severidade} | {arq_curto}:{a.linha} "
                      f"| {a.alvo or '—'} | {a.msg} | ⬜ |")
    linhas += ["", "Tratamento: ⬜ aberto · ✅ corrigido · 🚫 recusado (justificar abaixo)", ""]
    arq.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    return arq


def coleta_alvos(entrada: Path) -> tuple[Path, list[Path]]:
    """Devolve (raiz_do_refined, docs de feature)."""
    if entrada.is_file():
        raiz = entrada.parent.parent if entrada.parent.name == "Requisitos" else entrada.parent
        return raiz, [entrada]
    refined = entrada if (entrada / "Requisitos").is_dir() else entrada / "refined"
    if not (refined / "Requisitos").is_dir():
        sys.exit(f"erro: não achei {refined}/Requisitos/")
    return refined, sorted((refined / "Requisitos").glob("*.md"))


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint crítico do spec-kit (gate do loop).")
    ap.add_argument("alvo", type=Path, help="refined/ do wiki, ou um .md de feature")
    ap.add_argument("--regras", type=Path, default=REGRAS_PADRAO)
    ap.add_argument("--json", action="store_true", help="saída JSON (p/ o loop)")
    ap.add_argument("--ledger", type=Path, help="diretório onde gravar o ledger .md")
    ap.add_argument("--so-bloqueia", action="store_true", help="omitir achados «corrige»")
    args = ap.parse_args()

    regras = tomllib.loads(args.regras.read_text(encoding="utf-8"))
    raiz, docs = coleta_alvos(args.alvo)
    ctx = carrega_contexto(raiz)
    lint = Lint(regras)

    achados: list[Achado] = []
    for d in docs:
        achados.extend(lint.roda(parse_doc(d), ctx))
    if args.so_bloqueia:
        achados = [a for a in achados if a.severidade == "bloqueia"]

    achados.sort(key=lambda a: (a.arquivo, a.linha, a.regra))

    if args.json:
        print(json.dumps({"achados": [asdict(a) for a in achados],
                          "bloqueia": sum(1 for a in achados if a.severidade == "bloqueia"),
                          "corrige": sum(1 for a in achados if a.severidade == "corrige")},
                         ensure_ascii=False, indent=2))
    else:
        for a in achados:
            print(a.linha_texto())
        print()
        print(resumo(achados))

    if args.ledger:
        alvo = docs[0].stem if len(docs) == 1 else raiz.parent.name or "wiki"
        caminho = ledger(achados, args.ledger, alvo)
        if not args.json:
            print(f"\nledger: {caminho}")

    if any(a.severidade == "bloqueia" for a in achados):
        return EXIT_BLOQUEIA
    return EXIT_CORRIGE if achados else EXIT_LIMPO


if __name__ == "__main__":
    raise SystemExit(main())
