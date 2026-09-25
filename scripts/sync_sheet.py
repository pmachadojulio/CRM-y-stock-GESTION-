"""Sync Google Sheet -> docs/data/stock.csv (esqueleto Fase 2).

Cómo activarlo (cuando pasen el stock a Sheet):
1. En el Sheet: Archivo > Compartir > "Cualquiera con el enlace (lector)".
2. Archivo > Compartir > Publicar en la web > pestaña stock > CSV. Copiar la URL (export?format=csv).
3. Guardarla como secret del repo: Settings > Secrets > Actions > SHEET_STOCK_CSV_URL.
4. El workflow .github/workflows/sync-stock.yml corre este script (manual o diario).

Uso local:
    python scripts/sync_sheet.py "https://docs.google.com/spreadsheets/.../export?format=csv"
"""
import csv
import sys
from pathlib import Path
from urllib.request import urlopen

BASE = Path(__file__).resolve().parent.parent
DESTINO = BASE / "docs" / "data" / "stock.csv"
COLUMNAS = ["sku", "nombre", "marca", "auto_compatible", "tipo", "precio_costo",
            "precio_venta", "stock", "stock_minimo", "foto", "publicado", "texto_auto"]


def main(url):
    with urlopen(url, timeout=30) as r:
        texto = r.read().decode("utf-8-sig")
    filas = list(csv.DictReader(texto.splitlines()))
    faltan = [c for c in COLUMNAS if c not in (filas[0].keys() if filas else [])]
    if faltan:
        print(f"ERROR: al Sheet le faltan columnas: {faltan}")
        sys.exit(1)
    with open(DESTINO, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNAS)
        w.writeheader()
        for r in filas:
            if (r.get("sku") or "").strip():
                w.writerow({c: (r.get(c) or "").strip() for c in COLUMNAS})
    print(f"OK: {len(filas)} filas -> {DESTINO}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    main(sys.argv[1])
