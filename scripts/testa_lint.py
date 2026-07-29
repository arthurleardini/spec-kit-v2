#!/usr/bin/env python3
"""Teste de regressão do lint crítico.

Três asserções:
  1. `feature-boa.md` sai limpa (exit 0) — prova que o ruleset é satisfazível.
  2. `feature-ruim.md` dispara cada regra listada em `examples/lint/esperado-ruim.txt`.
  3. Com tetos apertados, as regras de tamanho disparam em `feature-boa.md`
     (prova que os tetos vêm do TOML e não estão hardcoded).

Uso: python3 scripts/testa_lint.py
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LINT = RAIZ / "scripts" / "lint_critico.py"
BOA = RAIZ / "examples" / "lint" / "refined" / "Requisitos" / "feature-boa.md"
RUIM = RAIZ / "examples" / "lint" / "refined" / "Requisitos" / "feature-ruim.md"
ESPERADO = RAIZ / "examples" / "lint" / "esperado-ruim.txt"
REGRAS = RAIZ / "regras" / "criticas.toml"

TETOS_APERTADOS = {
    "palavras_por_rf": 5,
    "palavras_por_artefato": 60,
    "telas_por_feature": 2,
    "rf_por_feature": 3,
    "palavras_por_cenario": 10,
}


def roda(alvo: Path, regras: Path = REGRAS) -> tuple[int, str]:
    p = subprocess.run([sys.executable, str(LINT), str(alvo), "--regras", str(regras)],
                       capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def regras_disparadas(saida: str) -> set[str]:
    return set(re.findall(r"\[([A-Z]\d{2})/", saida))


def toml_com_tetos(novos: dict) -> Path:
    texto = REGRAS.read_text(encoding="utf-8")
    for chave, valor in novos.items():
        texto = re.sub(rf"^{chave}\s*=.*$", f"{chave} = {valor}", texto,
                       count=1, flags=re.MULTILINE)
    tmp = Path(tempfile.mkdtemp()) / "criticas.toml"
    tmp.write_text(texto, encoding="utf-8")
    return tmp


def main() -> int:
    falhas: list[str] = []

    # 1 — a fixture boa passa limpa
    codigo, saida = roda(BOA)
    if codigo != 0:
        falhas.append(f"feature-boa deveria sair limpa; exit={codigo}\n{saida}")

    # 2 — a fixture ruim dispara todas as regras esperadas
    codigo, saida = roda(RUIM)
    if codigo != 2:
        falhas.append(f"feature-ruim deveria bloquear (exit 2); exit={codigo}")
    esperadas = {ln.split()[0] for ln in ESPERADO.read_text(encoding="utf-8").splitlines()
                 if ln.strip() and not ln.startswith("#")}
    faltando = esperadas - regras_disparadas(saida)
    if faltando:
        falhas.append(f"regras esperadas que não dispararam: {sorted(faltando)}")

    # 3 — tetos vêm do TOML
    codigo, saida = roda(BOA, toml_com_tetos(TETOS_APERTADOS))
    tamanho = {"R05", "R06", "S01", "S03", "T06"}
    faltando = tamanho - regras_disparadas(saida)
    if faltando:
        falhas.append(f"regras de teto não dispararam com tetos apertados: {sorted(faltando)}")

    if falhas:
        for f in falhas:
            print("FALHA:", f)
        return 1
    print("testa_lint: ok — 3 asserções passaram.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
