"""Genera textos de publicación para redes (Fase 4, paso 1: solo texto).

Lee docs/data/stock.csv (publicado=si, stock>0) y genera un .txt por producto
en posts/ con caption listo para Instagram/Facebook/WhatsApp, con link
de atribución para cada vendedor.

Uso:
    python generar_posts.py            # genera posts/
    python generar_posts.py --v julio  # solo captions de un vendedor

La imagen 1080x1080 viene en el paso 2 (requiere fotos reales).
"""
import csv
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
CSV = BASE / "docs" / "data" / "stock.csv"
OUT = BASE / "posts"
WEB = "https://pmachadojulio.github.io/repuestero/"


def caption(r, vendedor):
    precio = float(r["precio_venta"] or 0)
    precio_txt = f"${precio:,.0f}".replace(",", ".")
    link = f"{WEB}?v={vendedor}"
    return (
        f"🔧 {r['nombre']} ({r['sku']})\n"
        f"🚗 Compatible: {r['auto_compatible'] or 'consultanos'}\n"
        f"💰 {precio_txt} — stock: {r['stock']} u.\n"
        f"{(r['texto_auto'] or '').strip()}\n"
        f"📲 Pedilo acá: {link}\n"
        f"#Repuestero #ChapaYPintura"
    )


def main():
    solo = None
    if "--v" in sys.argv:
        solo = sys.argv[sys.argv.index("--v") + 1].lower()
    vendedores = [solo] if solo else ["julio", "matias"]
    OUT.mkdir(exist_ok=True)
    n = 0
    with open(CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if (r.get("publicado") or "").strip().lower() != "si":
                continue
            try:
                if int(float(r.get("stock") or 0)) <= 0:
                    continue
            except ValueError:
                continue
            for v in vendedores:
                dest = OUT / f"{r['sku']}_{v}.txt"
                dest.write_text(caption(r, v), encoding="utf-8")
                n += 1
    print(f"OK: {n} captions en {OUT}/")


if __name__ == "__main__":
    main()
