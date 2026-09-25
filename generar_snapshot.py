"""Genera docs/productos.html: snapshot ESTÁTICO del catálogo para SEO.

El catálogo principal se arma con JavaScript (los buscadores ven poco).
Esta página lista los mismos productos en HTML plano: indexable sin JS
y útil como fallback. Regenerar cada vez que cambie el stock:

    python generar_snapshot.py
"""
import csv
import html
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent
CSV = BASE / "docs" / "data" / "stock.csv"
DEST = BASE / "docs" / "productos.html"
WEB = "https://pmachadojulio.github.io/repuestero/"


def main():
    with open(CSV, encoding="utf-8") as f:
        items = [r for r in csv.DictReader(f)
                 if (r.get("publicado") or "").strip().lower() == "si" and r.get("sku")]
    items.sort(key=lambda r: (r.get("tipo") or "", r.get("nombre") or ""))
    hoy = date.today().isoformat()
    lis = []
    for r in items:
        try:
            precio = float(r.get("precio_venta") or 0)
        except ValueError:
            precio = 0
        try:
            stock = int(float(r.get("stock") or 0))
        except ValueError:
            stock = 0
        disp = "En stock" if stock > 0 else "Sin stock"
        lis.append(
            f'    <li itemscope itemtype="https://schema.org/Product">\n'
            f'      <h2 itemprop="name">{html.escape(r.get("nombre", ""))}</h2>\n'
            f'      <p>SKU: <span itemprop="sku">{html.escape(r.get("sku", ""))}</span> · '
            f'Marca: {html.escape(r.get("marca", ""))} · Rubro: {html.escape(r.get("tipo", ""))}</p>\n'
            f'      <p>Compatible: {html.escape(r.get("auto_compatible", ""))}</p>\n'
            f'      <p itemprop="offers" itemscope itemtype="https://schema.org/Offer">'
            f'<span itemprop="priceCurrency" content="ARS">$</span>'
            f'<span itemprop="price" content="{precio:.0f}">{precio:,.0f}</span> · '
            f'<link itemprop="availability" href="https://schema.org/{"InStock" if stock > 0 else "OutOfStock"}">{disp}</p>\n'
            f'    </li>')
    cuerpo = "\n".join(lis)
    DEST.write_text(f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Todos los productos · Repuestero</title>
<meta name="description" content="Lista completa de repuestos: chapa, pintura, mecánica, eléctrico y accesorios. Villa María.">
<link rel="canonical" href="{WEB}productos.html">
<style>body{{font-family:system-ui,sans-serif;max-width:800px;margin:0 auto;padding:24px 16px;color:#182230}}li{{margin-bottom:20px}}h2{{font-size:1rem}}p{{margin:2px 0;color:#5d6c82;font-size:.9rem}}a{{color:#9a3412}}</style>
</head>
<body>
<h1>Todos los productos · Repuestero</h1>
<p>Actualizado: {hoy} · <a href="{WEB}">Volver al catálogo con pedido por WhatsApp</a></p>
<ul>
{cuerpo}
</ul>
</body>
</html>
""", encoding="utf-8")
    print(f"OK: {len(items)} productos -> {DEST}")


if __name__ == "__main__":
    main()
