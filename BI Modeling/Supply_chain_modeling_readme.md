# Logistics Optimization Project

## Descripción
Este proyecto implementa un modelo de asignación de rutas y transportistas basado en métricas críticas: **demanda anual, valor de inventario, lead time y costo de envío (freight)**.  
La lógica se materializa en PostgreSQL mediante la vista `logistics_summary`, y se complementa con reglas de negocio en Python para asignar transportistas a rutas de manera óptima.

---

## Rutas y Asignación Estratégica

- **Ruta 1**  
  Países con condiciones favorables (bajo lead time, bajo costo, demanda moderada).  
  Se asigna a **Transportista 1**, optimizando rapidez y eficiencia.

- **Ruta 2**  
  Países con condiciones intermedias (moderado lead time, costos medios, demanda moderada).  
  Se asigna a **Transportista 2**, balanceando confiabilidad y costo.

- **Ruta 3**  
  Países con condiciones críticas (alto lead time, alto costo, alta demanda y valor).  
  Se asigna a **Transportista 3**, especializado en rutas complejas y de alto riesgo logístico.

---

## Impacto Esperado

- **Reducción de costos** en rutas de alta demanda al asignar transportistas más eficientes.  
- **Mejora en tiempos de entrega promedio** en países críticos.  
- **Mayor confiabilidad y control** en rutas de alto riesgo logístico.  

---

## Arquitectura de Datos

- **Silver Layer**: Tablas limpias (`orders_final_valid`, `customers_clean`, `order_details_valid`, `products_clean`).  
- **Materialized View**: `logistics_summary` con cálculos logísticos clave.  
- **Gold Layer**: Métricas derivadas persistidas desde Python (`delay_by_employee`, `productivity_by_team`, etc.).  

---

## Uso

1. Ejecutar el query en PostgreSQL para crear la vista:
   ```sql
   CREATE MATERIALIZED VIEW logistics_summary AS
   SELECT 
       o.shipperid,
       p.categoryid AS category,
       c.country,
       SUM(od.quantity) AS annual_demand,
       AVG(p.unitprice) * 0.2 AS holding_cost,
       SUM(od.quantity) AS rotation,
       SUM(p.unitprice * od.quantity) AS inventory_value,
       AVG(o.shippeddate - o.orderdate) AS lead_time_days,
       AVG(o.freight) AS avg_freight
   FROM silver.orders_final_valid o
   JOIN silver.customers_clean c ON o.customerid = c.customerid
   JOIN silver.order_details_valid od ON o.orderid = od.orderid
   JOIN silver.products_clean p ON od.productid = p.productid
   GROUP BY o.shipperid, p.categoryid, c.country;
