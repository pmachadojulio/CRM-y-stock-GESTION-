"""Cierre mensual de comisiones (el cuore del negocio).

Lee docs/data/ventas.csv + stock.csv y genera reportes/YYYY-MM.md con:
ventas cobradas, comisiones por vendedor (regla v1), pendientes de cobro,
top repuestos y quiebres. Todo queda versionado en git como registro.

Uso:
    python reporte_mensual.py              # mes actual
    python reporte_mensual.py --mes 2026-09
"""
import argparse
import csv
from datetime import date
from pathlib import Path

from reporte_comisiones import SOCIOS, resumir

BASE = Path(__file__).resolve().parent
VENTAS = BASE / "docs" / "data" / "ventas.csv"
STOCK = BASE / "docs" / "data" / "stock.csv"
OUT_DIR = BASE / "reportes"


def leer_ventas(mes):
    filas, bruto = [], []
    with open(VENTAS, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if not (r.get("sku") or "").strip():
                continue
            fecha = (r.get("fecha") or "").strip()
            if not fecha.startswith(mes):
                continue
            try:
                monto = float(str(r.get("monto") or 0).replace(",", "."))
            except ValueError:
                monto = 0.0
            try:
                com = float(str(r.get("comision_monto") or 0).replace(",", "."))
            except ValueError:
                com = 0.0
            bruto.append(r)
            filas.append({"vendedor": ((r.get("vendedor") or "local").strip().lower()),
                          "estado": ((r.get("estado") or "pendiente").strip().lower()),
                          "monto": monto, "comision": com})
    return filas, bruto


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mes", default=date.today().strftime("%Y-%m"))
    mes = ap.parse_args().mes
    filas, bruto = leer_ventas(mes)
    tot, pendiente = resumir(filas)

    por_sku = {}
    for r in bruto:
        if (r.get("estado") or "").strip().lower() in ("cobrada", "entregada"):
            k = f"{r.get('sku')} {(r.get('cantidad') or '1')}u"
            por_sku[r.get("sku", "")] = por_sku.get(r.get("sku", ""), 0) + float(r.get("monto") or 0)
    top = sorted(por_sku.items(), key=lambda x: -x[1])[:10]

    quiebres = []
    with open(STOCK, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                st, mn = int(float(r.get("stock") or 0)), int(float(r.get("stock_minimo") or 1))
            except ValueError:
                continue
            if r.get("sku") and st <= mn:
                quiebres.append((r["sku"], r.get("nombre", ""), st, mn))

    L = [f"# Cierre {mes} · Repuestero", "",
         f"Ventas del mes: **{len(filas)}**",
         "", "## Comisiones (regla v1)", ""]
    for k in list(SOCIOS) + ["local (50/50)"]:
        if k in tot:
            d = tot[k]
            L.append(f"- **{k}**: {d['ventas']} ventas, monto ${d['monto']:.2f}, "
                     f"**comisión ${d['comision']:.2f}**")
    L += ["", "## Pendientes de cobro", ""]
    if pendiente:
        for k, d in sorted(pendiente.items()):
            L.append(f"- {k}: {d['ventas']} ventas por ${d['monto']:.2f}")
    else:
        L.append("Sin pendientes 🎉")
    L += ["", "## Top repuestos", ""]
    L += [f"- {s}: ${m:.2f}" for s, m in top] or ["(sin ventas cobradas)"]
    L += ["", "## A reponer", ""]
    L += [f"- {s} {n}: stock {st} (mín {mn})" for s, n, st, mn in quiebres] or ["Sin quiebres 🎉"]
    L.append("")
    OUT_DIR.mkdir(exist_ok=True)
    dest = OUT_DIR / f"{mes}.md"
    dest.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L).replace("🎉", "(ok)"))
    print(f"\nGuardado en {dest}")


if __name__ == "__main__":
    main()
