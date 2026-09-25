"""Genera imágenes para redes (Fase 4, paso 2).

- docs/assets/og.jpg (1200x630): imagen de marca para compartir links (og:image).
  Se versiona (la referencia el <head>).
- posts/img/<SKU>.jpg (1080x1080): una por producto publicado con stock.
  NO se versiona (posts/ está en .gitignore); se generan a demanda.

Si existe docs/assets/fotos/<SKU>.jpg|png se incrusta como foto del producto.

Uso:
    python scripts/generar_imagenes.py           # todo
    python scripts/generar_imagenes.py --solo-og # solo marca
    python scripts/generar_imagenes.py --sku ME-001
"""
import csv
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent.parent
CSV = BASE / "docs" / "data" / "stock.csv"
FOTOS = BASE / "docs" / "assets" / "fotos"
OG = BASE / "docs" / "assets" / "og.jpg"
OUT = BASE / "posts" / "img"

FONDO, TINTA, GRIS, NARANJA, VERDE = (
    (243, 245, 248), (24, 34, 48), (93, 108, 130), (154, 52, 18), (22, 163, 74))


def fuentes(tam_titulo, tam_txt):
    try:
        arial = Path(r"C:\Windows\Fonts\arial.ttf")
        arial_b = Path(r"C:\Windows\Fonts\arialbd.ttf")
        return (ImageFont.truetype(str(arial_b), tam_titulo),
                ImageFont.truetype(str(arial), tam_txt),
                ImageFont.truetype(str(arial_b), tam_txt))
    except OSError:
        d = ImageFont.load_default()
        return d, d, d


def texto_centrado(draw, y, texto, font, fill, ancho):
    box = draw.textbbox((0, 0), texto, font=font)
    draw.text(((ancho - (box[2] - box[0])) / 2, y), texto, font=font, fill=fill)
    return y + (box[3] - box[1])


def partir(draw, texto, font, max_ancho, max_lineas=3):
    palabras, lineas, actual = texto.split(), [], ""
    for p in palabras:
        prueba = (actual + " " + p).strip()
        if draw.textlength(prueba, font=font) <= max_ancho:
            actual = prueba
        else:
            lineas.append(actual)
            actual = p
            if len(lineas) == max_lineas - 1:
                break
    lineas.append(actual)
    return [l for l in lineas if l][:max_lineas]


def marca(draw, ancho, f_tit, f_txt, subtitulo):
    draw.rectangle([0, 0, ancho, 14], fill=NARANJA)
    tam = getattr(f_tit, "size", 90)
    y = texto_centrado(draw, 60, "REPUESTERO", f_tit, NARANJA, ancho)
    y = texto_centrado(draw, y + tam // 2 + 12, subtitulo, f_txt, GRIS, ancho)
    return y


def foto_producto(sku, box):
    for ext in (".jpg", ".jpeg", ".png"):
        p = FOTOS / f"{sku}{ext}"
        if p.exists():
            img = Image.open(p).convert("RGB")
            img.thumbnail(box)
            return img
    return None


def placa_producto(r):
    W = H = 1080
    img = Image.new("RGB", (W, H), FONDO)
    d = ImageDraw.Draw(img)
    f_tit, f_txt, f_bold = fuentes(92, 44)
    f_precio, _, _ = fuentes(150, 44)
    y = marca(d, W, f_tit, f_txt, "Chapa y pintura · Repuestos")
    foto = foto_producto(r["sku"], (880, 380))
    if foto is not None:
        img.paste(foto, ((W - foto.width) // 2, y + 30))
        y += 30 + foto.height + 30
    else:
        y += 40
    for linea in partir(d, r["nombre"], f_tit, W - 160):
        y = texto_centrado(d, y + 10, linea, f_tit, TINTA, W)
    precio = f"${float(r['precio_venta'] or 0):,.0f}".replace(",", ".")
    y = texto_centrado(d, y + 30, precio, f_precio, VERDE, W) + 36
    y = texto_centrado(d, y, f"{r['sku']} · {r.get('auto_compatible') or 'Consultanos'}", f_txt, GRIS, W)
    texto_centrado(d, H - 120, "Pedilo por WhatsApp · Stock real", f_bold, NARANJA, W)
    return img


def placa_og():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    f_tit, f_txt, f_bold = fuentes(130, 48)
    y = marca(d, W, f_tit, f_txt, "Chapa y pintura · Repuestos · Villa María")
    pasos = ["1. Buscá tu repuesto", "2. Armá tu pedido", "3. Enviá por WhatsApp"]
    for i, p in enumerate(pasos):
        texto_centrado(d, y + 40 + i * 80, p, f_bold, TINTA, W)
    return img


def main():
    args = sys.argv[1:]
    OUT.mkdir(parents=True, exist_ok=True)
    if "--solo-og" not in args:
        with open(CSV, encoding="utf-8") as f:
            filas = [r for r in csv.DictReader(f)
                     if (r.get("publicado") or "").strip().lower() == "si" and r.get("sku")]
        if "--sku" in args:
            solo = args[args.index("--sku") + 1]
            filas = [r for r in filas if r["sku"] == solo]
        n = 0
        for r in filas:
            try:
                if int(float(r.get("stock") or 0)) <= 0:
                    continue
            except ValueError:
                continue
            placa_producto(r).save(OUT / f"{r['sku']}.jpg", quality=88)
            n += 1
        print(f"OK: {n} placas en {OUT}/")
    if "--sku" not in args:
        placa_og().save(OG, quality=88)
        print(f"OK: marca -> {OG}")


if __name__ == "__main__":
    main()
