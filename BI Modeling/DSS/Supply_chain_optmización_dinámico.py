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


#Keep
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


#DSS DINÁMICO 

import streamlit as st
import pandas as pd

# Supongamos que ya tienes tu DataFrame resumen_transportistas
# con columnas: shipperid, annual_demand, inventory_value, lead_time_days, avg_freight

st.title("Mini DSS Logístico")

# Parámetros dinámicos (solo asignación de rutas)
demanda_umbral = st.slider("Umbral de demanda", 1000, 20000, 10000)
valor_umbral = st.slider("Umbral de valor de inventario", 10000, 100000, 50000)
freight_umbral = st.slider("Umbral de freight", 10, 100, 70)
leadtime_umbral = st.slider("Umbral de lead time (días)", 1, 15, 9)

# Resultados narrativos
st.subheader("Asignación de rutas y transportistas")
asignaciones = []
for _, row in resumen_transportistas.iterrows():
    if (
        row["lead_time_days"] > leadtime_umbral
        and row["avg_freight"] > freight_umbral
        and row["annual_demand"] > demanda_umbral
        and row["inventory_value"] > valor_umbral
    ):
        ruta = "Ruta 3"
        transportista = "Transportista 3"
    elif (
        row["lead_time_days"] <= leadtime_umbral
        and row["avg_freight"] <= freight_umbral
        and row["annual_demand"] >= demanda_umbral/2
        and row["inventory_value"] >= valor_umbral/2
    ):
        ruta = "Ruta 2"
        transportista = "Transportista 2"
    else:
        ruta = "Ruta 1"
        transportista = "Transportista 1"

    asignaciones.append({
        "shipperid": row["shipperid"],
        "ruta": ruta,
        "transportista": transportista,
        "annual_demand": row["annual_demand"],
        "inventory_value": row["inventory_value"],
        "lead_time_days": row["lead_time_days"],
        "avg_freight": row["avg_freight"]
    })
    st.write(f"Transportista {row['shipperid']} asignado a {ruta} → {transportista}")

# Tabla de KPIs por escenario
st.subheader("KPIs por escenario")
df_asignaciones = pd.DataFrame(asignaciones)
kpis = df_asignaciones.groupby("ruta").agg({
    "annual_demand": "sum",
    "inventory_value": "sum",
    "lead_time_days": "mean",
    "avg_freight": "mean"
}).reset_index()

st.dataframe(kpis)

