from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5432/postgres")

#BQ: ¿Qué procesos operativos generan más retrasos y cómo optimizarlos?

# 2. Cargar tabla de órdenes desde la capa silver
query_orders = """
SELECT orderid, customerid, employeeid, orderdate, requireddate, shippeddate, shipperid, freight
FROM silver.orders_final_valid;
"""
df_orders = pd.read_sql(query_orders, engine)

# 3. Convertir fechas a tipo datetime
df_orders["orderdate"] = pd.to_datetime(df_orders["orderdate"])
df_orders["requireddate"] = pd.to_datetime(df_orders["requireddate"])
df_orders["shippeddate"] = pd.to_datetime(df_orders["shippeddate"])

# 4. Calcular métricas de retraso y procesamiento
df_orders["delay_days"] = (df_orders["shippeddate"] - df_orders["requireddate"]).dt.days
df_orders["processing_days"] = (df_orders["shippeddate"] - df_orders["orderdate"]).dt.days

# 5. Retraso promedio por empleado
delay_by_employee = (
    df_orders.groupby("employeeid")["delay_days"]
    .mean()
    .reset_index()
    .sort_values("delay_days", ascending=False)
)

# 6. Retraso promedio por shipper
delay_by_shipper = (
    df_orders.groupby("shipperid")["delay_days"]
    .mean()
    .reset_index()
    .sort_values("delay_days", ascending=False)
)

print("Retraso promedio por empleado:")
print(delay_by_employee)

print("Retraso promedio por shipper:")
print(delay_by_shipper)

#AQ: ¿Cuál es el tiempo promedio de procesamiento por empleado y por orden?

import pandas as pd
from sqlalchemy import create_engine


# 2. Cargar tabla de órdenes
query_orders_1 = """
SELECT orderid, employeeid, orderdate, shippeddate
FROM silver.orders_final_valid;
"""
df_orders = pd.read_sql(query_orders_1, engine)

# 3. Convertir fechas a datetime
df_orders["orderdate"] = pd.to_datetime(df_orders["orderdate"])
df_orders["shippeddate"] = pd.to_datetime(df_orders["shippeddate"])

# 4. Calcular tiempo de procesamiento por orden
df_orders["processing_days"] = (df_orders["shippeddate"] - df_orders["orderdate"]).dt.days

# 5. Promedio por empleado
processing_by_employee = (
    df_orders.groupby("employeeid")["processing_days"]
    .mean()
    .reset_index()
    .sort_values("processing_days", ascending=True)
)

# 6. Promedio global por orden
avg_processing_time = df_orders["processing_days"].mean()

print("Tiempo promedio de procesamiento por empleado:")
print(processing_by_employee)

print(f"Tiempo promedio global de procesamiento por orden: {avg_processing_time:.2f} días")

#AQ: ¿Qué variaciones de productividad existen entre equipos?

import pandas as pd
from sqlalchemy import create_engine


# 2. Cargar tabla de órdenes
query_orders_2 = """
SELECT orderid, employeeid, orderdate, shippeddate
FROM silver.orders_final_valid;
"""
df_orders = pd.read_sql(query_orders_2, engine)

# 3. Convertir fechas
df_orders["orderdate"] = pd.to_datetime(df_orders["orderdate"])
df_orders["shippeddate"] = pd.to_datetime(df_orders["shippeddate"])

# 4. Calcular tiempo de procesamiento
df_orders["processing_days"] = (df_orders["shippeddate"] - df_orders["orderdate"]).dt.days

# 5. Productividad por empleado
productivity_by_employee = (
    df_orders.groupby("employeeid")
    .agg(
        orders_processed=("orderid", "count"),
        avg_processing_days=("processing_days", "mean")
    )
    .reset_index()
)

# diccionario de asignación
employee_team_map = {
    1: "Team A", 2: "Team A", 3: "Team B", 4: "Team B", 5: "Team C"
}
productivity_by_employee["team"] = productivity_by_employee["employeeid"].map(employee_team_map)

# 7. Productividad por equipo
productivity_by_team = (
    productivity_by_employee.groupby("team")
    .agg(
        total_orders=("orders_processed", "sum"),
        avg_processing_days=("avg_processing_days", "mean"),
        std_processing_days=("avg_processing_days", "std")
    )
    .reset_index()
)

print("Productividad por empleado:")
print(productivity_by_employee)

print("Productividad por equipo:")
print(productivity_by_team)

import matplotlib.pyplot as plt
import seaborn as sns

# 1. Barras comparativas
plt.figure(figsize=(8,6))
sns.barplot(data=productivity_by_team, x="team", y="total_orders", color="skyblue")
plt.ylabel("Órdenes procesadas")
plt.title("Órdenes procesadas por equipo")
plt.show()

#Boxplot de tiempos 
plt.figure(figsize=(8,6))
sns.boxplot(data=productivity_by_employee, x="team", y="avg_processing_days")
plt.ylabel("Tiempo promedio de procesamiento (días)")
plt.title("Variabilidad de tiempos de procesamiento por equipo")
plt.show()


#AQ: ¿Cuál es la relación entre número de órdenes procesadas y horas trabajadas?

# 2. Cargar tabla de órdenes
query_orders_3 = """
SELECT orderid, employeeid, orderdate, shippeddate
FROM silver.orders_final_valid;
"""
df_orders = pd.read_sql(query_orders_3, engine)

# 3. Convertir fechas
df_orders["orderdate"] = pd.to_datetime(df_orders["orderdate"])
df_orders["shippeddate"] = pd.to_datetime(df_orders["shippeddate"])

# 4. Órdenes procesadas por empleado
orders_per_employee = df_orders.groupby("employeeid")["orderid"].count().reset_index(name="orders_processed")

# 5. Ventana de trabajo estimada por empleado
work_window = df_orders.groupby("employeeid").agg(
    first_order=("orderdate", "min"),
    last_order=("shippeddate", "max")
).reset_index()
work_window["work_days"] = (work_window["last_order"] - work_window["first_order"]).dt.days

# 6. Merge y calcular productividad relativa
employee_productivity = orders_per_employee.merge(work_window, on="employeeid")
employee_productivity["orders_per_day"] = employee_productivity["orders_processed"] / employee_productivity["work_days"]

print("Productividad relativa por empleado (órdenes/día):")
print(employee_productivity)

plt.figure(figsize=(10,6))
sns.barplot(data=employee_productivity, x="employeeid", y="orders_per_day", palette="Blues")
plt.title("Órdenes por día trabajado (proxy productividad)")
plt.xlabel("Empleado")
plt.ylabel("Órdenes por día")
plt.show()

# AQ: ¿Qué empleados tienen mayor tasa de cumplimiento de objetivos?

# 2. Cargar tabla de órdenes
query_orders_4 = """
SELECT orderid, employeeid, orderdate, requireddate, shippeddate
FROM silver.orders_final_valid;
"""
df_orders = pd.read_sql(query_orders_4, engine)

# 3. Convertir fechas
df_orders["orderdate"] = pd.to_datetime(df_orders["orderdate"])
df_orders["requireddate"] = pd.to_datetime(df_orders["requireddate"])
df_orders["shippeddate"] = pd.to_datetime(df_orders["shippeddate"])

# 4. Cumplimiento de objetivos
df_orders["on_time"] = (df_orders["shippeddate"] <= df_orders["requireddate"]).astype(int)

# 5. Tasa de cumplimiento por empleado
compliance_by_employee = (
    df_orders.groupby("employeeid")["on_time"]
    .mean()
    .reset_index()
    .rename(columns={"on_time": "compliance_rate"})
    .sort_values("compliance_rate", ascending=False)
)

print("Tasa de cumplimiento por empleado:")
print(compliance_by_employee)

#Órdenes procesadas por hora trabajada.

import pandas as pd

# Partimos del DataFrame employee_productivity que ya tiene orders_per_day
employee_productivity["orders_per_hour"] = employee_productivity["orders_per_day"] / 8

print("Órdenes procesadas por hora trabajada (proxy):")
print(employee_productivity[["employeeid", "orders_per_day", "orders_per_hour"]])


# Promedio global de órdenes por día
avg_orders_per_day = employee_productivity["orders_per_day"].mean()

# Promedio global de órdenes por hora (proxy)
avg_orders_per_hour = employee_productivity["orders_per_hour"].mean()

print(f"Promedio global de órdenes por día: {avg_orders_per_day:.4f}")
print(f"Promedio global de órdenes por hora (proxy): {avg_orders_per_hour:.4f}")

#H1: La productividad mejora con capacitación y claridad de procesos

# proxy de capacitación (0= bajo, 1= medio, 2= alto)
training_score = {
    1: 2, 2: 1, 3: 2, 4: 2, 5: 0, 6: 1, 7: 2, 8: 1
}
employee_productivity["training_score"] = employee_productivity["employeeid"].map(training_score)

import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Scatterplot productividad vs capacitación
sns.scatterplot(
    data=employee_productivity,
    x="training_score",
    y="orders_per_day",
    hue="employeeid",
    palette="viridis"
)
plt.title("Productividad vs Capacitación (proxy)")
plt.xlabel("Nivel de capacitación/claridad de procesos")
plt.ylabel("Órdenes por día")
plt.show()

#H2: Los cuellos de botella se reducen con automatización y control de tiempos.

df_orders["orderdate"] = pd.to_datetime(df_orders["orderdate"])
df_orders["shippeddate"] = pd.to_datetime(df_orders["shippeddate"])

# Crear columna processing_days
df_orders["processing_days"] = (df_orders["shippeddate"] - df_orders["orderdate"]).dt.days

print(df_orders[["orderid", "orderdate", "shippeddate", "processing_days"]].head())

# Variabilidad de tiempos por empleado
variability_by_employee = (
    df_orders.groupby("employeeid")["processing_days"]
    .std()
    .reset_index()
    .rename(columns={"processing_days": "std_processing_days"})
)

# Merge con productividad
employee_analysis = employee_productivity.merge(variability_by_employee, on="employeeid")

print(employee_analysis[["employeeid", "orders_per_day", "std_processing_days"]])

#Guardar 
# Copias explícitas para asegurar independencia
delay_by_employee = delay_by_employee.copy()
delay_by_shipper = delay_by_shipper.copy()
processing_by_employee = processing_by_employee.copy()
productivity_by_employee = productivity_by_employee.copy()
productivity_by_team = productivity_by_team.copy()
employee_productivity = employee_productivity.copy()
compliance_by_employee = compliance_by_employee.copy()
employee_analysis = employee_analysis.copy()

# Exportar a PostgreSQL (capa gold)
delay_by_employee.to_sql("gold.delay_by_employee", engine, if_exists="replace", index=False)
delay_by_shipper.to_sql("gold.delay_by_shipper", engine, if_exists="replace", index=False)
processing_by_employee.to_sql("gold.processing_by_employee", engine, if_exists="replace", index=False)
productivity_by_employee.to_sql("gold.productivity_by_employee", engine, if_exists="replace", index=False)
productivity_by_team.to_sql("gold.productivity_by_team", engine, if_exists="replace", index=False)
employee_productivity.to_sql("gold.employee_productivity", engine, if_exists="replace", index=False)
compliance_by_employee.to_sql("gold.compliance_by_employee", engine, if_exists="replace", index=False)
employee_analysis.to_sql("gold.employee_analysis", engine, if_exists="replace", index=False)

# Exportar resultados a CSVs en carpeta "exports"
# Exportar resultados a CSV en carpeta del proyecto BI
delay_by_employee.to_csv(
    r"C:\Users\jg436\OneDrive\Documentos\BI Projects\BI retail Project\gold_delay_by_employee.csv",
    index=False
)

delay_by_shipper.to_csv(
    r"C:\Users\jg436\OneDrive\Documentos\BI Projects\BI retail Project\gold_delay_by_shipper.csv",
    index=False
)

processing_by_employee.to_csv(
    r"C:\Users\jg436\OneDrive\Documentos\BI Projects\BI retail Project\gold_processing_by_employee.csv",
    index=False
)

productivity_by_employee.to_csv(
    r"C:\Users\jg436\OneDrive\Documentos\BI Projects\BI retail Project\gold_productivity_by_employee.csv",
    index=False
)

productivity_by_team.to_csv(
    r"C:\Users\jg436\OneDrive\Documentos\BI Projects\BI retail Project\gold_productivity_by_team.csv",
    index=False
)

employee_productivity.to_csv(
    r"C:\Users\jg436\OneDrive\Documentos\BI Projects\BI retail Project\gold_employee_productivity.csv",
    index=False
)

compliance_by_employee.to_csv(
    r"C:\Users\jg436\OneDrive\Documentos\BI Projects\BI retail Project\gold_compliance_by_employee.csv",
    index=False
)

employee_analysis.to_csv(
    r"C:\Users\jg436\OneDrive\Documentos\BI Projects\BI retail Project\gold_employee_analysis.csv",
    index=False
)







