"""Valida docs/data/stock.csv antes de publicar.

Chequea: columnas exactas, SKU único y no vacío, precios numéricos > 0,
stock/stock_minimo enteros >= 0, publicado en {si,no}, y que todo lo
publicado con stock tenga nombre y compatibilidad.

Uso:
    python validar_stock.py
Sale con código 1 si hay errores (útil para CI).
"""
import csv
import sys
from pathlib import Path

CSV = Path(__file__).resolve().parent / "docs" / "data" / "stock.csv"
COLUMNAS = ["sku", "nombre", "marca", "auto_compatible", "tipo", "precio_costo",
            "precio_venta", "stock", "stock_minimo", "foto", "publicado", "texto_auto"]


def main():
    errores, avisos = [], []
    with open(CSV, encoding="utf-8") as f:
        lector = csv.DictReader(f)
        if list(lector.fieldnames or []) != COLUMNAS:
            errores.append(f"Columnas distintas de las esperadas: {lector.fieldnames}")
        vistos = set()
        n = 0
        for i, r in enumerate(lector, start=2):
            n += 1
            sku = (r.get("sku") or "").strip()
            if not sku:
                errores.append(f"línea {i}: sku vacío")
            elif sku in vistos:
                errores.append(f"línea {i}: sku duplicado {sku}")
            vistos.add(sku)
            for col in ("precio_costo", "precio_venta"):
                try:
                    v = float(r.get(col) or 0)
                    if v <= 0:
                        avisos.append(f"línea {i} {sku}: {col}={r.get(col)} (<=0)")
                except ValueError:
                    errores.append(f"línea {i} {sku}: {col} no numérico")
            for col in ("stock", "stock_minimo"):
                try:
                    v = int(float(r.get(col) or 0))
                    if v < 0:
                        errores.append(f"línea {i} {sku}: {col} negativo")
                except ValueError:
                    errores.append(f"línea {i} {sku}: {col} no entero")
            pub = (r.get("publicado") or "").strip().lower()
            if pub not in ("si", "no"):
                errores.append(f"línea {i} {sku}: publicado debe ser si/no")
            if pub == "si" and (r.get("stock") or "0").strip().lstrip("-").isdigit() and int(float(r.get("stock") or 0)) > 0:
                if not (r.get("nombre") or "").strip():
                    errores.append(f"línea {i} {sku}: publicado con stock pero sin nombre")
                if not (r.get("auto_compatible") or "").strip():
                    avisos.append(f"línea {i} {sku}: sin auto_compatible")
                if not (r.get("foto") or "").strip():
                    avisos.append(f"linea {i} {sku}: sin foto (muestra placeholder)")
    print(f"Filas: {n} | Errores: {len(errores)} | Avisos: {len(avisos)}")
    for e in errores:
        print("  ERROR:", e)
    for a in avisos:
        print("  aviso:", a)
    sys.exit(1 if errores else 0)


if __name__ == "__main__":
    main()
