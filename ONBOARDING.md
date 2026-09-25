# Onboarding — CRM y Stock GESTIÓN (para pegar a una IA)

> Matías: copiá todo este archivo y pegáselo a tu IA (ChatGPT, Claude, Gemini, la que uses)
> con el mensaje: "Este es el contexto de nuestro proyecto, ayudame a trabajar en él".

## 1. Qué es

Empresa automotriz de **chapa y pintura** que se expande a **venta de repuestos de todo tipo**.
Estamos haciendo un sistema propio, simple y barato (costo $0) que permita:

1. **Revisar y controlar stock** de repuestos.
2. **Vender** (catálogo público estético + pedidos por WhatsApp).
3. **Cobrar comisiones**: somos 2 socios (Julio y Matías), cada venta debe quedar atribuida.
4. **Publicar** en la misma página y en redes (Instagram/Facebook/WhatsApp).
5. A futuro: mini-CRM del taller (clientes, presupuestos, estados).

## 2. Personas y contactos

| Quién | GitHub | WhatsApp | Link de venta |
|---|---|---|---|
| Julio | `pmachadojulio` (dueño del repo) | 5493534018769 | `?v=julio` |
| Matías | `mativ93` | 5493534128663 | `?v=matias` |

- Sin `?v` en el link → el WhatsApp va a Matías por defecto y el asesor figura como `local`.
- Cupones de respaldo: `JULIO10` / `MATIAS10`.

## 3. Links

- Repo: `https://github.com/pmachadojulio/CRM-y-stock-GESTION-`
- Web pública: `https://pmachadojulio.github.io/CRM-y-stock-GESTION-/`
- Panel interno: `https://pmachadojulio.github.io/CRM-y-stock-GESTION-/admin.html` (no indexar)

## 4. Stack (todo gratis)

- **Web:** HTML+CSS+JS puro en `docs/` (sin build, sin framework), publicada con **GitHub Pages** (`main` → carpeta `/docs`).
- **Datos:** CSV (`docs/data/stock.csv` = fuente de verdad, `docs/data/ventas.csv` = ventas). A futuro se migra a Google Sheet con sync automático (esqueleto ya existe).
- **Sin backend ni base de datos** hasta que duela (>1000 SKUs).

## 5. Estructura actual del repo

```
docs/index.html          # catálogo público (buscador, filtros, WhatsApp con atribución)
docs/admin.html          # panel interno: comisiones + pendientes + quiebres (noindex)
docs/data/stock.csv      # 20 repuestos ejemplo. Columnas: sku,nombre,marca,auto_compatible,
                         # tipo,precio_costo,precio_venta,stock,stock_minimo,foto,publicado,texto_auto
docs/data/ventas.csv     # una venta demo. Columnas: fecha,sku,cantidad,monto,canal,
                         # vendedor,estado,comision_pct,comision_monto,comprobante
reporte_comisiones.py    # CLI: python reporte_comisiones.py (regla v1, ver punto 7)
scripts/sync_sheet.py    # esqueleto Fase 2: Sheet -> stock.csv (inactivo hasta tener Sheet)
.github/workflows/sync-stock.yml  # workflow manual/diario para el sync (requiere secret)
README.md / ROADMAP.md   # docs generales y checklist de fases
```

## 6. Reglas de trabajo (obligatorias)

1. `main` es sagrada: **nada directo**, todo por `branch feat/... + Pull Request + review del otro`.
2. Stock: editar SOLO `docs/data/stock.csv`, no renombrar columnas.
3. Ventas: solo agregar filas en `ventas.csv`, nunca borrar ni editar las ajenas.
4. Probar en local antes de pushear:
   ```
   cd docs
   python -m http.server 8000
   # http://localhost:8000/?v=matias
   ```
5. Commits en español, prefijo `feat:` / `fix:` / `chore:`.

## 7. Regla de comisiones v1 (no cambiar sin acordarlo los dos)

- Venta con `?v=julio` o `?v=matias` (o cupón propio) → **100% de la comisión al vendedor**.
- Venta `local` (mostrador, sin atribución) → **50/50**.
- Solo `cobrada`/`entregada` suma comisión; `pendiente` se informa aparte.
- Insistir: **Fase 3 (comisiones) antes que Fase 4 (redes)**. No publicar sin atribución.

## 8. Roadmap (estado al 25/09/2026)

- [x] Fase 0: repo + Pages viva + atribución por vendedor.
- [x] Fase 3 (base): reporte CLI + admin.html.
- [x] Fase 2 (esqueleto): sync Sheet listo para activar.
- [ ] Fase 1: reemplazar los 20 repuestos ejemplo por **repuestos reales** (foto, precio, compatibilidad).
- [ ] Fase 2: pasar stock a Google Sheet compartido y activar sync.
- [ ] Fase 4: generador de posts para redes con link `?v=`.
- [ ] Fase 5: mini-CRM taller (clientes, presupuestos, estados).
- [ ] Fase 6: dominio propio, MercadoPago, MercadoLibre/IG Shopping, métricas.

## 9. Primeras tareas sugeridas para Matías

1. Clonar, correr en local, probar `?v=matias` y mandar un WhatsApp de prueba.
2. Revisar el diseño del catálogo en tu celular y proponer mejoras (es nuestro frente público).
3. Empezar a cargar repuestos reales en `stock.csv` (o armar la lista para el Sheet).
4. Revisar `reporte_comisiones.py` y confirmar que la regla 50/50 te cierra.

## 10. Preguntas que tu IA te va a hacer (tenelas a mano)

- ¿Qué repuestos reales cargamos primero?
- ¿La comisión es % fijo o varía por producto? (hoy: `comision_pct` por fila)
- ¿Un solo WhatsApp o cada uno el suyo? (hoy: cada uno el suyo, default Julio)
- ¿Precios con IVA incluido o más IVA?
