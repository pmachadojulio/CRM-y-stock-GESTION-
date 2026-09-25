# CRM-y-stock-GESTION-

Sistema simple para empresa automotriz (chapa y pintura) que ahora vende repuestos de todo tipo.

**Objetivos:** revisar stock, vender, controlar comisiones (2 socios), publicar en la misma página + redes. Simple y estético para el público.

**Demo viva (GitHub Pages):** `https://pmachadojulio.github.io/CRM-y-stock-GESTION-/`
> Se activa en `Settings > Pages > Deploy from branch > main > /docs`.

## Estructura

| Ruta | Qué es |
|---|---|
| `docs/index.html` | Catálogo público (único archivo, sin build, mobile-first) |
| `docs/data/stock.csv` | **Fuente de verdad** del stock (por ahora manual, luego Google Sheet) |
| `docs/data/ventas.csv` | Registro de ventas + atribución de comisión |
| `ROADMAP.md` | Roadmap punto por punto (Fase 0 → 6) |
| `.github/workflows/` | Automatizaciones futuras (Sheet → CSV → Pages) |

## Cómo trabajar de a 2 (reglas)

1. `main` es sagrada. Nada directo: todo por **branch + Pull Request + review del otro**.
2. Branches: `feat/catalogo`, `feat/stock-xxx`, `fix/...`.
3. Issues con labels: `catalogo / stock / ventas / comisiones / diseño / automatizacion`.
4. Stock: editar SOLO `docs/data/stock.csv` (columnas fijas, no renombrar).
5. Ventas: agregar fila en `docs/data/ventas.csv`, nunca borrar.

```powershell
# clonar (tu amigo)
git clone https://github.com/pmachadojulio/CRM-y-stock-GESTION-.git
cd CRM-y-stock-GESTION-
git checkout -b feat/mi-cambio
# ... editar ...
git add -A; git commit -m "feat: mi cambio"; git push -u origin feat/mi-cambio
# -> en GitHub: Compare & pull request, pide review al otro, merge.
```

## Comisiones (regla inicial v1)

- Links: `?v=julio` → WhatsApp Julio (5493534018769) · `?v=matias` → WhatsApp Matías (5493534128663). Sin `?v` → Julio por defecto, asesor muestra `local`.
- El `?v=` se guarda en el navegador (first-touch) + va en el mensaje de WhatsApp.
- Respaldo manual: cupón `JULIO10` / `MATIAS10`.
- Venta local sin atribución: 50/50. Venta con `?v=` o cupón: 100% al vendedor.
- `ventas.csv` manda. Reporte semanal a ojo hasta automatizar (Fase 3).

## Configurar (2 min)

1. ✅ Números ya cableados en `docs/index.html` → `CONFIG.numeros`.
2. Cargar 20 repuestos reales en `docs/data/stock.csv` y pushear. La web se actualiza sola.

Ver `ROADMAP.md` para el paso a paso completo.
