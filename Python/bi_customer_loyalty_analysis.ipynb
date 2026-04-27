from sqlalchemy import create_engine
import pandas as pd

# Ajusta con tus credenciales reales
engine = create_engine("postgresql+psycopg2://postgres:@localhost:/")


# BQ: ¿Qué segmentos de clientes tienen mayor potencial de fidelización?

df_products = pd.read_sql("SELECT * FROM gold.sales_margin_by_product;", engine)
df_customers = pd.read_sql("SELECT * FROM gold.sales_margin_by_customer;", engine)
df_categories = pd.read_sql("SELECT * FROM gold.sales_margin_by_category;", engine)

df_customers = pd.read_sql("SELECT * FROM gold.sales_margin_by_customer;", engine)
print(df_customers.head())


# Calcular participación en margen
df_customers["pct_margin"] = df_customers["total_margin"] / df_customers["total_margin"].sum()

# Normalizar frecuencia de pedidos usando total_orders
df_customers["order_freq"] = df_customers["total_orders"] / df_customers["total_orders"].max()

# Score de fidelización (60% margen, 40% frecuencia)
df_customers["loyalty_score"] = (0.6 * df_customers["pct_margin"]) + (0.4 * df_customers["order_freq"])

# Ordenar por score
df_loyalty = df_customers.sort_values("loyalty_score", ascending=False)
print(df_loyalty.head(10))


import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
plt.bar(df_loyalty["companyname"].head(10), df_loyalty["loyalty_score"].head(10), color="skyblue")
plt.xticks(rotation=90)
plt.title("Top 10 clientes por potencial de fidelización")
plt.ylabel("Loyalty Score")
plt.show()

# AQ: ¿Qué patrones de consumo se observan en clientes?

import numpy as np

# Ticket promedio por cliente
df_customers["avg_ticket"] = df_customers["total_margin"] / df_customers["total_orders"]

# Clasificación de patrones de consumo
conditions = [
    (df_customers["total_margin"] > df_customers["total_margin"].median()) & (df_customers["total_orders"] > df_customers["total_orders"].median()),
    (df_customers["total_margin"] > df_customers["total_margin"].median()) & (df_customers["total_orders"] <= df_customers["total_orders"].median()),
    (df_customers["total_margin"] <= df_customers["total_margin"].median()) & (df_customers["total_orders"] > df_customers["total_orders"].median()),
    (df_customers["total_margin"] <= df_customers["total_margin"].median()) & (df_customers["total_orders"] <= df_customers["total_orders"].median())
]

labels = ["Premium recurrente", "Premium ocasional", "Frecuente bajo ticket", "Ocasional bajo impacto"]

df_customers["consumption_pattern"] = np.select(conditions, labels, default="Otro")

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
sns.scatterplot(data=df_customers, x="total_orders", y="avg_ticket", hue="consumption_pattern")
plt.title("Patrones de consumo de clientes")
plt.xlabel("Número de órdenes")
plt.ylabel("Ticket promedio")
plt.show()

# AQ: ¿Cuál es el ticket promedio por segmento de cliente?

# Ticket promedio por cliente
df_customers["avg_ticket"] = df_customers["total_margin"] / df_customers["total_orders"]

# Segmentar clientes en 4 grupos según loyalty_score
df_customers["segment"] = pd.qcut(df_customers["loyalty_score"], q=4, labels=["Bajo", "Medio", "Alto", "Premium"])

# Ticket promedio por segmento
ticket_segment = df_customers.groupby("segment")["avg_ticket"].mean().reset_index()
print(ticket_segment)


import matplotlib.pyplot as plt

plt.figure(figsize=(8,6))
plt.bar(ticket_segment["segment"], ticket_segment["avg_ticket"], color="green")
plt.title("Ticket promedio por segmento de cliente")
plt.ylabel("Ticket promedio")
plt.show()

#AQ: ¿Qué porcentaje de clientes premium repite compras en un periodo de 3 meses?

query_orders = """
SELECT o.customerid, o.orderid, o.orderdate
FROM silver.orders_final_valid o;
"""
df_orders = pd.read_sql(query_orders, engine)
df_orders["orderdate"] = pd.to_datetime(df_orders["orderdate"])

premium_ids = df_customers[df_customers["loyalty_score"] >= df_customers["loyalty_score"].quantile(0.75)]["customerid"].unique()

# Filtrar órdenes de clientes premium
df_premium_orders = df_orders[df_orders["customerid"].isin(premium_ids)]

# Ordenar por cliente y fecha
df_premium_orders = df_premium_orders.sort_values(["customerid","orderdate"])

# Diferencia en días entre compras consecutivas
df_premium_orders["days_diff"] = df_premium_orders.groupby("customerid")["orderdate"].diff().dt.days

# Marcar repetición si la diferencia <= 90 días
df_premium_orders["repeat_purchase"] = df_premium_orders["days_diff"].apply(lambda x: 1 if x is not None and x <= 90 else 0)

# Calcular porcentaje de clientes premium que repiten
repeat_customers = df_premium_orders.groupby("customerid")["repeat_purchase"].max().reset_index()
pct_repeat = repeat_customers["repeat_purchase"].mean() * 100

# AQ: ¿Qué productos son más consumidos por clientes premium?

# Órdenes con fechas y clientes
query_orders = "SELECT orderid, customerid, orderdate FROM silver.orders_final_valid;"
df_orders = pd.read_sql(query_orders, engine)

# Detalles de productos
query_details = "SELECT orderid, productid, unitprice, quantity, discount FROM silver.order_details_valid;"
df_details = pd.read_sql(query_details, engine)

# Productos
query_products = "SELECT productid, productname FROM silver.products_valid;"
df_products = pd.read_sql(query_products, engine)

premium_ids = df_customers[df_customers["loyalty_score"] >= df_customers["loyalty_score"].quantile(0.75)]["customerid"].unique()
df_premium_orders = df_orders[df_orders["customerid"].isin(premium_ids)]

# Merge órdenes premium con detalles
df_premium_details = df_premium_orders.merge(df_details, on="orderid", how="inner")

# Merge con nombres de productos
df_premium_details = df_premium_details.merge(df_products, on="productid", how="left")

# Calcular cantidad total consumida por producto
product_consumption = df_premium_details.groupby("productname")["quantity"].sum().reset_index()
product_consumption = product_consumption.sort_values("quantity", ascending=False)

print(product_consumption.head(10))


import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))
plt.bar(product_consumption["productname"].head(10), product_consumption["quantity"].head(10), color="steelblue")
plt.xticks(rotation=90)
plt.title("Top 10 productos más consumidos por clientes premium")
plt.ylabel("Cantidad total")
plt.show()

#KPI % de clientes leales vs no leales.

# Definir clientes leales como el cuartil superior de loyalty_score
threshold = df_customers["loyalty_score"].quantile(0.75)
df_customers["loyal_segment"] = np.where(
    df_customers["loyalty_score"] >= threshold, "Leales", "No Leales"
)

loyal_summary = df_customers["loyal_segment"].value_counts(normalize=True) * 100
print(loyal_summary)

import matplotlib.pyplot as plt

plt.figure(figsize=(6,6))
plt.pie(loyal_summary, labels=loyal_summary.index, autopct="%1.1f%%", colors=["gold","lightgray"])
plt.title("Porcentaje de clientes leales vs no leales")
plt.show()

# KPI Tasa de retención por costo por segmento  leal vs no leal 

# Definir clientes leales como el cuartil superior de loyalty_score
threshold = df_customers["loyalty_score"].quantile(0.75)
df_customers["loyal_segment"] = np.where(
    df_customers["loyalty_score"] >= threshold, "Leales", "No Leales"
)

query_orders = """
SELECT orderid, customerid, orderdate, freight
FROM silver.orders_final_valid;
"""
df_orders = pd.read_sql(query_orders, engine)
df_orders["orderdate"] = pd.to_datetime(df_orders["orderdate"])

# Merge con segmento de lealtad
df_orders = df_orders.merge(df_customers[["customerid","loyal_segment"]], on="customerid", how="left")

# Diferencia en días entre compras consecutivas
df_orders = df_orders.sort_values(["customerid","orderdate"])
df_orders["days_diff"] = df_orders.groupby("customerid")["orderdate"].diff().dt.days

# Marcar repetición si la diferencia <= 90 días
df_orders["repeat_purchase"] = df_orders["days_diff"].apply(lambda x: 1 if x is not None and x <= 90 else 0)

# Calcular tasa de retención por segmento
retention_summary = df_orders.groupby("loyal_segment")["repeat_purchase"].mean().reset_index()
retention_summary["retention_rate"] = retention_summary["repeat_purchase"] * 100

# Calcular costo promedio por segmento
cost_summary = df_orders.groupby("loyal_segment")["freight"].mean().reset_index()

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(figsize=(8,6))

# Barras para tasa de retención
ax1.bar(retention_summary["loyal_segment"], retention_summary["retention_rate"], color="steelblue", alpha=0.7)
ax1.set_ylabel("Tasa de retención (%)", color="steelblue")
ax1.set_title("Tasa de retención y costo por segmento leal vs no leal")

# Línea para costo promedio
ax2 = ax1.twinx()
ax2.plot(cost_summary["loyal_segment"], cost_summary["freight"], color="darkred", marker="o")
ax2.set_ylabel("Costo promedio (freight)", color="darkred")
plt.show()

# H1: Los clientes premium representan el mayor valor de vida (LTV).

df_customers["avg_ticket"] = df_customers["total_margin"] / df_customers["total_orders"]
df_customers["ltv"] = df_customers["avg_ticket"] * df_customers["order_freq"] * df_customers["loyalty_score"]

#Comparar entre segmentos 
threshold = df_customers["loyalty_score"].quantile(0.75)
df_customers["segment"] = np.where(df_customers["loyalty_score"] >= threshold, "Premium", "No Premium")

ltv_summary = df_customers.groupby("segment")["ltv"].mean().reset_index()
print(ltv_summary)

import matplotlib.pyplot as plt

plt.figure(figsize=(6,6))
plt.bar(ltv_summary["segment"], ltv_summary["ltv"], color=["gold","gray"])
plt.title("Valor de vida (LTV) por segmento de cliente")
plt.ylabel("LTV promedio")
plt.show()

# H2: La frecuencia de compra está relacionada con descuentos y cantidad 

# Merge órdenes con detalles
df_orders_details = df_orders.merge(df_details, on="orderid", how="inner")

# Calcular frecuencia de compra por cliente
freq = df_orders.groupby("customerid")["orderid"].count().reset_index(name="order_freq")

# Calcular promedio de descuento y cantidad por cliente
agg = df_orders_details.groupby("customerid")[["discount","quantity"]].mean().reset_index()

# Dataset final
df_analysis = freq.merge(agg, on="customerid", how="left")

#Análisis de correlación 
corr_matrix = df_analysis[["order_freq","discount","quantity"]].corr()
print(corr_matrix)

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(8,6))
sns.scatterplot(data=df_analysis, x="discount", y="order_freq", size="quantity", hue="quantity", palette="viridis")
plt.title("Frecuencia de compra vs descuento (tamaño = cantidad)")
plt.xlabel("Descuento promedio")
plt.ylabel("Frecuencia de compra")
plt.show()

# Crear alias consistentes
df_loyalty_ranking = df_loyalty.copy()                  # Ranking de clientes por potencial de fidelización
df_consumption_patterns = df_customers.copy()           # Patrones de consumo por cliente
df_ticket_segment = ticket_segment.copy()               # Ticket promedio por segmento
df_premium_repeat = repeat_customers.copy()             # Clientes premium que repiten compras en 3 meses
df_premium_products = product_consumption.copy()        # Top productos consumidos por clientes premium
df_loyal_summary = loyal_summary.copy()                 # % de clientes leales vs no leales
df_retention_cost = retention_summary.copy()            # Tasa de retención por segmento
df_cost_summary = cost_summary.copy()                   # Costo promedio por segmento
df_ltv_summary = ltv_summary.copy()                     # LTV promedio por segmento
df_corr_freq_discount = corr_matrix.copy()              # Correlación frecuencia vs descuento vs cantidad

# Exportar a SQL
df_loyalty_ranking.to_sql("gold.loyalty_ranking", engine, if_exists="replace", index=False)
df_consumption_patterns.to_sql("gold.consumption_patterns", engine, if_exists="replace", index=False)
df_ticket_segment.to_sql("gold.ticket_segment", engine, if_exists="replace", index=False)
df_premium_repeat.to_sql("gold.premium_repeat_customers", engine, if_exists="replace", index=False)
df_premium_products.to_sql("gold.premium_products_consumption", engine, if_exists="replace", index=False)
df_loyal_summary.to_sql("gold.loyal_summary", engine, if_exists="replace", index=False)
df_retention_cost.to_sql("gold.retention_rate_by_segment", engine, if_exists="replace", index=False)
df_cost_summary.to_sql("gold.cost_summary_by_segment", engine, if_exists="replace", index=False)
df_ltv_summary.to_sql("gold.ltv_summary_by_segment", engine, if_exists="replace", index=False)
df_corr_freq_discount.to_sql("gold.correlation_freq_discount_quantity", engine, if_exists="replace", index=False)






