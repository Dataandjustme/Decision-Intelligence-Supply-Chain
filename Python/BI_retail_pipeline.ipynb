from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("postgresql+psycopg2://postgres:@localhost:5432/")

df_products = pd.read_sql("SELECT * FROM gold.sales_margin_by_product;", engine)
df_customers = pd.read_sql("SELECT * FROM gold.sales_margin_by_customer;", engine)
df_categories = pd.read_sql("SELECT * FROM gold.sales_margin_by_category;", engine)

#BQ: ¿Cómo podemos aumentar el margen de ventas en los próximos 6 meses?

#Se asume que algunos clientes aportan un 80% del margen 

df_customers = df_customers.sort_values("total_margin", ascending=False)
df_customers["pct_margin"] = df_customers["total_margin"] / df_customers["total_margin"].sum()
df_customers["cum_pct"] = df_customers["pct_margin"].cumsum()
print(df_customers.head())

import matplotlib.pyplot as plt

# Ordenar clientes por margen
df_customers = df_customers.sort_values("total_margin", ascending=False)
df_customers["pct_margin"] = df_customers["total_margin"] / df_customers["total_margin"].sum()
df_customers["cum_pct"] = df_customers["pct_margin"].cumsum()

# Gráfico Pareto
plt.figure(figsize=(10,6))
plt.bar(df_customers["companyname"], df_customers["pct_margin"], color="skyblue")
plt.plot(df_customers["companyname"], df_customers["cum_pct"], color="red", marker="o")
plt.xticks(rotation=90)
plt.title("Pareto 80/20 - Clientes por margen")
plt.ylabel("Porcentaje de margen")
plt.show()


#Top productos por margen unitario 
top_products = df_products.sort_values("avg_margin_unit", ascending=False).head(10)
print(top_products)

top_products = df_products.sort_values("avg_margin_unit", ascending=False).head(10)

plt.figure(figsize=(10,6))
plt.bar(top_products["productname"], top_products["avg_margin_unit"], color="green")
plt.xticks(rotation=90)
plt.title("Top 10 productos por margen unitario")
plt.ylabel("Margen unitario promedio")
plt.show()


#categorias top
top_categories = df_categories.sort_values("total_margin", ascending=False)
print(top_categories)

top_categories = df_categories.sort_values("total_margin", ascending=False)

plt.figure(figsize=(8,6))
plt.bar(top_categories["categoryname"], top_categories["total_margin"], color="orange")
plt.xticks(rotation=45)
plt.title("Margen total por categoría")
plt.ylabel("Margen total")
plt.show()

#Proyección a 6 meses 
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Query mensual desde PostgreSQL
df_monthly = pd.read_sql("""
SELECT DATE_TRUNC('month', o.orderdate) AS month,
       SUM((od.unitprice - (od.unitprice*0.7)) * od.quantity) AS margin
FROM silver.orders_final_valid o
JOIN silver.order_details_valid od ON o.orderid = od.orderid
JOIN silver.products_valid p ON od.productid = p.productid
GROUP BY month
ORDER BY month;
""", engine)

print(df_monthly.head())   # Validar que sí trae datos

# 2. Modelo de regresión
X = np.arange(len(df_monthly)).reshape(-1,1)
y = df_monthly["margin"].values

model = LinearRegression().fit(X,y)
future = np.arange(len(X), len(X)+6).reshape(-1,1)
predictions = model.predict(future)

print("Proyección de margen próximos 6 meses:", predictions)

# 3. Construir DataFrame con resultados
future_dates = pd.date_range(df_monthly["month"].max() + pd.offsets.MonthBegin(1), periods=6, freq="M")
results = pd.DataFrame({
    "month_future": future_dates,
    "predicted_margin": predictions
})

print(results)

# 4. Visualización
plt.figure(figsize=(10,6))
plt.plot(df_monthly["month"], df_monthly["margin"], marker="o", label="Histórico")
plt.plot(results["month_future"], results["predicted_margin"], marker="x", linestyle="--", color="red", label="Proyección 6 meses")
plt.xticks(rotation=45)
plt.title("Proyección de margen a 6 meses")
plt.ylabel("Margen")
plt.legend()
plt.show()

#AQ:¿Cuál es la tendencia histórica de ingresos y márgenes por categoría de producto?

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# 1. Definir la consulta SQL en una variable
query = """
SELECT 
    DATE_TRUNC('month', o.orderdate) AS month,
    ca.categoryname,
    SUM(od.unitprice * od.quantity) AS total_sales,
    SUM((od.unitprice - (od.unitprice*0.7)) * od.quantity) AS total_margin
FROM silver.orders_final_valid o
JOIN silver.order_details_valid od ON o.orderid = od.orderid
JOIN silver.products_valid p ON od.productid = p.productid
JOIN silver.category_assumptions ca ON p.categoryid = ca.categoryid
GROUP BY month, ca.categoryname
ORDER BY month, ca.categoryname;
"""

# 2. Ejecutar la consulta y traer resultados
df_trend = pd.read_sql(query, engine)

# 3. Visualizar ingresos por categoría
plt.figure(figsize=(12,6))
sns.lineplot(data=df_trend, x="month", y="total_sales", hue="categoryname", marker="o")
plt.title("Tendencia histórica de ingresos por categoría")
plt.ylabel("Ingresos")
plt.xticks(rotation=45)
plt.show()

# 4. Visualizar márgenes por categoría
plt.figure(figsize=(12,6))
sns.lineplot(data=df_trend, x="month", y="total_margin", hue="categoryname", marker="o")
plt.title("Tendencia histórica de márgenes por categoría")
plt.ylabel("Margen")
plt.xticks(rotation=45)
plt.show()

# AQ: ¿Qué productos generan mayor rentabilidad y cuáles menor?

import pandas as pd

# Definir la consulta como string
query = """
SELECT 
    p.productname AS productname,
    SUM(od.unitprice * od.quantity) AS total_sales,
    SUM((od.unitprice - (od.unitprice*0.7)) * od.quantity) AS total_margin,
    AVG((od.unitprice - (od.unitprice*0.7))) AS avg_margin_unit
FROM silver.order_details_valid od
JOIN silver.products_valid p ON od.productid = p.productid
GROUP BY p.productname
ORDER BY total_margin DESC;
"""

# Ejecutar la consulta en Python
df_products = pd.read_sql(query, engine)

# Validar columnas
print(df_products.columns)
print(df_products.head())

import matplotlib.pyplot as plt

# Top 10 productos más rentables
top_products = df_products.sort_values("total_margin", ascending=False).head(10)

plt.figure(figsize=(10,6))
plt.bar(top_products["productname"], top_products["total_margin"], color="green")
plt.xticks(rotation=90)
plt.title("Top 10 productos por rentabilidad (margen total)")
plt.ylabel("Margen total")
plt.show()

# Bottom 10 productos menos rentables
bottom_products = df_products.sort_values("total_margin", ascending=True).head(10)

plt.figure(figsize=(10,6))
plt.bar(bottom_products["productname"], bottom_products["total_margin"], color="red")
plt.xticks(rotation=90)
plt.title("Bottom 10 productos por rentabilidad (margen total)")
plt.ylabel("Margen total")
plt.show()


#AQ: ¿Cuál es la tasa de crecimiento mensual por categoría en los últimos meses?


df_category_query = '''
SELECT 
    DATE_TRUNC('month', o.orderdate) AS month,
    ca.categoryname AS categoryname, 
    SUM(od.unitprice * od.quantity) AS total_sales
FROM silver.orders_final_valid o
JOIN silver.order_details_valid od ON o.orderid = od.orderid
JOIN silver.products_valid p ON od.productid = p.productid
JOIN silver.category_assumptions ca ON p.categoryid = ca.categoryid
GROUP BY month, ca.categoryname
ORDER BY month, ca.categoryname;
'''

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Ejecutar la consulta
df_sales = pd.read_sql(df_category_query, engine)

print(df_sales.columns)
print(df_sales.head())

# Ordenar por categoría y mes
df_sales = df_sales.sort_values(["categoryname", "month"])

# Calcular tasa de crecimiento mensual por categoría
df_sales["growth_rate"] = df_sales.groupby("categoryname")["total_sales"].pct_change()

# Validar resultados
print(df_sales.head())

# Gráfico de líneas por categoría
plt.figure(figsize=(12,6))
sns.lineplot(data=df_sales, x="month", y="growth_rate", hue="categoryname", marker="o")
plt.title("Tasa de crecimiento mensual por categoría")
plt.ylabel("Growth Rate (%)")
plt.xticks(rotation=45)
plt.axhline(0, color="black", linestyle="--")  # línea de referencia en 0
plt.show()

# --- Promedio últimos 6 meses ---
# Filtrar últimos 6 meses
last_months = df_sales["month"].max() - pd.DateOffset(months=6)
df_recent = df_sales[df_sales["month"] >= last_months]

# Promedio de crecimiento por categoría
avg_growth = df_recent.groupby("categoryname")["growth_rate"].mean().reset_index()
print(avg_growth)



# AQ: ¿Qué correlación existe entre promociones y variación en ventas?

df_corr_query = '''
SELECT 
    DATE_TRUNC('month', o.orderdate) AS month,
    ca.categoryname AS categoryname,
    SUM(od.unitprice * od.quantity) AS total_sales,
    SUM(od.discount) AS total_discount
FROM silver.orders_final_valid o
JOIN silver.order_details_valid od ON o.orderid = od.orderid
JOIN silver.products_valid p ON od.productid = p.productid
JOIN silver.category_assumptions ca ON p.categoryid = ca.categoryid
GROUP BY month, ca.categoryname
ORDER BY month, ca.categoryname;
'''


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Ejecutar consulta
df_promo = pd.read_sql(df_corr_query, engine)

# Ordenar
df_promo = df_promo.sort_values(["categoryname", "month"])

# Calcular variación mensual en ventas
df_promo["sales_variation"] = df_promo.groupby("categoryname")["total_sales"].pct_change()

# Calcular correlación entre promociones y variación en ventas
corr_results = df_promo.groupby("categoryname")[["total_discount", "sales_variation"]].corr().iloc[0::2,-1]

print(corr_results)


# Gráfico de dispersión por categoría
plt.figure(figsize=(12,6))
sns.scatterplot(data=df_promo, x="total_discount", y="sales_variation", hue="categoryname")
plt.title("Correlación entre promociones y variación en ventas")
plt.xlabel("Promociones (descuentos)")
plt.ylabel("Variación en ventas (%)")
plt.axhline(0, color="black", linestyle="--")
plt.show()

corr = df_promo[["total_discount","sales_variation"]].corr()
print(corr)


#KPI Margen bruto mensual por categoría.

df_KPI_Margen = '''
SELECT 
    DATE_TRUNC('month', o.orderdate) AS month,
    ca.categoryname AS categoryname,
    SUM(od.unitprice * od.quantity) AS total_sales,
    SUM((od.unitprice - (od.unitprice*0.7)) * od.quantity) AS gross_margin
FROM silver.orders_final_valid o
JOIN silver.order_details_valid od ON o.orderid = od.orderid
JOIN silver.products_valid p ON od.productid = p.productid
JOIN silver.category_assumptions ca ON p.categoryid = ca.categoryid
GROUP BY month, ca.categoryname
ORDER BY month, ca.categoryname;
'''

import pandas as pd

df_margin = pd.read_sql(df_KPI_Margen, engine)

# Validar columnas
print(df_margin.columns)
print(df_margin.head())

# KPI: margen bruto mensual por categoría
df_margin["gross_margin_rate"] = df_margin["gross_margin"] / df_margin["total_sales"]

print(df_margin.head())

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))
sns.lineplot(data=df_margin, x="month", y="gross_margin_rate", hue="categoryname", marker="o")
plt.title("Margen bruto mensual por categoría")
plt.ylabel("Gross Margin Rate (%)")
plt.xticks(rotation=45)
plt.show()

# KPI Tasa de crecimiento mensual de ventas por categoría.

df_KPI_PCT_Margen = '''
SELECT 
    DATE_TRUNC('month', o.orderdate) AS month,
    ca.categoryname AS categoryname,
    SUM(od.unitprice * od.quantity) AS total_sales
FROM silver.orders_final_valid o
JOIN silver.order_details_valid od ON o.orderid = od.orderid
JOIN silver.products_valid p ON od.productid = p.productid
JOIN silver.category_assumptions ca ON p.categoryid = ca.categoryid
GROUP BY month, ca.categoryname
ORDER BY month, ca.categoryname;
'''

import pandas as pd

df_growth = pd.read_sql(df_KPI_PCT_Margen, engine)

# Ordenar por categoría y mes
df_growth = df_growth.sort_values(["categoryname", "month"])

# Calcular tasa de crecimiento mensual por categoría
df_growth["growth_rate"] = df_growth.groupby("categoryname")["total_sales"].pct_change()

print(df_growth.head())


import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))
sns.lineplot(data=df_growth, x="month", y="growth_rate", hue="categoryname", marker="o")
plt.title("Tasa de crecimiento mensual de ventas por categoría")
plt.ylabel("Growth Rate (%)")
plt.xticks(rotation=45)
plt.axhline(0, color="black", linestyle="--")
plt.show()

# H1: El aumento de ventas depende de la rotación de productos de alta demanda y promociones efectivas.

df_h1 = '''
SELECT 
    DATE_TRUNC('month', o.orderdate) AS month,
    ca.categoryname AS categoryname,
    SUM(od.unitprice * od.quantity) AS total_sales,
    SUM(od.quantity) AS total_units,
    SUM(od.discount) AS total_discount
FROM silver.orders_final_valid o
JOIN silver.order_details_valid od ON o.orderid = od.orderid
JOIN silver.products_valid p ON od.productid = p.productid
JOIN silver.category_assumptions ca ON p.categoryid = ca.categoryid
GROUP BY month, ca.categoryname
ORDER BY month, ca.categoryname;
'''

import pandas as pd

df_multi = pd.read_sql(df_h1, engine)

# Variación mensual en ventas
df_multi["sales_variation"] = df_multi.groupby("categoryname")["total_sales"].pct_change()

# Rotación: unidades vendidas / total ventas
df_multi["rotation_rate"] = df_multi["total_units"] / df_multi["total_sales"]

# Promociones: total descuentos normalizados
df_multi["promo_intensity"] = df_multi["total_discount"] / df_multi["total_sales"]

print(df_multi.head())

import seaborn as sns
import matplotlib.pyplot as plt

corr_matrix = df_multi[["sales_variation","rotation_rate","promo_intensity"]].corr()
print(corr_matrix)

sns.heatmap(corr_matrix, annot=True, cmap="coolwarm")
plt.title("Correlación multivariada: ventas, rotación y promociones")
plt.show()

#H2: Los productos gourmet premium tienen mayor margen pero menor volumen.

df_h2 = '''
SELECT 
    p.productname AS productname,
    ca.categoryname AS categoryname,
    SUM(od.unitprice * od.quantity) AS total_sales,
    SUM(od.quantity) AS total_units,
    SUM((od.unitprice - (od.unitprice*0.7)) * od.quantity) AS gross_margin
FROM silver.order_details_valid od
JOIN silver.products_valid p ON od.productid = p.productid
JOIN silver.category_assumptions ca ON p.categoryid = ca.categoryid
GROUP BY p.productname, ca.categoryname
ORDER BY gross_margin DESC;
'''

import seaborn as sns
import matplotlib.pyplot as plt

df_products = pd.read_sql(df_h2, engine)

# Gráfico de dispersión margen vs volumen
plt.figure(figsize=(10,6))
sns.scatterplot(data=df_products, x="total_units", y="gross_margin", hue="categoryname")
plt.title("Relación margen vs volumen por producto")
plt.xlabel("Volumen de ventas (unidades)")
plt.ylabel("Margen bruto")
plt.show()

#H3: Las promociones incrementan ventas a corto plazo pero reducen margen si no se controlan.

df_h3 = '''
SELECT 
    DATE_TRUNC('month', o.orderdate) AS month,
    ca.categoryname AS categoryname,
    SUM(od.unitprice * od.quantity) AS total_sales,
    SUM((od.unitprice - (od.unitprice*0.7)) * od.quantity) AS gross_margin,
    SUM(od.discount) AS total_discount
FROM silver.orders_final_valid o
JOIN silver.order_details_valid od ON o.orderid = od.orderid
JOIN silver.products_valid p ON od.productid = p.productid
JOIN silver.category_assumptions ca ON p.categoryid = ca.categoryid
GROUP BY month, ca.categoryname
ORDER BY month, ca.categoryname;
'''

import seaborn as sns
import matplotlib.pyplot as plt

df_promo_margin = pd.read_sql(df_h3, engine)

# Relación entre promociones y margen
plt.figure(figsize=(10,6))
sns.scatterplot(data=df_promo_margin, x="total_discount", y="gross_margin", hue="categoryname")
plt.title("Relación entre promociones y margen bruto")
plt.xlabel("Promociones (descuentos)")
plt.ylabel("Margen bruto")
plt.show()

#Guardar en Postgresql

# Crear alias consistentes
df_sales_growth = df_sales.copy()                
df_recent_growth = avg_growth.copy()            
df_top_margin = top_products.copy()              
df_promotions_margin_corr = df_promo.copy()      
df_sales_rotation_corr = df_multi.copy()         
df_margin_volume_corr = df_products.copy()  

df_sales_growth.to_sql("gold.category_monthly_sales_growth", engine, if_exists="replace", index=False)
df_recent_growth.to_sql("gold.category_recent_growth", engine, if_exists="replace", index=False)
df_top_margin.to_sql("gold.top_products_margin", engine, if_exists="replace", index=False)
df_promotions_margin_corr.to_sql("gold.promotions_vs_margin_correlation", engine, if_exists="replace", index=False)
df_sales_rotation_corr.to_sql("gold.sales_rotation_promotions_correlation", engine, if_exists="replace", index=False)
df_margin_volume_corr.to_sql("gold.margin_vs_volume_correlation", engine, if_exists="replace", index=False)
     
#Exportar 

# --- Exportar a CSV con ruta completa ---
df_sales_growth.to_csv(r"C:\Users\jg436\OneDrive\Documentos\BI Projects\BI retail Project\gold_category_monthly_sales_growth.csv", index=False)
df_recent_growth.to_csv(r"C:\Users\jg436\OneDrive\Documentos\BI Projects\BI retail Project\gold_category_recent_growth.csv", index=False)
df_top_margin.to_csv(r"C:\Users\jg436\OneDrive\Documentos\BI Projects\BI retail Project\gold_top_products_margin.csv", index=False)
df_promotions_margin_corr.to_csv(r"C:\Users\jg436\OneDrive\Documentos\BI Projects\BI retail Project\gold_promotions_vs_margin_correlation.csv", index=False)
df_sales_rotation_corr.to_csv(r"C:\Users\jg436\OneDrive\Documentos\BI Projects\BI retail Project\gold_sales_rotation_promotions_correlation.csv", index=False)
df_margin_volume_corr.to_csv(r"C:\Users\jg436\OneDrive\Documentos\BI Projects\BI retail Project\gold_margin_vs_volume_correlation.csv", index=False)


