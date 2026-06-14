#!/usr/bin/env python3
"""
build-navigator.py — Gera um navegador HTML single-file do refined/.

Varre a Camada de Intenção (refined/intencao/visao.md) e a Camada de Contrato
(refined/contracts/<feature>/contrato.md) e embute todo o conteúdo num único
arquivo refined-navigator.html, que abre com duplo-clique (sem servidor).
Blocos ```mermaid embutidos no markdown são renderizados como diagramas.

Uso:
    python3 build-navigator.py [diretorio-do-wiki]

Rode novamente sempre que os .md mudarem.
"""
import json
import re
import sys
from pathlib import Path

BASE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
REFINED = BASE / "refined"
CONTRACTS = REFINED / "contracts"
OUT = BASE / "refined-navigator.html"

DOC_LABELS = {
    "contrato": "Contrato",
    # compatibilidade com docs antigos (caso existam):
    "06-telas-fluxos": "06 · Telas e Fluxos",
    "07-historias": "07 · Histórias",
    "08-requisitos": "08 · Requisitos",
    "09-dados": "09 · Dados",
}


def read(p: Path) -> str:
    txt = p.read_text(encoding="utf-8")
    return strip_frontmatter(txt)


def strip_frontmatter(txt: str) -> str:
    """Remove o bloco YAML frontmatter inicial (--- ... ---) para não vazar no render."""
    if txt.startswith("---"):
        end = txt.find("\n---", 3)
        if end != -1:
            nl = txt.find("\n", end + 1)
            return txt[nl + 1:].lstrip("\n") if nl != -1 else ""
    return txt


def md_title(p: Path) -> str:
    """Primeiro heading '# ' do arquivo, ou o stem."""
    if not p.stat().st_size:
        return p.stem
    for line in read(p).splitlines():
        s = line.strip()
        if s.startswith("# "):
            return s[2:].strip()
    return p.stem


def parse_blueprint(text):
    """Parseia blueprint.md em [{'etapa': str, 'features': [{nome,href,resumo,ator,ia}]}]."""
    etapas = []
    atual = None
    for line in text.splitlines():
        h2 = re.match(r"^##\s+(.+)$", line)
        if h2:
            atual = {"etapa": h2.group(1).strip(), "features": []}
            etapas.append(atual)
            continue
        if atual is None:
            continue
        b = re.match(r"^\s*-\s+\[([^\]]+)\]\(([^)]+)\)\s*(.*)$", line)
        if b:
            nome, href, resto = b.group(1), b.group(2), b.group(3)
            am = re.search(r"\[ator:([^\]]+)\]", resto)
            ator = am.group(1).strip() if am else None
            ia = "[ia]" in resto
            resumo = re.sub(r"\[ator:[^\]]+\]|\[ia\]", "", resto).lstrip("-— ").strip()
            atual["features"].append({"nome": nome, "href": href, "resumo": resumo,
                                      "ator": ator, "ia": ia})
    return [e for e in etapas if e["features"]]


def collect():
    if not REFINED.is_dir():
        sys.exit(f"ERRO: {REFINED} não encontrado. Rode na raiz do knowledge_cob.")

    docs = {}
    tree = []

    def add_doc(doc_id, path, label, group_children):
        docs[doc_id] = {"title": md_title(path), "path": str(path.relative_to(BASE)),
                        "content": read(path)}
        group_children.append({"label": label, "type": "doc", "id": doc_id})

    # ---- Páginas-raiz do wiki ----
    raiz = []
    for name in ("overview.md", "index.md", "log.md"):
        f = REFINED / name
        if f.is_file():
            add_doc(f"wiki/{f.stem}", f, f.stem, raiz)
    bp = REFINED / "blueprint.md"
    if bp.is_file():
        bp_text = read(bp)
        docs["wiki/blueprint"] = {"title": md_title(bp), "path": str(bp.relative_to(BASE)),
                                  "content": bp_text, "kind": "blueprint",
                                  "etapas": parse_blueprint(bp_text)}
        raiz.append({"label": "blueprint", "type": "doc", "id": "wiki/blueprint"})
    if raiz:
        tree.append({"label": "Wiki", "type": "group", "children": raiz})

    # ---- Camada de Intenção ----
    intencao = REFINED / "intencao"
    if intencao.is_dir():
        kids = []
        for f in sorted(intencao.glob("*.md")):
            add_doc(f"intencao/{f.stem}", f, f.stem, kids)
        if kids:
            tree.append({"label": "Camada de Intenção", "type": "group", "children": kids})

    # ---- Entidades ----
    entities = REFINED / "entities"
    if entities.is_dir():
        ent_children = []
        for sub in ("personas", "features"):
            d = entities / sub
            if d.is_dir():
                kids = []
                for f in sorted(d.glob("*.md")):
                    add_doc(f"entities/{sub}/{f.stem}", f, f.stem, kids)
                if kids:
                    ent_children.append({"label": f"{sub.capitalize()} ({len(kids)})",
                                         "type": "group", "children": kids})
        if ent_children:
            tree.append({"label": "Entidades", "type": "group", "children": ent_children})

    # ---- Conceitos ----
    concepts = REFINED / "concepts"
    if concepts.is_dir():
        kids = []
        for f in sorted(concepts.glob("*.md")):
            add_doc(f"concepts/{f.stem}", f, f.stem, kids)
        if kids:
            tree.append({"label": "Conceitos", "type": "group", "children": kids})

    # ---- Camada de Contrato ----
    if CONTRACTS.is_dir():
        feat_dirs = sorted(d for d in CONTRACTS.iterdir()
                           if d.is_dir() and not d.name.startswith("_"))
        feat_group = []
        for d in feat_dirs:
            kids = []
            # v2: 1 contrato.md por feature; mantém suporte aos docs antigos 06-09.
            feat_files = sorted(set(d.glob("contrato.md")) | set(d.glob("0[6-9]-*.md")),
                                key=lambda p: p.name)
            for f in feat_files:
                doc_id = f"contrato/{d.name}/{f.stem}"
                t = md_title(f)
                title = t if t.lower().startswith(d.name.lower()) else f"{d.name} — {t}"
                docs[doc_id] = {"title": title,
                                "path": str(f.relative_to(BASE)), "content": read(f)}
                kids.append({"label": DOC_LABELS.get(f.stem, f.stem),
                             "type": "doc", "id": doc_id})
            if kids:
                feat_group.append({"label": d.name, "type": "group", "children": kids})
        if feat_group:
            tree.append({"label": f"Camada de Contrato ({len(feat_group)})",
                         "type": "group", "children": feat_group})

    # ---- Análises ----
    analyses = REFINED / "analyses"
    if analyses.is_dir():
        kids = []
        for f in sorted(analyses.glob("*.md")):
            add_doc(f"analyses/{f.stem}", f, f.stem, kids)
        if kids:
            tree.append({"label": "Análises", "type": "group", "children": kids})

    return docs, tree


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Navegador — __WIKINAME__/refined</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/marked@12/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<style>
  :root {
    --bg: #F9F9F9; --panel: #FFFFFF; --ink: #272727; --muted: #6B6E7A;
    --line: #D8DAE0; --accent: #0C1BA8; --accent-soft: #EEF2FE;
    --sidebar-w: 312px; --toc-w: 224px;
    --code-bg: #F0F2F7; --hl: #FFF3CD;
  }
  body.dark {
    --bg: #16161c; --panel: #20202b; --ink: #e8e8ee; --muted: #9a9aa8;
    --line: #34343f; --accent: #9DB0F5; --accent-soft: #262b46;
    --code-bg: #26262f; --hl: #3a3420;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; height: 100%; }
  body {
    font: 15px/1.6 'Outfit', system-ui, -apple-system, sans-serif;
    background: var(--bg); color: var(--ink);
    display: grid; grid-template-columns: var(--sidebar-w) 1fr;
    grid-template-rows: 54px 1fr; height: 100vh; overflow: hidden;
  }
  header {
    grid-column: 1 / -1; display: flex; align-items: center; gap: 14px;
    padding: 0 18px; border-bottom: 1px solid var(--line); background: var(--panel);
  }
  header .brand small { color: var(--muted); font-weight: 400; margin-left: 6px; }
  header .spacer { flex: 1; }
  #search {
    width: 320px; max-width: 40vw; padding: 7px 11px; border-radius: 8px;
    border: 1px solid var(--line); background: var(--bg); color: var(--ink); font-size: 14px;
  }
  #search:focus { outline: 2px solid var(--accent-soft); }
  .btn {
    padding: 6px 11px; border-radius: 8px; border: 1px solid var(--line);
    background: var(--bg); color: var(--ink); cursor: pointer; font-size: 13px;
  }
  .btn:hover { border-color: var(--accent); }

  aside {
    border-right: 1px solid var(--line); background: var(--panel);
    overflow-y: auto; padding: 10px 8px 40px;
  }
  .node-group > .row {
    font-weight: 600; cursor: pointer; user-select: none;
    padding: 5px 8px; border-radius: 6px; display: flex; gap: 6px; align-items: center;
  }
  .node-group > .row:hover { background: var(--accent-soft); }
  .node-group .caret { color: var(--muted); transition: transform .15s; font-size: 11px; }
  .node-group.collapsed .caret { transform: rotate(-90deg); }
  .node-group.collapsed > .children { display: none; }
  .children { margin-left: 13px; border-left: 1px solid var(--line); padding-left: 6px; }
  .doc {
    cursor: pointer; padding: 4px 8px; border-radius: 6px; color: var(--ink);
    font-size: 13.5px; display: block; white-space: nowrap; overflow: hidden;
    text-overflow: ellipsis;
  }
  .doc:hover { background: var(--accent-soft); }
  .doc.active { background: var(--accent); color: #fff; }
  .doc.hit { box-shadow: inset 2px 0 0 var(--accent); }
  .hidden { display: none !important; }

  main { overflow-y: auto; position: relative; }
  .layout { display: grid; grid-template-columns: 1fr var(--toc-w);
            max-width: 1180px; margin: 0 auto; }
  article { padding: 30px 38px 120px; min-width: 0; }
  .crumb { color: var(--muted); font-size: 13px; margin-bottom: 4px; }
  .docpath { color: var(--muted); font-size: 12px; font-family: 'Roboto Mono', ui-monospace, monospace; }

  nav.toc {
    padding: 30px 16px; font-size: 12.5px; position: sticky; top: 0;
    align-self: start; max-height: 100vh; overflow-y: auto;
  }
  nav.toc h4 { margin: 0 0 8px; color: var(--muted); text-transform: uppercase;
               letter-spacing: .6px; font-size: 11px; }
  nav.toc a { display: block; color: var(--muted); text-decoration: none;
              padding: 2px 0; border-left: 2px solid transparent; padding-left: 8px; }
  nav.toc a:hover { color: var(--accent); }
  nav.toc a.lvl3 { padding-left: 18px; font-size: 12px; }
  nav.toc a.active { color: var(--accent); border-left-color: var(--accent); }

  article h1 { font-size: 26px; letter-spacing: -.4px; margin: .2em 0 .5em; }
  article h2 { font-size: 20px; margin-top: 1.6em; padding-bottom: 4px;
               border-bottom: 1px solid var(--line); }
  article h3 { font-size: 16px; margin-top: 1.4em; }
  article h4 { font-size: 14px; color: var(--muted); }
  article code { background: var(--code-bg); padding: 1px 5px; border-radius: 4px;
                 font-family: 'Roboto Mono', ui-monospace, monospace; font-size: 13px; }
  article pre { background: var(--code-bg); padding: 13px 15px; border-radius: 9px;
                overflow-x: auto; border: 1px solid var(--line); }
  article pre code { background: none; padding: 0; font-size: 12.5px; line-height: 1.5; }
  article table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 13px; }
  article th, article td { border: 1px solid var(--line); padding: 6px 9px;
                           text-align: left; vertical-align: top; }
  article th { background: var(--accent-soft); }
  article tr:nth-child(even) td { background: var(--code-bg); }
  article blockquote { margin: 1em 0; padding: 6px 14px; border-left: 3px solid var(--accent);
                       background: var(--code-bg); border-radius: 0 8px 8px 0; color: var(--muted); }
  article a { color: var(--accent); }
  article hr { border: none; border-top: 1px solid var(--line); margin: 1.8em 0; }
  .mermaid { background: var(--panel); border: 1px solid var(--line); border-radius: 9px;
             padding: 14px; margin: 1em 0; text-align: center; overflow-x: auto; }
  .mermaid-err { color: #b04a3a; font-size: 12px; }
  mark { background: var(--hl); color: inherit; padding: 0 2px; border-radius: 3px; }

  .empty { color: var(--muted); padding: 60px 38px; text-align: center; }
  .badge { display: inline-block; font-size: 10.5px; padding: 1px 7px; border-radius: 20px;
           background: var(--accent-soft); color: var(--accent); margin-left: 6px;
           vertical-align: middle; }
  .searchcount { font-size: 12px; color: var(--muted); padding: 4px 10px; }
  .bp-hint { color: var(--muted); font-size: 13px; margin: 0 0 14px; }
  .bp-chain { display: flex; overflow-x: auto; padding: 4px 0 24px; align-items: stretch; }
  .bp-stage { min-width: 230px; flex: 1; background: var(--panel);
    border: 1px solid var(--line); border-radius: 10px; }
  .bp-stage-h { background: var(--accent-soft); color: var(--accent); font-weight: 700;
    padding: 9px 12px; border-radius: 10px 10px 0 0; border-bottom: 1px solid var(--line); }
  .bp-arrow { display: flex; align-items: center; color: var(--muted); font-size: 20px; padding: 0 3px; }
  .bp-feat { display: block; padding: 9px 12px; border-bottom: 1px solid var(--line);
    color: var(--ink); text-decoration: none; cursor: pointer; }
  .bp-feat:last-child { border-bottom: none; }
  .bp-feat:hover { background: var(--accent-soft); }
  .bp-nome { font-weight: 600; }
  .bp-resumo { display: block; color: var(--muted); font-size: 12.5px; }
  .bp-badge { display: inline-block; font-size: 10px; padding: 1px 6px; border-radius: 20px; margin-left: 6px; }
  .bp-badge.ator { background: var(--accent-soft); color: var(--accent); }
  .bp-badge.ia { background: var(--accent); color: #fff; }
  a.deadlink { color: var(--muted) !important; text-decoration: line-through; cursor: default; }
  .brand { display: flex; align-items: center; gap: 10px; }
  .brand-logo svg { height: 22px; width: auto; display: block; }
  .brand-txt { font-weight: 700; letter-spacing: -.2px; }
  body.dark .brand-logo svg { filter: invert(1) brightness(1.7); }
</style>
</head>
<body>
<header>
  <div class="brand"><span class="brand-logo"><svg id="Layer_1" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 595.28 175.54"><defs><style>.cls-1{fill:#272727;}</style></defs><rect class="cls-1" x="54.02" y="94.52" width="13.5" height="13.5"/><path class="cls-1" d="M87.78,121.53a13.5,13.5,0,0,0,13.5-13.5H67.53v13.5Z"/><path class="cls-1" d="M81,81a13.5,13.5,0,0,0-13.5,13.5h54A13.49,13.49,0,0,0,135,81H81Z"/><path class="cls-1" d="M114.79,54a13.51,13.51,0,0,0-13.51,13.51H135V54Z"/><rect class="cls-1" x="135.04" y="67.52" width="13.5" height="13.5"/><path class="cls-1" d="M202.64,103V72.64H234.9v6.75H211v4.75h19.7v6.75H211v5.34H234.9V103Z"/><path class="cls-1" d="M244.35,103V72.64h8.38V95.85h20V103Z"/><path class="cls-1" d="M284.08,99.26a14.07,14.07,0,0,1-5.25-11.45,14.08,14.08,0,0,1,5.25-11.45c3.55-2.87,8.25-4.32,14.19-4.32s10.64,1.45,14.15,4.32a14,14,0,0,1,5.29,11.45,14,14,0,0,1-5.29,11.45c-3.51,2.87-8.21,4.32-14.15,4.32S287.63,102.13,284.08,99.26Zm22.1-4.87a8.21,8.21,0,0,0,2.94-6.58,8,8,0,0,0-2.94-6.54,13.85,13.85,0,0,0-15.82,0,8.05,8.05,0,0,0-2.95,6.54,8.21,8.21,0,0,0,2.95,6.58,14,14,0,0,0,15.82,0Z"/><path class="cls-1" d="M330,99.35A14.53,14.53,0,0,1,325,87.81a13.9,13.9,0,0,1,5.3-11.41c3.54-2.91,8.25-4.36,14-4.36,7.52,0,13.59,2.82,16.7,7.74l-6.11,4a13,13,0,0,0-10.64-5,11.5,11.5,0,0,0-7.78,2.48,8.13,8.13,0,0,0-2.9,6.54c0,5.51,4.1,9.06,10.64,9.06a13.36,13.36,0,0,0,9.87-4.27h-8.76v-6.2h17V103h-6.54v-4.1c-2.69,3.08-6.92,4.7-12.44,4.7S333.33,102.17,330,99.35Z"/><path class="cls-1" d="M372.19,103V72.64h24a11.16,11.16,0,0,1,7.86,2.78,9.25,9.25,0,0,1,3,7.13,8.72,8.72,0,0,1-3,6.88,11.14,11.14,0,0,1-7.61,2.65L408.22,103H396.85l-10.47-10.6h-5.81V103Zm8.38-23.59v6.33h13.67c2.69,0,4.28-1.16,4.28-3.17s-1.59-3.16-4.28-3.16Z"/><path class="cls-1" d="M419.47,99.26a14.07,14.07,0,0,1-5.26-11.45,14.09,14.09,0,0,1,5.26-11.45C423,73.49,427.72,72,433.66,72s10.64,1.45,14.15,4.32a14,14,0,0,1,5.29,11.45,14,14,0,0,1-5.29,11.45c-3.51,2.87-8.21,4.32-14.15,4.32S423,102.13,419.47,99.26Zm22.1-4.87a8.21,8.21,0,0,0,2.94-6.58,8,8,0,0,0-2.94-6.54,13.85,13.85,0,0,0-15.82,0,8.05,8.05,0,0,0-2.95,6.54,8.21,8.21,0,0,0,2.95,6.58,14,14,0,0,0,15.82,0Z"/><path class="cls-1" d="M496.46,72.64v17c0,9.1-6.11,14-17.52,14s-17.52-4.87-17.52-14v-17h8.37V88.79c0,5.13,3.21,7.87,9.15,7.87s9.14-2.74,9.14-7.87V72.64Z"/><path class="cls-1" d="M514.84,94.18V103h-8.38V72.64H529c7.73,0,12.3,4,12.3,10.73A10,10,0,0,1,538,91.23a12.37,12.37,0,0,1-8.64,3Zm0-14.79v8h12.61c3.38,0,5.21-1.46,5.21-4.06s-1.83-4-5.21-4Z"/></svg></span><span class="brand-txt">__WIKINAME__ <small>· navegador</small></span></div>
  <div class="spacer"></div>
  <input id="search" type="search" placeholder="Buscar na árvore e no conteúdo…" autocomplete="off">
  <button class="btn" id="expand">Expandir tudo</button>
  <button class="btn" id="theme">◐ Tema</button>
</header>
<aside id="sidebar"></aside>
<main>
  <div class="layout">
    <article id="article"><div class="empty">Selecione um documento na barra lateral.</div></article>
    <nav class="toc" id="toc"></nav>
  </div>
</main>

<script>
const DOCS = __DOCS__;
const TREE = __TREE__;

const PATH_TO_ID = {};
for (const [id, d] of Object.entries(DOCS)) { if (d.path) PATH_TO_ID[d.path] = id; }

function resolvePath(fromPath, href) {
  href = (href || '').split('#')[0].split('?')[0];
  if (!href || !fromPath) return null;
  const stack = fromPath.split('/').slice(0, -1);
  for (const p of href.split('/')) {
    if (p === '..') stack.pop();
    else if (p === '.' || p === '') continue;
    else stack.push(p);
  }
  return stack.join('/');
}

function rewireLinks(scope, doc) {
  scope.querySelectorAll('a[href]').forEach(a => {
    const href = a.getAttribute('href') || '';
    if (/^https?:/i.test(href)) return;
    if (!/\.md($|#|\?)/.test(href)) return;
    const tid = PATH_TO_ID[resolvePath(doc.path, href)];
    if (tid) {
      a.addEventListener('click', e => { e.preventDefault(); renderDoc(tid); });
    } else {
      a.classList.add('deadlink');
    }
  });
}

function renderBlueprint(id, doc) {
  const art = document.getElementById('article');
  document.getElementById('toc').innerHTML = '';
  let head = '<div class="crumb">Wiki</div><div class="docpath">' + doc.path + '</div>'
    + '<h1>' + (doc.title || 'Blueprint') + '</h1>'
    + '<p class="bp-hint">Cadeia de valor — clique numa feature para abrir a página.</p>';
  let chain = '';
  const etapas = doc.etapas || [];
  etapas.forEach((e, i) => {
    let feats = '';
    e.features.forEach(f => {
      let badges = '';
      if (f.ator) badges += '<span class="bp-badge ator">' + f.ator + '</span>';
      if (f.ia) badges += '<span class="bp-badge ia">IA</span>';
      const tid = PATH_TO_ID[resolvePath(doc.path, f.href)];
      feats += '<a class="bp-feat' + (tid ? '' : ' deadlink') + '"'
        + (tid ? ' data-bpid="' + tid + '"' : '') + '>'
        + '<span class="bp-nome">' + f.nome + '</span>' + badges
        + '<span class="bp-resumo">' + f.resumo + '</span></a>';
    });
    chain += '<div class="bp-stage"><div class="bp-stage-h">' + e.etapa + '</div>' + feats + '</div>';
    if (i < etapas.length - 1) chain += '<div class="bp-arrow">&rarr;</div>';
  });
  art.innerHTML = head + '<div class="bp-chain">' + chain + '</div>';
  art.querySelectorAll('.bp-feat[data-bpid]').forEach(a =>
    a.addEventListener('click', () => renderDoc(a.dataset.bpid)));
  document.querySelector('main').scrollTop = 0;
  location.hash = encodeURIComponent(id);
}

mermaid.initialize({ startOnLoad: false, theme: 'neutral', securityLevel: 'loose' });

/* ---------- DBML → Mermaid erDiagram ---------- */
function dbmlToMermaid(dbml) {
  const lines = dbml.split('\n');
  const tables = []; const refs = [];
  let cur = null; let depth = 0; let inIndexes = false;
  const clean = t => (t || '').split('(')[0].replace(/[^A-Za-z0-9_]/g, '') || 'x';
  for (let raw of lines) {
    const line = raw.replace(/\/\/.*$/, '').trim();
    if (!line) continue;
    const mt = line.match(/^Table\s+"?([A-Za-z0-9_]+)"?/);
    if (mt && !cur) { cur = { name: mt[1], cols: [] }; depth = 0; inIndexes = false;
                      if (line.includes('{')) depth = 1; continue; }
    if (!cur) continue;
    if (/^indexes\s*\{/.test(line)) { inIndexes = true; depth += 1; continue; }
    const opens = (line.match(/\{/g) || []).length;
    const closes = (line.match(/\}/g) || []).length;
    if (inIndexes) { depth += opens - closes; if (depth <= 1) inIndexes = false; continue; }
    depth += opens - closes;
    if (depth <= 0) { tables.push(cur); cur = null; continue; }
    const cm = line.match(/^"?([A-Za-z0-9_]+)"?\s+([A-Za-z0-9_]+(?:\([^)]*\))?)(.*)$/);
    if (cm) {
      const cname = cm[1], ctype = clean(cm[2]), rest = cm[3] || '';
      let key = '';
      if (/\[pk\]|primary key|\bpk\b/i.test(rest)) key = 'PK';
      const rf = rest.match(/ref:\s*[<>-]\s*"?([A-Za-z0-9_]+)"?\.\s*"?([A-Za-z0-9_]+)"?/);
      if (rf) { key = key ? 'PK' : 'FK'; refs.push([cur.name, rf[1], cname]); }
      cur.cols.push({ name: cname, type: ctype, key });
    }
  }
  if (cur) tables.push(cur);
  if (!tables.length) return null;
  let out = 'erDiagram\n';
  for (const t of tables) {
    out += '  ' + t.name + ' {\n';
    for (const c of t.cols.slice(0, 30))
      out += '    ' + c.type + ' ' + c.name + (c.key ? ' ' + c.key : '') + '\n';
    out += '  }\n';
  }
  const seen = new Set();
  for (const [from, to, col] of refs) {
    const k = from + '>' + to;
    if (seen.has(k) || from === to) continue;
    seen.add(k);
    if (tables.find(t => t.name === to))
      out += '  ' + from + ' }o--|| ' + to + ' : "' + col + '"\n';
  }
  return out;
}

/* ---------- Render ---------- */
let mermaidSeq = 0;
function renderDoc(id) {
  const doc = DOCS[id];
  const art = document.getElementById('article');
  if (!doc) { art.innerHTML = '<div class="empty">Documento não encontrado.</div>'; return; }
  document.querySelectorAll('.doc').forEach(d =>
    d.classList.toggle('active', d.dataset.id === id));

  if (doc.kind === 'blueprint') { renderBlueprint(id, doc); return; }

  let html = marked.parse(doc.content);
  const wrap = document.createElement('div');
  wrap.innerHTML = html;

  // converter blocos de código mermaid / dbml
  wrap.querySelectorAll('pre > code').forEach(code => {
    const cls = code.className || '';
    const txt = code.textContent;
    let diagram = null;
    if (/language-mermaid/.test(cls)) diagram = txt;
    else if (/language-dbml/.test(cls)) diagram = dbmlToMermaid(txt);
    if (diagram) {
      const div = document.createElement('div');
      div.className = 'mermaid';
      div.dataset.src = diagram;
      code.parentElement.replaceWith(div);
    }
  });

  const head = '<div class="crumb">' + (id.split('/').slice(0, -1).join(' / ') || '') +
    '</div><div class="docpath">' + doc.path + '</div>';
  art.innerHTML = head;
  art.appendChild(wrap);

  rewireLinks(wrap, doc);

  // renderizar mermaid
  wrap.querySelectorAll('.mermaid').forEach(async div => {
    const src = div.dataset.src;
    const gid = 'mmd' + (mermaidSeq++);
    try {
      const { svg } = await mermaid.render(gid, src);
      div.innerHTML = svg;
    } catch (e) {
      div.innerHTML = '<div class="mermaid-err">⚠ Não foi possível renderizar o diagrama</div>' +
        '<pre><code>' + src.replace(/</g, '&lt;') + '</code></pre>';
    }
  });

  buildToc(wrap);
  highlightSearch();
  document.querySelector('main').scrollTop = 0;
  location.hash = encodeURIComponent(id);
}

/* ---------- TOC ---------- */
function buildToc(scope) {
  const toc = document.getElementById('toc');
  const heads = [...scope.querySelectorAll('h1, h2, h3')];
  if (heads.length < 2) { toc.innerHTML = ''; return; }
  let html = '<h4>Neste documento</h4>';
  heads.forEach((h, i) => {
    const slug = 'h_' + i;
    h.id = slug;
    const lvl = h.tagName === 'H3' ? ' lvl3' : '';
    if (h.tagName === 'H1') return;
    html += '<a class="toclink' + lvl + '" href="#" data-slug="' + slug + '">' +
      h.textContent + '</a>';
  });
  toc.innerHTML = html;
  toc.querySelectorAll('a').forEach(a => a.onclick = e => {
    e.preventDefault();
    document.getElementById(a.dataset.slug)
      .scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
}

/* ---------- Sidebar ---------- */
function buildTree(nodes, container) {
  for (const n of nodes) {
    if (n.type === 'group') {
      const g = document.createElement('div');
      g.className = 'node-group';
      const row = document.createElement('div');
      row.className = 'row';
      row.innerHTML = '<span class="caret">▼</span><span>' + n.label + '</span>';
      const kids = document.createElement('div');
      kids.className = 'children';
      row.onclick = () => g.classList.toggle('collapsed');
      g.appendChild(row); g.appendChild(kids);
      container.appendChild(g);
      buildTree(n.children || [], kids);
    } else {
      const d = document.createElement('a');
      d.className = 'doc';
      d.dataset.id = n.id;
      d.textContent = n.label;
      d.title = (DOCS[n.id] && DOCS[n.id].title) || n.label;
      d.onclick = () => renderDoc(n.id);
      container.appendChild(d);
    }
  }
}

/* ---------- Busca ---------- */
let searchTerm = '';
function applySearch() {
  const q = searchTerm.toLowerCase().trim();
  const docEls = [...document.querySelectorAll('.doc')];
  if (!q) {
    docEls.forEach(d => { d.classList.remove('hidden', 'hit'); });
    document.querySelectorAll('.node-group').forEach(g => g.classList.remove('hidden'));
    return;
  }
  let hits = 0;
  docEls.forEach(d => {
    const id = d.dataset.id;
    const doc = DOCS[id];
    const inName = d.textContent.toLowerCase().includes(q) ||
      (doc && doc.title.toLowerCase().includes(q));
    const inBody = doc && doc.content.toLowerCase().includes(q);
    const match = inName || inBody;
    d.classList.toggle('hidden', !match);
    d.classList.toggle('hit', !!(inBody && match));
    if (match) hits++;
  });
  // esconder grupos sem filhos visíveis
  document.querySelectorAll('.node-group').forEach(g => {
    const anyVisible = g.querySelector('.doc:not(.hidden)');
    g.classList.toggle('hidden', !anyVisible);
    if (anyVisible) g.classList.remove('collapsed');
  });
}
function highlightSearch() {
  const q = searchTerm.trim();
  if (q.length < 2) return;
  const art = document.getElementById('article');
  const needle = q.toLowerCase();
  const esc = q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const escapeHtml = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;')
                            .replace(/>/g, '&gt;');
  const walk = node => {
    if (node.nodeType === 3) {
      if (node.nodeValue.toLowerCase().includes(needle)) {
        const rx = new RegExp('(' + esc + ')', 'gi');
        const span = document.createElement('span');
        span.innerHTML = escapeHtml(node.nodeValue).replace(rx, '<mark>$1</mark>');
        node.replaceWith(span);
      }
    } else if (node.nodeType === 1 &&
               !['PRE', 'CODE', 'SCRIPT', 'STYLE'].includes(node.tagName) &&
               !node.classList.contains('mermaid')) {
      [...node.childNodes].forEach(walk);
    }
  };
  [...art.childNodes].forEach(walk);
}

/* ---------- Init ---------- */
buildTree(TREE, document.getElementById('sidebar'));

document.getElementById('search').addEventListener('input', e => {
  searchTerm = e.target.value;
  applySearch();
});
document.getElementById('theme').onclick = () => {
  document.body.classList.toggle('dark');
  const dark = document.body.classList.contains('dark');
  mermaid.initialize({ startOnLoad: false, theme: dark ? 'dark' : 'neutral',
                       securityLevel: 'loose' });
  try { localStorage.setItem('nav-theme', dark ? 'dark' : 'light'); } catch (e) {}
  const cur = location.hash.slice(1);
  if (cur) renderDoc(decodeURIComponent(cur));
};
let allExpanded = true;
document.getElementById('expand').onclick = () => {
  allExpanded = !allExpanded;
  document.querySelectorAll('.node-group').forEach(g =>
    g.classList.toggle('collapsed', !allExpanded));
  document.getElementById('expand').textContent =
    allExpanded ? 'Recolher tudo' : 'Expandir tudo';
};
try {
  if (localStorage.getItem('nav-theme') === 'dark') {
    document.body.classList.add('dark');
    mermaid.initialize({ startOnLoad: false, theme: 'dark', securityLevel: 'loose' });
  }
} catch (e) {}

// abrir doc do hash, ou o primeiro
const initial = location.hash.slice(1);
if (initial && DOCS[decodeURIComponent(initial)]) renderDoc(decodeURIComponent(initial));
else { const first = Object.keys(DOCS)[0]; if (first) renderDoc(first); }
</script>
</body>
</html>
"""


def main():
    docs, tree = collect()
    docs_json = json.dumps(docs, ensure_ascii=False).replace("</", "<\\/")
    tree_json = json.dumps(tree, ensure_ascii=False).replace("</", "<\\/")
    html = (HTML_TEMPLATE
            .replace("__DOCS__", docs_json)
            .replace("__TREE__", tree_json)
            .replace("__WIKINAME__", BASE.name or "wiki"))
    OUT.write_text(html, encoding="utf-8")
    total_kb = OUT.stat().st_size / 1024
    print(f"OK: {OUT.relative_to(BASE)} gerado — {len(docs)} documentos, {total_kb:.0f} KB")


if __name__ == "__main__":
    main()
