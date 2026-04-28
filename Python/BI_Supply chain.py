from sqlalchemy import create_engine
import pandas as pd

from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:@localhost:5432/")


#BQ: ¿Cómo reducir costos de transporte sin afectar tiempos de entrega?
query_transport = """
SELECT o.orderid, o.shipperid, o.freight, o.orderdate, o.shippeddate, c.country
FROM silver.orders_final_valid o
JOIN silver.customers_clean c
    ON o.customerid = c.customerid;
"""
df_transport = pd.read_sql(query_transport, engine)

# Convertir fechas
df_transport["orderdate"] = pd.to_datetime(df_transport["orderdate"])
df_transport["shippeddate"] = pd.to_datetime(df_transport["shippeddate"])

# Calcular tiempo de entrega
df_transport["delivery_days"] = (df_transport["shippeddate"] - df_transport["orderdate"]).dt.days

# Agrupar por transportista y país
transport_analysis = (
    df_transport.groupby(["shipperid", "country"])
    .agg(
        avg_cost=("freight", "mean"),
        avg_delivery_days=("delivery_days", "mean"),
        total_orders=("orderid", "count")
    )
    .reset_index()
    .sort_values("avg_cost", ascending=False)
)

# KPI Accountability: costo promedio / tiempo promedio
transport_analysis["kpi_accountability"] = transport_analysis["avg_cost"] / transport_analysis["avg_delivery_days"]

print("Análisis transporte (costo vs tiempo):")
print(transport_analysis)

import matplotlib.pyplot as plt

# Agrupar por país
country_analysis = (
    df_transport.groupby("country")
    .agg(
        avg_cost=("freight", "mean"),
        avg_delivery_days=("delivery_days", "mean")
    )
    .reset_index()
)

# Gráfico de barras comparando costo y tiempo
fig, ax1 = plt.subplots(figsize=(10,6))

# Barras de costo promedio
ax1.bar(country_analysis["country"], country_analysis["avg_cost"], color="steelblue", alpha=0.7, label="Costo promedio")

# Barras de tiempo promedio (superpuestas con otro eje)
ax2 = ax1.twinx()
ax2.plot(country_analysis["country"], country_analysis["avg_delivery_days"], color="darkorange", marker="o", label="Tiempo promedio (días)")

# Etiquetas y título
ax1.set_xlabel("País")
ax1.set_ylabel("Costo promedio por envío")
ax2.set_ylabel("Tiempo promedio de entrega (días)")
plt.title("Costo vs Tiempo de entrega por país")

# Leyendas
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")

plt.show()

#AQ: ¿Cuál es el costo promedio por envío y cómo varía según transportista y región?

# Agrupar por transportista y país
cost_analysis = (
    df_transport.groupby(["shipperid", "country"])
    .agg(
        avg_cost=("freight", "mean"),
        total_orders=("orderid", "count")
    )
    .reset_index()
    .sort_values("avg_cost", ascending=False)
)

print(cost_analysis.head())


import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))

# Gráfico de barras agrupadas por país
for shipper in cost_analysis["shipperid"].unique():
    subset = cost_analysis[cost_analysis["shipperid"] == shipper]
    plt.bar(subset["country"], subset["avg_cost"], label=f"Transportista {shipper}")

plt.xlabel("País")
plt.ylabel("Costo promedio por envío")
plt.title("Costo promedio por envío según transportista y país")
plt.legend()
plt.xticks(rotation=45)
plt.show()

# AQ: ¿Cuál es el tiempo promedio de entrega por transportista?

# Calcular tiempo de entrega en días
df_transport["delivery_days"] = (df_transport["shippeddate"] - df_transport["orderdate"]).dt.days

# Agrupar por transportista
delivery_analysis = (
    df_transport.groupby("shipperid")
    .agg(
        avg_delivery_days=("delivery_days", "mean"),
        total_orders=("orderid", "count")
    )
    .reset_index()
    .sort_values("avg_delivery_days", ascending=True)
)

print("Tiempo promedio de entrega por transportista:")
print(delivery_analysis)

import matplotlib.pyplot as plt

plt.figure(figsize=(8,6))
plt.bar(delivery_analysis["shipperid"].astype(str), delivery_analysis["avg_delivery_days"], color="seagreen")

plt.xlabel("Transportista (shipperid)")
plt.ylabel("Tiempo promedio de entrega (días)")
plt.title("Tiempo promedio de entrega por transportista")
plt.xticks(rotation=45)
plt.show()

#BQ: ¿Cuál es el EOQ óptimo para cada categoría de producto?

import pandas as pd
import numpy as np

import pandas as pd
import numpy as np

# Definimos demanda anual y precio unitario aproximado por categoría
df_sales = pd.DataFrame({
    "category": [
        "Bebidas", "Snacks", "Lácteos",
        "Meat & Poultry", "Confections", "Seafood",
        "Condiments", "Produce"
    ],
    "annual_demand": [12000, 8000, 15000, 10000, 9000, 7000, 6000, 11000],
    "unit_price": [10, 5, 8, 12, 6, 15, 4, 7]
})

# Costo de pedido (S) fijo por categoría
df_sales["order_cost"] = 50  # ejemplo: $50 por pedido

# Costo de almacenamiento (H) como 20% del precio unitario
df_sales["holding_cost"] = df_sales["unit_price"] * 0.2

# Calcular EOQ
df_sales["EOQ"] = np.sqrt((2 * df_sales["annual_demand"] * df_sales["order_cost"]) / df_sales["holding_cost"])

print("EOQ óptimo por categoría de producto:")
print(df_sales[["category", "annual_demand", "order_cost", "holding_cost", "EOQ"]])

#AQ: ¿Qué relación existe entre demanda histórica y costos de almacenamiento?

import pandas as pd
import matplotlib.pyplot as plt

# Datos ficticios: demanda anual y costo de almacenamiento por categoría
df_storage = pd.DataFrame({
    "category": [
        "Bebidas", "Snacks", "Lácteos",
        "Meat & Poultry", "Confections", "Seafood",
        "Condiments", "Produce"
    ],
    "annual_demand": [12000, 8000, 15000, 10000, 9000, 7000, 6000, 11000],
    "holding_cost": [2.0, 1.0, 1.6, 2.4, 1.2, 3.0, 0.8, 1.4]  # costo por unidad/año
})

# Visualización: scatter demanda vs costo de almacenamiento
plt.figure(figsize=(8,6))
plt.scatter(df_storage["annual_demand"], df_storage["holding_cost"], color="darkblue")

for i, row in df_storage.iterrows():
    plt.text(row["annual_demand"], row["holding_cost"], row["category"], fontsize=9)

plt.xlabel("Demanda anual (unidades)")
plt.ylabel("Costo de almacenamiento por unidad ($/año)")
plt.title("Relación entre demanda histórica y costos de almacenamiento")
plt.show()

#AQ: ¿Qué nivel de inventario minimiza costos por catgeoria sin generar quiebres de stock?

import pandas as pd
import numpy as np


df_inventory = pd.DataFrame({
    "category": [
        "Bebidas", "Snacks", "Lácteos",
        "Meat & Poultry", "Confections", "Seafood",
        "Condiments", "Produce"
    ],
    "annual_demand": [12000, 8000, 15000, 10000, 9000, 7000, 6000, 11000],
    "unit_price": [10, 5, 8, 12, 6, 15, 4, 7],
    "lead_time_days": [5, 7, 4, 6, 8, 10, 5, 6]  # tiempo de entrega estimado
})

# Costo de pedido (S) fijo
df_inventory["order_cost"] = 50

# Costo de almacenamiento (H) = 20% del precio unitario
df_inventory["holding_cost"] = df_inventory["unit_price"] * 0.2

# EOQ
df_inventory["EOQ"] = np.sqrt((2 * df_inventory["annual_demand"] * df_inventory["order_cost"]) / df_inventory["holding_cost"])

# Demanda diaria
df_inventory["daily_demand"] = df_inventory["annual_demand"] / 365

# Punto de reorden (ROP)
df_inventory["ROP"] = df_inventory["daily_demand"] * df_inventory["lead_time_days"]

# Nivel óptimo de inventario (EOQ + ROP)
df_inventory["optimal_inventory_level"] = df_inventory["EOQ"] + df_inventory["ROP"]

print(df_inventory[["category", "annual_demand", "EOQ", "ROP", "optimal_inventory_level"]])

import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
plt.bar(df_inventory["category"], df_inventory["optimal_inventory_level"], color="royalblue")

plt.xlabel("Categoría de producto")
plt.ylabel("Nivel óptimo de inventario (unidades)")
plt.title("Nivel óptimo de inventario por categoría")
plt.xticks(rotation=45)
plt.show()

# Costo promedio por envío / Tiempo promedio de entrega.

# Ya tenemos df_transport con freight, delivery_days, shipperid y country

# --- Análisis por transportista y país (tu script original) ---
accountability_analysis = (
    df_transport.groupby(["shipperid", "country"])
    .agg(
        avg_cost=("freight", "mean"),
        avg_delivery_days=("delivery_days", "mean"),
        total_orders=("orderid", "count")
    )
    .reset_index()
)

# KPI Accountability = costo promedio / tiempo promedio
accountability_analysis["kpi_accountability"] = accountability_analysis["avg_cost"] / accountability_analysis["avg_delivery_days"]

print("KPI Accountability por transportista y país:")
print(accountability_analysis[["shipperid", "country", "avg_cost", "avg_delivery_days", "kpi_accountability"]])

import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))
for shipper in accountability_analysis["shipperid"].unique():
    subset = accountability_analysis[accountability_analysis["shipperid"] == shipper]
    plt.bar(subset["country"], subset["kpi_accountability"], label=f"Transportista {shipper}")

plt.xlabel("País")
plt.ylabel("KPI Accountability (Costo/tiempo)")
plt.title("Costo promedio por envío / Tiempo promedio de entrega (por país)")
plt.legend()
plt.xticks(rotation=45)
plt.show()


# --- NUEVO: Análisis global por transportista ---
global_accountability = (
    df_transport.groupby("shipperid")
    .agg(
        global_avg_cost=("freight", "mean"),
        global_avg_delivery_days=("delivery_days", "mean"),
        total_orders=("orderid", "count")
    )
    .reset_index()
)

global_accountability["global_kpi_accountability"] = global_accountability["global_avg_cost"] / global_accountability["global_avg_delivery_days"]

print("\nKPI Accountability global por transportista:")
print(global_accountability[["shipperid", "global_avg_cost", "global_avg_delivery_days", "global_kpi_accountability"]])

# Visualización global
plt.figure(figsize=(8,6))
plt.bar(global_accountability["shipperid"], global_accountability["global_kpi_accountability"], color=["orange","blue","green"])
plt.xlabel("Transportista")
plt.ylabel("KPI Accountability Global (Costo/tiempo)")
plt.title("Costo promedio por envío / Tiempo promedio de entrega (global por transportista)")
plt.show()

#H1: EOQ depende de demanda promedio y costo de almacenamiento.


import matplotlib.pyplot as plt

# Usamos df_sales o df_inventory ya definido con annual_demand y holding_cost
plt.figure(figsize=(8,6))
plt.scatter(df_inventory["annual_demand"], df_inventory["holding_cost"], 
            s=df_inventory["EOQ"], color="royalblue", alpha=0.6)

# Etiquetas de categorías
for i, row in df_inventory.iterrows():
    plt.text(row["annual_demand"], row["holding_cost"], row["category"], fontsize=9)

plt.xlabel("Demanda anual (unidades)")
plt.ylabel("Costo de almacenamiento por unidad ($/año)")
plt.title("Relación bivariada: Demanda vs Costo de almacenamiento (tamaño = EOQ)")
plt.show()

#H2: Variabilidad en tiempos se debe a transportistas y zonas geográficas.

import matplotlib.pyplot as plt

# Agrupamos por transportista y país
delivery_variability = (
    df_transport.groupby(["shipperid", "country"])
    .agg(
        avg_delivery_days=("delivery_days", "mean"),
        std_delivery_days=("delivery_days", "std"),
        total_orders=("orderid", "count")
    )
    .reset_index()
)

print(delivery_variability)

# Visualización: barras con error (variabilidad)
plt.figure(figsize=(12,6))
for shipper in delivery_variability["shipperid"].unique():
    subset = delivery_variability[delivery_variability["shipperid"] == shipper]
    plt.bar(subset["country"], subset["avg_delivery_days"], 
            yerr=subset["std_delivery_days"], capsize=5, label=f"Transportista {shipper}")

plt.xlabel("País")
plt.ylabel("Tiempo promedio de entrega (días)")
plt.title("Variabilidad en tiempos de entrega por transportista y país")
plt.legend()
plt.xticks(rotation=45)
plt.show()

# Crear alias del DataFrame
df = df_transport.copy()

# Guardar en PostgreSQL
# Supongamos que ya tienes definido el objeto `engine` con SQLAlchemy
df.to_sql(
    name="transport_analysis_results",   # nombre de la tabla destino
    con=engine,                          # conexión al motor PostgreSQL
    if_exists="replace",                 # reemplazar si ya existe
    index=False                          # no guardar el índice como columna
)

print("DataFrame guardado en PostgreSQL como 'transport_analysis_results'")

accountability_analysis.to_sql("accountability_analysis", con=engine, if_exists="replace", index=False)
global_accountability.to_sql("global_accountability", con=engine, if_exists="replace", index=False)
df_sales.to_sql("sales_eoq", con=engine, if_exists="replace", index=False)
df_inventory.to_sql("inventory_optimal", con=engine, if_exists="replace", index=False)


# Exportar cada DataFrame relevante a CSV
df_transport.to_csv(f"{ruta}\\df_transport.csv", index=False)
accountability_analysis.to_csv(f"{ruta}\\accountability_analysis.csv", index=False)
global_accountability.to_csv(f"{ruta}\\global_accountability.csv", index=False)
df_sales.to_csv(f"{ruta}\\sales_eoq.csv", index=False)
df_inventory.to_csv(f"{ruta}\\inventory_optimal.csv", index=False)
delivery_analysis.to_csv(f"{ruta}\\delivery_analysis.csv", index=False)
cost_analysis.to_csv(f"{ruta}\\cost_analysis.csv", index=False)
country_analysis.to_csv(f"{ruta}\\country_analysis.csv", index=False)
delivery_variability.to_csv(f"{ruta}\\delivery_variability.csv", index=False)

print("Todos los DataFrames han sido exportados a CSV en la carpeta Supply Chain\\Csvs")

