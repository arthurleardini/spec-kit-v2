#!/usr/bin/env python3
"""Lint crítico determinístico do spec-kit — gate do loop crítico.

Dois formatos de entrada:

- **spec único** (v3) — um `spec.md` por produto, com a seção `## 7. Features` e uma
  subseção por feature. É o formato preferido: uma spec, não um wiki.
- **wiki legado** (v2) — `refined/visao.md` + transversais na raiz +
  `refined/Requisitos/<feature>.md`. Suportado para não quebrar os wikis existentes.

Verifica o que dá para verificar por script: forma EARS-PT do RF, vocabulário proibido,
singularidade, RF↔cenário, cobertura de desvio, tetos por seção e global, RNF local,
rastreabilidade de ID/link e capítulo de Dados.

Regras e listas vêm de `regras/criticas.toml` — não há regra hardcoded aqui.

Uso:
    python3 scripts/lint_critico.py caminho/spec.md
    python3 scripts/lint_critico.py caminho/refined            # wiki legado
    python3 scripts/lint_critico.py caminho/spec.md --json --ledger criticas/

Exit codes:  0 = limpo · 1 = só achados "corrige" · 2 = há achado "bloqueia"
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
import tomllib
import unicodedata
from dataclasses import dataclass, asdict, field
from pathlib import Path

EXIT_LIMPO, EXIT_CORRIGE, EXIT_BLOQUEIA = 0, 1, 2

RAIZ_KIT = Path(__file__).resolve().parent.parent
REGRAS_PADRAO = RAIZ_KIT / "regras" / "criticas.toml"

STOPWORDS = {
    "a", "à", "ao", "aos", "as", "às", "com", "como", "da", "das", "de", "do",
    "dos", "e", "em", "na", "nas", "no", "nos", "o", "os", "ou", "para", "por",
    "que", "se", "sem", "um", "uma", "deve", "deverá", "ser", "the",
}

# Título de seção → chave de teto em [tetos.secoes].
CHAVES_SECAO = {
    "contexto": ("contexto",),
    "glossario": ("glossario",),
    "regras": ("regras",),
    "modelo_dados": ("modelo de dados",),
    "transversais": ("transversais",),
    "arquetipos": ("arquetipo", "telas comuns"),
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
def sem_acento(txt: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", txt)
                   if unicodedata.category(c) != "Mn")


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


def conta_palavras(linhas: list[str]) -> int:
    return sum(len(ln.split()) for ln in sem_blocos_codigo(linhas))


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
# Índice de seções
# ---------------------------------------------------------------------------
RE_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")


@dataclass
class Secao:
    nivel: int
    titulo: str
    ini: int          # índice da linha do heading (0-based)
    fim: int          # índice exclusivo do fim do bloco

    @property
    def rotulo(self) -> str:
        """Título sem a numeração (`7.1 Régua` → `Régua`)."""
        return re.sub(r"^[\d.]+\s*", "", self.titulo).strip()

    @property
    def chave(self) -> str | None:
        t = sem_acento(self.rotulo.lower())
        for chave, termos in CHAVES_SECAO.items():
            if any(x in t for x in termos):
                return chave
        return None


def indexa_secoes(linhas: list[str]) -> list[Secao]:
    brutas: list[Secao] = []
    dentro_codigo = False
    for i, ln in enumerate(linhas):
        if ln.lstrip().startswith("```"):
            dentro_codigo = not dentro_codigo
            continue
        if dentro_codigo:
            continue
        if m := RE_HEADING.match(ln):
            brutas.append(Secao(len(m.group(1)), m.group(2), i, len(linhas)))
    for idx, s in enumerate(brutas):
        for prox in brutas[idx + 1:]:
            if prox.nivel <= s.nivel:
                s.fim = prox.ini
                break
    return brutas


def filhas(secoes: list[Secao], pai: Secao, nivel: int | None = None) -> list[Secao]:
    alvo = nivel if nivel is not None else pai.nivel + 1
    return [s for s in secoes if pai.ini < s.ini < pai.fim and s.nivel == alvo]


def acha_secao(secoes: list[Secao], *termos: str, dentro: Secao | None = None,
               nivel: int | None = None) -> Secao | None:
    for s in secoes:
        if dentro is not None and not (dentro.ini < s.ini < dentro.fim):
            continue
        if nivel is not None and s.nivel != nivel:
            continue
        t = sem_acento(s.rotulo.lower())
        if any(sem_acento(x.lower()) in t for x in termos):
            return s
    return None


# ---------------------------------------------------------------------------
# Estruturas do documento
# ---------------------------------------------------------------------------
RE_ID_TELA = re.compile(r"^T-?\d+$")
RE_ID_CT = re.compile(r"^CT-?\d+$")
RE_ARQUETIPO = re.compile(r"\*\*Arquétipo:\*\*\s*(\S+)")
RE_RNF_LOCAL_DEF = re.compile(r"^\s*[-*|]\s*\**(RNF-(?!T-)[A-ZÀ-Ý]+-\d+)\**")
RE_LINK_MD = re.compile(r"\]\(([^)#\s]+\.md)")

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
    """Uma feature — seção `7.N` no spec único, ou o arquivo inteiro no wiki legado."""
    caminho: Path
    nome: str
    linhas: list[str]                 # fatia da feature
    offset: int                       # linha absoluta (0-based) onde a fatia começa
    metadados: str                    # linha «**Eixo:** … **Apetite:** …» ou frontmatter
    rfs: list[RF] = field(default_factory=list)
    cts: list[CT] = field(default_factory=list)
    telas: list[Tela] = field(default_factory=list)
    rnf_locais: list[tuple[str, int]] = field(default_factory=list)
    mermaids: list[tuple[str, str]] = field(default_factory=list)   # (tipo, corpo)
    entidades_proprias: list[tuple[str, int]] = field(default_factory=list)
    campos_sem_tipo: list[tuple[str, int]] = field(default_factory=list)
    links: list[tuple[str, int]] = field(default_factory=list)
    ids_citados: dict[str, set[str]] = field(default_factory=dict)
    dados_texto: str = ""
    dados_linha: int = 1
    referencia_canonica: bool = False
    palavras: int = 0


@dataclass
class Contexto:
    ids_definidos: dict[str, set[str]] = field(default_factory=dict)
    transversais: dict[str, str] = field(default_factory=dict)
    entidades_canonicas: set[str] = field(default_factory=set)


@dataclass
class Spec:
    caminho: Path
    modo: str                          # "spec" | "legado"
    contexto: Contexto
    features: list[Doc]
    secoes_comuns: list[tuple[str, str, int, int]]   # (chave, titulo, linha, palavras)
    palavras: int


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
def _frontmatter_dict(linhas: list[str]) -> dict:
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
    """Devolve (índice da 1ª linha, cabeçalho, linhas de dados) de cada tabela markdown."""
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


def _tipo_mermaid(corpo: str) -> str:
    """Classifica pelo conteúdo, não pelo título — funciona nos dois formatos."""
    if "erDiagram" in corpo:
        return "er"
    if re.search(r"\bT-?\d+\b", corpo):
        return "navegacao"
    return "fluxo"


def _doc_da_fatia(caminho: Path, todas: list[str], ini: int, fim: int, nome: str,
                  metadados: str) -> Doc:
    linhas = todas[ini:fim]
    secoes = indexa_secoes(linhas)
    d = Doc(caminho=caminho, nome=nome, linhas=linhas, offset=ini, metadados=metadados)
    L = lambda i: ini + i + 1          # noqa: E731  índice local → linha 1-based absoluta

    # --- RF ---------------------------------------------------------------
    for t_ini, cab, dados in _tabelas(linhas):
        i_id = _idx_coluna(cab, "id")
        i_en = _idx_coluna(cab, "enunciado", "requisito")
        if i_id is None or i_en is None:
            continue
        i_pr = _idx_coluna(cab, "prioridade")
        i_rf = _idx_coluna(cab, "rn", "ref", "origem", "regra")
        for off, cels in enumerate(dados):
            if i_id >= len(cels) or not re.fullmatch(r"RF-\d+", cels[i_id]):
                continue
            d.rfs.append(RF(
                id=cels[i_id],
                enunciado=cels[i_en] if i_en < len(cels) else "",
                prioridade=cels[i_pr] if i_pr is not None and i_pr < len(cels) else "",
                refs=cels[i_rf] if i_rf is not None and i_rf < len(cels) else "",
                linha=L(t_ini + 2 + off),
            ))

    # --- Telas e cenários: detectados pelo ID no heading ------------------
    for s in secoes:
        m = re.match(r"^(\S+)\s*[—–-]\s*(.*)$", s.rotulo)
        ident, resto = (m.group(1), m.group(2)) if m else (s.rotulo.strip(), "")
        bloco = "\n".join(linhas[s.ini + 1:s.fim])
        if RE_ID_CT.match(ident):
            d.cts.append(CT(
                id=ident, titulo=resto, corpo=bloco,
                rfs=sorted(set(re.findall(
                    r"\b(?:RF-T-\d+|RF-\d+|RNF-T-[A-ZÀ-Ý]+-\d+)\b", resto + " " + bloco))),
                linha=L(s.ini),
            ))
        elif RE_ID_TELA.match(ident):
            arq = RE_ARQUETIPO.search(bloco)
            d.telas.append(Tela(
                id=ident, nome=resto,
                arquetipo=(arq.group(1) if arq else ""),
                tem_wireframe="```wireframe" in bloco,
                linha=L(s.ini),
            ))

    # --- RNF local, mermaid, links, IDs ----------------------------------
    d.rnf_locais = [(m.group(1), L(i)) for i, ln in enumerate(linhas)
                    if (m := RE_RNF_LOCAL_DEF.match(ln))]

    i = 0
    while i < len(linhas):
        if linhas[i].lstrip().startswith("```mermaid"):
            corpo = []
            i += 1
            while i < len(linhas) and not linhas[i].lstrip().startswith("```"):
                corpo.append(linhas[i])
                i += 1
            texto = "\n".join(corpo)
            d.mermaids.append((_tipo_mermaid(texto), texto))
        i += 1

    d.links = [(m.group(1), L(i)) for i, ln in enumerate(linhas)
               for m in RE_LINK_MD.finditer(ln)]
    texto = "\n".join(linhas)
    d.ids_citados = {k: set(rx.findall(texto)) for k, rx in IDS_CITAVEIS.items()}

    # --- Dados -----------------------------------------------------------
    sec_dados = acha_secao(secoes, "dados", dentro=None)
    if sec_dados is not None and "modelo de dados" in sem_acento(sec_dados.rotulo.lower()):
        sec_dados = None                       # é a seção canônica, não a da feature
    if sec_dados is not None:
        fatia = linhas[sec_dados.ini:sec_dados.fim]
        d.dados_texto = "\n".join(fatia)
        d.dados_linha = L(sec_dados.ini)
        d.referencia_canonica = bool(
            re.search(r"modelo-dados\.md|§\s*4|canônic", d.dados_texto, re.IGNORECASE))
        for s in secoes:
            if not (sec_dados.ini < s.ini < sec_dados.fim):
                continue
            t = sem_acento(s.rotulo.lower())
            if any(x in t for x in ("relaco", "relacoe", "canonic", "propri", "entidades")):
                continue
            d.entidades_proprias.append((s.rotulo.strip(), L(s.ini)))
        for t_ini, cab, dados in _tabelas(fatia):
            i_campo = _idx_coluna(cab, "campo")
            i_tipo = _idx_coluna(cab, "tipo")
            if i_campo is None:
                continue
            for off, cels in enumerate(dados):
                nome_c = cels[i_campo] if i_campo < len(cels) else ""
                tipo = cels[i_tipo] if i_tipo is not None and i_tipo < len(cels) else ""
                if nome_c and not nome_c.startswith("<") and not tipo.strip(" <>—-"):
                    d.campos_sem_tipo.append((nome_c, L(sec_dados.ini + t_ini + 2 + off)))

    d.palavras = conta_palavras(linhas)
    return d


def _contexto_do_spec(linhas: list[str], secoes: list[Secao]) -> Contexto:
    ctx = Contexto(ids_definidos={k: set() for k in IDS_CITAVEIS})

    def texto_de(*termos: str) -> str:
        s = acha_secao(secoes, *termos, nivel=2)
        return "\n".join(linhas[s.ini:s.fim]) if s else ""

    contexto_txt = texto_de("contexto")
    ctx.ids_definidos["JTBD"] |= set(IDS_CITAVEIS["JTBD"].findall(contexto_txt))

    regras_txt = texto_de("regras")
    for k in ("RN", "RN-AI"):
        ctx.ids_definidos[k] |= set(IDS_CITAVEIS[k].findall(regras_txt))

    transv_txt = texto_de("transversais")
    ctx.ids_definidos["RF-T"] |= set(IDS_CITAVEIS["RF-T"].findall(transv_txt))
    ctx.ids_definidos["RNF-T"] |= set(IDS_CITAVEIS["RNF-T"].findall(transv_txt))
    for ln in transv_txt.splitlines():
        m = re.search(r"\b(RF-T-\d+|RNF-T-[A-ZÀ-Ý]+-\d+)\b", ln)
        if not m:
            continue
        enunciado = re.sub(r"^\s*[-*|]?\s*\**\s*" + re.escape(m.group(1)) + r"\**\s*[—–|-]?\s*",
                           "", ln).strip(" *|")
        if m.group(1) not in ctx.transversais or len(enunciado) > len(ctx.transversais[m.group(1)]):
            ctx.transversais[m.group(1)] = enunciado

    ctx.ids_definidos["A"] |= set(IDS_CITAVEIS["A"].findall(texto_de("arquétipo", "telas comuns")))

    modelo = texto_de("modelo de dados")
    for ln in modelo.splitlines():
        if m := re.match(r"^\s*[-*]\s*\*\*(.+?)\*\*", ln):
            ctx.entidades_canonicas.add(m.group(1).strip())
    for m in re.finditer(r"^\s{2,}(\w+)\s*\{", modelo, re.MULTILINE):
        ctx.entidades_canonicas.add(m.group(1))
    ctx.entidades_canonicas = {e for e in ctx.entidades_canonicas
                              if e and not e.startswith("<")}
    return ctx


def _contexto_legado(raiz: Path) -> Contexto:
    ctx = Contexto(ids_definidos={k: set() for k in IDS_CITAVEIS})

    def le(nome: str) -> str:
        p = raiz / nome
        return p.read_text(encoding="utf-8") if p.is_file() else ""

    visao = le("visao.md")
    for k in ("RN", "RN-AI", "JTBD"):
        ctx.ids_definidos[k] |= set(IDS_CITAVEIS[k].findall(visao))

    transv = le("requisitos-transversais.md")
    ctx.ids_definidos["RF-T"] |= set(IDS_CITAVEIS["RF-T"].findall(transv))
    ctx.ids_definidos["RNF-T"] |= set(IDS_CITAVEIS["RNF-T"].findall(transv))
    for ln in transv.splitlines():
        m = re.search(r"\b(RF-T-\d+|RNF-T-[A-ZÀ-Ý]+-\d+)\b", ln)
        if not m:
            continue
        enunciado = re.sub(r"^\s*[-*]?\s*\**\s*" + re.escape(m.group(1)) + r"\**\s*[—–-]?\s*",
                           "", ln).strip(" *")
        if m.group(1) not in ctx.transversais or len(enunciado) > len(ctx.transversais[m.group(1)]):
            ctx.transversais[m.group(1)] = enunciado

    ctx.ids_definidos["A"] |= set(IDS_CITAVEIS["A"].findall(le("telas-comuns.md")))

    modelo = le("modelo-dados.md")
    for ln in modelo.splitlines():
        if m := re.match(r"^###\s+(.+?)\s*$", ln):
            ctx.entidades_canonicas.add(m.group(1).strip())
        elif m := re.match(r"^\s*[-*]\s*\*\*(.+?)\*\*", ln):
            ctx.entidades_canonicas.add(m.group(1).strip())
    for m in re.finditer(r"^\s{2,}(\w+)\s*\{", modelo, re.MULTILINE):
        ctx.entidades_canonicas.add(m.group(1))
    ctx.entidades_canonicas = {e for e in ctx.entidades_canonicas
                              if e and not e.startswith("<")}
    return ctx


RE_METADADOS = re.compile(r"\*\*Eixo:\*\*.*\*\*Apetite:\*\*", re.IGNORECASE)


def parse_spec_unico(caminho: Path) -> Spec:
    linhas = caminho.read_text(encoding="utf-8").splitlines()
    secoes = indexa_secoes(linhas)
    sec_features = acha_secao(secoes, "features", "feature", nivel=2)
    ctx = _contexto_do_spec(linhas, secoes)

    features: list[Doc] = []
    for s in filhas(secoes, sec_features, nivel=3):
        meta = next((ln for ln in linhas[s.ini + 1:min(s.ini + 6, s.fim)]
                     if RE_METADADOS.search(ln)), "")
        features.append(_doc_da_fatia(caminho, linhas, s.ini, s.fim, s.rotulo, meta))

    comuns: list[tuple[str, str, int, int]] = []
    for s in secoes:
        if s.nivel != 2 or s.ini == sec_features.ini:
            continue
        if (chave := s.chave):
            comuns.append((chave, s.rotulo, s.ini + 1, conta_palavras(linhas[s.ini:s.fim])))

    return Spec(caminho=caminho, modo="spec", contexto=ctx, features=features,
                secoes_comuns=comuns, palavras=conta_palavras(linhas))


def parse_wiki_legado(refined: Path) -> Spec:
    ctx = _contexto_legado(refined)
    features: list[Doc] = []
    total = 0
    for p in sorted((refined / "Requisitos").glob("*.md")):
        linhas = p.read_text(encoding="utf-8").splitlines()
        fm = _frontmatter_dict(linhas)
        d = _doc_da_fatia(p, linhas, 0, len(linhas), p.stem,
                          f"eixo: {fm.get('eixo', '')}" if fm.get("eixo") else "")
        features.append(d)
        total += d.palavras
    return Spec(caminho=refined, modo="legado", contexto=ctx, features=features,
                secoes_comuns=[], palavras=total)


def e_spec_unico(caminho: Path) -> bool:
    if not caminho.is_file() or caminho.suffix != ".md":
        return False
    linhas = caminho.read_text(encoding="utf-8").splitlines()
    return acha_secao(indexa_secoes(linhas), "features", "feature", nivel=2) is not None


# ---------------------------------------------------------------------------
# Regras
# ---------------------------------------------------------------------------
class Lint:
    def __init__(self, regras: dict):
        self.cfg = regras
        self.tetos = regras["tetos"]
        self.tetos_secao = regras["tetos"].get("secoes", {})
        self.vocab = regras["vocabulario"]
        self.ears = {k: re.compile(v, re.IGNORECASE)
                     for k, v in regras["ears"]["padroes"].items()}
        self.meta_regras = regras["regras"]

    def _novo(self, regra: str, doc: Doc | None, linha: int, alvo: str,
              msg: str, arquivo: str | None = None) -> Achado | None:
        meta = self.meta_regras.get(regra)
        if meta is None or meta.get("severidade") == "off":
            return None
        return Achado(regra=regra, severidade=meta["severidade"],
                      critico=meta.get("critico", ""),
                      arquivo=arquivo or str(doc.caminho), linha=linha,
                      alvo=alvo, msg=msg)

    def classifica_ears(self, enunciado: str) -> str | None:
        alvo = enunciado.strip().lower()
        for nome, rx in self.ears.items():
            if rx.match(alvo):
                return nome
        return None

    # -- execução ----------------------------------------------------------
    def roda(self, spec: Spec) -> list[Achado]:
        out: list[Achado] = []
        add = lambda *a, **kw: out.append(x) if (x := self._novo(*a, **kw)) else None  # noqa: E731

        for doc in spec.features:
            self._redacao(doc, spec, add)
            self._testabilidade(doc, add)
            self._fluxos(doc, add)
            self._simplicidade(doc, spec, add)
            self._nao_funcional(doc, add)
            self._rastreabilidade(doc, spec.contexto, add)
            self._dados(doc, spec.contexto, add)

        # tetos de seção comum e global — só no spec único
        for chave, titulo, linha, palavras in spec.secoes_comuns:
            teto = self.tetos_secao.get(chave, 0)
            if teto and palavras > teto:
                add("R08", None, linha, titulo,
                    f"{palavras} palavras (teto {teto}) — cortar ou mover p/ anexo",
                    arquivo=str(spec.caminho))
        if spec.modo == "spec":
            teto_g = self.tetos.get("palavras_por_spec", 0)
            if teto_g and spec.palavras > teto_g:
                add("R09", None, 1, "",
                    f"spec com {spec.palavras} palavras (teto {teto_g}) — "
                    "cortar feature, seção ou detalhe",
                    arquivo=str(spec.caminho))
        return out

    # --- R: redação --------------------------------------------------------
    def _redacao(self, doc: Doc, spec: Spec, add) -> None:
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

        teto = self.tetos_secao.get("feature", 0)
        if teto and doc.palavras > teto:
            add("R06", doc, doc.offset + 1, doc.nome,
                f"{doc.palavras} palavras (teto {teto}) — mover o comum p/ as seções "
                "transversais ou cortar")

    @staticmethod
    def _nao_singular(en: str) -> bool:
        limpo = re.sub(r"\([^)]*\)", "", en)
        limpo = re.sub(r"`[^`]*`", "", limpo)
        if re.search(r"\be/ou\b", limpo, re.IGNORECASE):
            return True
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
            add("F01", doc, doc.rfs[0].linha, doc.nome,
                "nenhum RF de comportamento indesejado (Se <gatilho>, então …)")

        fluxos = [c for t, c in doc.mermaids if t == "fluxo"]
        if fluxos and not any("{" in c for c in fluxos):
            add("F02", doc, doc.offset + 1, doc.nome,
                "fluxo sem nó de decisão — sem ramo de exceção")

        if doc.rfs and not any(t == "navegacao" for t, _ in doc.mermaids):
            add("F03", doc, doc.offset + 1, doc.nome, "sem diagrama de navegação entre telas")

        texto = "\n".join(doc.linhas).lower()
        faltando = [d for d in self.vocab["desvios_canonicos"] if d not in texto]
        if faltando and doc.rfs:
            add("F04", doc, doc.offset + 1, doc.nome,
                f"desvio canônico não endereçado: {', '.join(faltando)}")

    # --- S: simplicidade ---------------------------------------------------
    def _simplicidade(self, doc: Doc, spec: Spec, add) -> None:
        if len(doc.telas) > self.tetos["telas_por_feature"]:
            add("S01", doc, doc.telas[0].linha, doc.nome,
                f"{len(doc.telas)} telas (teto {self.tetos['telas_por_feature']}) "
                "— fundir em abas/drawers ou reusar arquétipo")

        for t in doc.telas:
            if not t.arquetipo or t.arquetipo.strip("<>—-") == "":
                add("S02", doc, t.linha, t.id, "declarar **Arquétipo:** (A-NN ou «—»)")
            if not t.tem_wireframe:
                add("S05", doc, t.linha, t.id, "sem bloco ```wireframe")

        if len(doc.rfs) > self.tetos["rf_por_feature"]:
            add("S03", doc, doc.rfs[0].linha, doc.nome,
                f"{len(doc.rfs)} RF (teto {self.tetos['rf_por_feature']}) "
                "— promover o comum a RF-T-* ou cortar escopo")

        for rf in doc.rfs:
            for tid, enunciado in spec.contexto.transversais.items():
                if jaccard(rf.enunciado, enunciado) >= self.tetos["similaridade_duplicata"]:
                    add("S04", doc, rf.linha, rf.id,
                        f"duplica {tid} do transversal — citar por ID")
                    break

        if spec.modo == "spec" and doc.rfs and not RE_METADADOS.search(doc.metadados):
            add("S06", doc, doc.offset + 1, doc.nome,
                "declarar **Eixo:** … **Apetite:** … **Fora desta feature:** …")

    # --- N: não-funcional --------------------------------------------------
    def _nao_funcional(self, doc: Doc, add) -> None:
        for rid, linha in doc.rnf_locais:
            add("N01", doc, linha, rid,
                "RNF vive só na seção de requisitos transversais — promover a "
                "RNF-T-* e citar por ID")
        if doc.rfs and not doc.ids_citados.get("RNF-T"):
            add("N02", doc, doc.offset + 1, doc.nome,
                "nenhum RNF-T-* citado — declarar os aplicáveis")

    # --- X: rastreabilidade ------------------------------------------------
    def _rastreabilidade(self, doc: Doc, ctx: Contexto, add) -> None:
        for rf in doc.rfs:
            if not re.search(r"\b(RN-\d+|RN-AI-\d+|RF-T-\d+|JTBD-\d+)\b",
                             rf.refs + " " + rf.enunciado):
                add("X01", doc, rf.linha, rf.id, "sem RN/JTBD de origem")

        for colecao in (doc.rfs, doc.cts, doc.telas):
            vistos: dict[str, int] = {}
            for item in colecao:
                if item.id in vistos:
                    add("X02", doc, item.linha, item.id,
                        f"já definido na linha {vistos[item.id]}")
                vistos[item.id] = item.linha

        for tipo, citados in doc.ids_citados.items():
            definidos = ctx.ids_definidos.get(tipo, set())
            if not definidos:
                continue
            for cid in sorted(citados - definidos):
                linha = next((doc.offset + i + 1 for i, ln in enumerate(doc.linhas)
                              if cid in ln), doc.offset + 1)
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
        if not doc.dados_texto:
            return
        canon_baixo = {e.lower() for e in ctx.entidades_canonicas}
        for nome, linha in doc.entidades_proprias:
            if nome.lower() in canon_baixo:
                add("D01", doc, linha, nome,
                    "entidade canônica — referenciar a seção de modelo de dados, não remodelar")

        if not doc.referencia_canonica:
            add("D02", doc, doc.dados_linha, doc.nome,
                "não referencia as entidades canônicas do modelo de dados")

        for campo, linha in doc.campos_sem_tipo:
            add("D03", doc, linha, campo, "campo sem tipo")

        for termo in self.vocab["proibido_dados"]:
            if contem_termo(doc.dados_texto, termo):
                linha = next((doc.dados_linha + i
                              for i, ln in enumerate(doc.dados_texto.splitlines())
                              if contem_termo(ln, termo)), doc.dados_linha)
                add("D04", doc, linha, "", f"detalhe técnico em Dados: «{termo.strip()}»")


# ---------------------------------------------------------------------------
# Saída
# ---------------------------------------------------------------------------
def resumo(achados: list[Achado]) -> str:
    if not achados:
        return "lint crítico: limpo."
    por_regra: dict[str, int] = {}
    for a in achados:
        chave = f"{a.regra}/{a.severidade}"
        por_regra[chave] = por_regra.get(chave, 0) + 1
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
        "---", "tipo: ledger-critica", f"alvo: {alvo}", f"data: {hoje}",
        f"achados: {len(achados)}", "---", "",
        f"# Críticas — {alvo} ({hoje})", "",
        "Achados do lint determinístico. Cada correção referencia o ID do achado.", "",
        "| # | Regra | Sev | Arquivo:linha | Alvo | Achado | Tratamento |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, a in enumerate(achados, 1):
        linhas.append(f"| {i} | {a.regra} | {a.severidade} | {Path(a.arquivo).name}:{a.linha} "
                      f"| {a.alvo or '—'} | {a.msg} | ⬜ |")
    linhas += ["", "Tratamento: ⬜ aberto · ✅ corrigido · 🚫 recusado (justificar abaixo)", ""]
    arq.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    return arq


def carrega_spec(entrada: Path) -> Spec:
    if entrada.is_file():
        if e_spec_unico(entrada):
            return parse_spec_unico(entrada)
        # arquivo isolado de feature (wiki legado)
        raiz = entrada.parent.parent if entrada.parent.name == "Requisitos" else entrada.parent
        ctx = _contexto_legado(raiz)
        linhas = entrada.read_text(encoding="utf-8").splitlines()
        fm = _frontmatter_dict(linhas)
        d = _doc_da_fatia(entrada, linhas, 0, len(linhas), entrada.stem,
                          f"eixo: {fm.get('eixo', '')}" if fm.get("eixo") else "")
        return Spec(caminho=entrada, modo="legado", contexto=ctx, features=[d],
                    secoes_comuns=[], palavras=d.palavras)

    for cand in (entrada / "spec.md", entrada / "refined" / "spec.md"):
        if cand.is_file():
            return parse_spec_unico(cand)
    refined = entrada if (entrada / "Requisitos").is_dir() else entrada / "refined"
    if (refined / "Requisitos").is_dir():
        return parse_wiki_legado(refined)
    sys.exit(f"erro: não achei spec.md nem {refined}/Requisitos/ em {entrada}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint crítico do spec-kit (gate do loop).")
    ap.add_argument("alvo", type=Path, help="spec.md, ou refined/ de um wiki legado")
    ap.add_argument("--regras", type=Path, default=REGRAS_PADRAO)
    ap.add_argument("--json", action="store_true", help="saída JSON (p/ o loop)")
    ap.add_argument("--ledger", type=Path, help="diretório onde gravar o ledger .md")
    ap.add_argument("--so-bloqueia", action="store_true", help="omitir achados «corrige»")
    args = ap.parse_args()

    regras = tomllib.loads(args.regras.read_text(encoding="utf-8"))
    spec = carrega_spec(args.alvo)
    achados = Lint(regras).roda(spec)
    if args.so_bloqueia:
        achados = [a for a in achados if a.severidade == "bloqueia"]
    achados.sort(key=lambda a: (a.arquivo, a.linha, a.regra))

    if args.json:
        print(json.dumps({"modo": spec.modo, "features": len(spec.features),
                          "palavras": spec.palavras,
                          "achados": [asdict(a) for a in achados],
                          "bloqueia": sum(1 for a in achados if a.severidade == "bloqueia"),
                          "corrige": sum(1 for a in achados if a.severidade == "corrige")},
                         ensure_ascii=False, indent=2))
    else:
        for a in achados:
            print(a.linha_texto())
        print()
        print(f"modo {spec.modo} · {len(spec.features)} feature(s) · {spec.palavras} palavras")
        print(resumo(achados))

    if args.ledger:
        alvo = spec.caminho.stem if spec.caminho.is_file() else (spec.caminho.parent.name or "wiki")
        caminho = ledger(achados, args.ledger, alvo)
        if not args.json:
            print(f"\nledger: {caminho}")

    if any(a.severidade == "bloqueia" for a in achados):
        return EXIT_BLOQUEIA
    return EXIT_CORRIGE if achados else EXIT_LIMPO


if __name__ == "__main__":
    raise SystemExit(main())
