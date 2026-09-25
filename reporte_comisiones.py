"""Reporte de comisiones v1 — lee docs/data/ventas.csv y resume por vendedor.

Regla v1 (ver README):
- vendedor julio/matias -> 100% de comision_monto para él.
- vendedor local/vacío -> 50/50 entre julio y matías.
- Solo cuentan filas con estado cobrada/entregada (pendiente se informa aparte).

Uso:
    python reporte_comisiones.py            # imprime resumen
    python reporte_comisiones.py --csv docs/data/comisiones_resumen.csv
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
VENTAS = BASE / "docs" / "data" / "ventas.csv"
SOCIOS = ("julio", "matias")
VALIDOS = ("pendiente", "cobrada", "entregada")


def cargar():
    filas = []
    with open(VENTAS, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if not (r.get("sku") or "").strip():
                continue
            if r["sku"].strip().lower().startswith("ejemplo"):
                continue
            v = (r.get("vendedor") or "local").strip().lower()
            estado = (r.get("estado") or "pendiente").strip().lower()
            try:
                monto = float(str(r.get("monto") or 0).replace(",", "."))
            except ValueError:
                monto = 0.0
            try:
                com = float(str(r.get("comision_monto") or 0).replace(",", "."))
            except ValueError:
                com = 0.0
            filas.append({"vendedor": v, "estado": estado, "monto": monto, "comision": com})
    return filas


def resumir(filas):
    tot = defaultdict(lambda: {"ventas": 0, "monto": 0.0, "comision": 0.0})
    pendiente = defaultdict(lambda: {"ventas": 0, "monto": 0.0})
    for r in filas:
        v, e = r["vendedor"], r["estado"]
        if e not in VALIDOS:
            e = "pendiente"
        if e == "pendiente":
            pendiente[v]["ventas"] += 1
            pendiente[v]["monto"] += r["monto"]
            continue
        if v in SOCIOS:
            tot[v]["ventas"] += 1
            tot[v]["monto"] += r["monto"]
            tot[v]["comision"] += r["comision"]
        else:  # local / sin atribución -> 50/50
            for s in SOCIOS:
                tot[s]["ventas"] += 0  # la venta no es de nadie, solo la comisión se parte
                tot[s]["monto"] += 0.0
                tot[s]["comision"] += r["comision"] / 2
            tot["local (50/50)"]["ventas"] += 1
            tot["local (50/50)"]["monto"] += r["monto"]
            tot["local (50/50)"]["comision"] += r["comision"]
    return tot, pendiente


def main():
    filas = cargar()
    tot, pendiente = resumir(filas)
    print(f"Ventas leídas: {len(filas)}")
    print(f"{'vendedor':<16}{'ventas':>8}{'monto':>14}{'comision':>12}")
    for k in list(SOCIOS) + ["local (50/50)"]:
        if k in tot:
            d = tot[k]
            print(f"{k:<16}{d['ventas']:>8}{d['monto']:>14.2f}{d['comision']:>12.2f}")
    if pendiente:
        print("\nPendientes de cobro:")
        for k, d in sorted(pendiente.items()):
            print(f"  {k}: {d['ventas']} ventas por ${d['monto']:.2f}")
    if "--csv" in sys.argv:
        i = sys.argv.index("--csv")
        salida = Path(sys.argv[i + 1]) if len(sys.argv) > i + 1 else BASE / "docs" / "data" / "comisiones_resumen.csv"
        with open(salida, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["vendedor", "ventas", "monto", "comision"])
            for k in list(SOCIOS) + ["local (50/50)"]:
                if k in tot:
                    d = tot[k]
                    w.writerow([k, d["ventas"], f"{d['monto']:.2f}", f"{d['comision']:.2f}"])
        print(f"\nResumen guardado en {salida}")


if __name__ == "__main__":
    main()
