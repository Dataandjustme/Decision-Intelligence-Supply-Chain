import pandas as pd
import numpy as np
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:@localhost:/")


# 2. Definir funciones de clasificación (van aquí, antes de usarlas)
def clasificar_demanda(demanda):
    if demanda > 10000:
        return "alta"
    elif demanda >= 5000:
        return "moderada"
    else:
        return "baja"

def clasificar_costo(costo):
    if costo > 3:
        return "alto"
    elif costo >= 1.5:
        return "moderado"
    else:
        return "bajo"

def clasificar_rotacion(rotacion):
    if rotacion > 8:
        return "alta"
    elif rotacion >= 4:
        return "moderada"
    else:
        return "baja"

def clasificar_valor(valor):
    if valor > 50000:
        return "alto"
    elif valor >= 20000:
        return "moderado"
    else:
        return "baja"

def clasificar_leadtime(dias):
    if dias > 9:
        return "alto"
    elif dias >= 5:
        return "moderado"
    else:
        return "bajo"

#Definir query 

query_EOQ = '''
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
'''
    

df = pd.read_sql(query_EOQ, engine)

df["demanda_clas"] = df["annual_demand"].apply(clasificar_demanda)
df["costo_clas"] = df["holding_cost"].apply(clasificar_costo)
df["rotacion_clas"] = df["rotation"].apply(clasificar_rotacion)
df["valor_clas"] = df["inventory_value"].apply(clasificar_valor)
df["leadtime_clas"] = df["lead_time_days"].apply(clasificar_leadtime)

print(df.head())


#Definir rutas 

rutas = {
    "Ruta 1": df[df["leadtime_clas"] == "bajo"]["country"].unique().tolist(),
    "Ruta 2": df[df["leadtime_clas"] == "moderado"]["country"].unique().tolist(),
    "Ruta 3": df[df["leadtime_clas"] == "alto"]["country"].unique().tolist(),
}

print(rutas)

# Resumen por transportista
resumen_transportistas = df.groupby("shipperid").agg({
    "annual_demand": "sum",
    "inventory_value": "sum",
    "lead_time_days": "mean",
    "avg_freight": "mean"
}).reset_index()

print(resumen_transportistas)

for _, row in resumen_transportistas.iterrows():
    if (
        row["lead_time_days"] > 9
        and row["avg_freight"] > 70
        and row["annual_demand"] > 10000
        and row["inventory_value"] > 50000
    ):
        ruta = "Ruta 3"
        transportista = "Transportista 3"
    elif (
        row["lead_time_days"] <= 9
        and row["avg_freight"] <= 70
        and row["annual_demand"] >= 5000
        and row["inventory_value"] >= 20000
    ):
        ruta = "Ruta 2"
        transportista = "Transportista 2"
    else:
        ruta = "Ruta 1"
        transportista = "Transportista 1"

    print(f"{ruta} {rutas[ruta]} → {transportista}")


#Resumen de logistica
DF_logistics ='''
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
'''

