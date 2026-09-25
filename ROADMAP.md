# Roadmap — CRM + Stock + Ventas (chapa y pintura → repuestos)

## Fase 0 — Base colaborativa ✅ (en curso)
- [x] Repo creado + clonado
- [ ] `docs/index.html` + `docs/data/*.csv` iniciales
- [ ] Pages activada (`Settings > Pages > main > /docs`)
- [ ] Amigo agregado como Collaborator (`Maintain`)
- [ ] Protección de `main`: exigir PR + 1 review

## Fase 1 — Catálogo público MVP (esta semana)
- [ ] Cargar 20 SKUs reales en `stock.csv` (foto + precio + compatibilidad)
- [ ] Probar en celular: buscar, filtrar, botón WhatsApp con `?v=`
- [ ] Definir número WhatsApp único + mensaje pre-rellenado
- [ ] Ocultar `stock=0`, badge "Últimas unidades" si `stock<=minimo`

## Fase 2 — Control de stock
- [ ] Pasar `stock.csv` a Google Sheet compartido (mismas columnas)
- [ ] Action: Sheet → `docs/data/stock.csv` → rebuild Pages (botón + diario)
- [ ] Pestaña `movimientos`: fecha, sku, entrada/salida, motivo, quién
- [ ] Regla quiebre: alerta WhatsApp interno si `stock<=minimo`

## Fase 3 — Ventas + comisiones (antes de pautar en redes)
- [ ] Atribución `?v=` + `localStorage` + cupón de respaldo
- [ ] `ventas.csv` como registro único (estado: pendiente/cobrada/entregada)
- [ ] Reporte semanal por vendedor (script chico, suma por `vendedor`)
- [ ] 3 ventas de prueba (web / local / redes) y verificar comisión

## Fase 4 — Publicar en redes en automático
- [ ] Columnas `publicar_si_no, texto_auto` en stock
- [ ] Generar imagen 1080x1080 (precio + SKU + foto) en `/posts/`
- [ ] Posteo asistido (descargar y subir) → luego API Meta / n8n / Buffer
- [ ] Todo link con `?v=` para no perder atribución

## Fase 5 — CRM ligero taller + repuestos (base lista, a probar)
- [x] Panel: pestañas Clientes + Presupuestos (`docs/data/clientes.csv`, `presupuestos.csv`)
- [x] Presupuesto: ítems + mano de obra, total vivo, estados pendiente > en taller > listo > entregada
- [x] Aceptar descuenta stock (una sola vez, al pasar a en taller)
- [x] Pedido web pide nombre/tel → viaja en el WhatsApp y la venta lo guarda (auto-crea ficha)
- [ ] Probar circuito completo con un caso real (cliente + presupuesto + aceptar + venta)
- [ ] Migrar a Supabase/Firebase solo cuando Sheet/CSV duela (>1000 SKUs)

## Fase 6 — Pulido / escala
- [ ] Dominio propio + Instagram Shopping / MercadoLibre espejo
- [ ] Cobros: link MercadoPago / transferencia con comprobante por WA
- [ ] Métricas: más visto, más consultado, quiebre, comisión mensual

---
**Regla de oro:** Fase 3 (comisiones) antes que Fase 4 (redes). Si publican sin atribución, pierden plata.
