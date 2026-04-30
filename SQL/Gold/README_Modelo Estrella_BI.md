#  README – Modelo Estrella BI

##  Enfoque de diseño
Este modelo se construyó siguiendo un enfoque **business-driven**:
- Se definieron primero las **preguntas de negocio** (ventas, costos, inventarios, supply chain, consumo).
- A partir de esas preguntas se diseñaron las **dimensiones** que permiten responderlas.
- Finalmente se crearon las **fact tables**, que almacenan las métricas clave y se relacionan con las dimensiones en un esquema estrella.

---

##  Dimensiones creadas

### Dim_Categoría
### Dim_cliente 
### Dim_región
### Dim_tiempo
### Dim_producto

## Facts creadas 

### Fact_sales ¿Cuánto vendimos?, ¿qué descuentos aplicamos?, ¿qué ingresos netos se generaron?
### Fact_costos ¿Cuáles son los costos de pedido, almacenamiento y transporte?
### Fact_inventory ¿Cuál es el nivel óptimo de inventario?, ¿cuál es su valor monetario?
### Fact_supplychain ¿Cuál es el tiempo de entrega?, ¿qué porcentaje de órdenes llegan a tiempo?, ¿cuánto cuesta la logística?
### Fact_consumption ¿Qué consumen los clientes?, ¿cuál es la frecuencia y el valor del consumo?


