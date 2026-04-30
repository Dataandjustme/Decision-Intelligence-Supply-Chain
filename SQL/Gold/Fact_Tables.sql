--Crear Fact tables 

-- Crear Fact sales 

CREATE TABLE gold.fact_sales AS
SELECT 
    o.orderid,
    o.customerid,
    o.employeeid,
    o.shipperid,
    o.orderdate,
    od.productid,
    p.categoryid,
    c.country,
    c.city,
    -- Claves de dimensiones
    to_char(o.orderdate, 'YYYYMMDD')::int AS dateid,
    -- Medidas
    od.unitprice,
    od.quantity,
    od.discount,
    (od.unitprice * od.quantity) AS gross_sales,
    (od.unitprice * od.quantity * (1 - od.discount)) AS net_sales,
    (od.unitprice * od.quantity * od.discount) AS discount_amount,
    o.freight
FROM silver.orders_final_valid o
JOIN silver.order_details_valid od ON o.orderid = od.orderid
JOIN silver.products_valid p ON od.productid = p.productid
JOIN silver.customers_clean c ON o.customerid = c.customerid;

--Crear Fact costos 

CREATE TABLE gold.fact_costs AS
SELECT 
    o.orderid,
    o.customerid,
    c.country,
    c.city,
    p.productid,
    p.categoryid,
    to_char(o.orderdate, 'YYYYMMDD')::int AS dateid,
    -- Medidas de costos
    se.order_cost,
    se.holding_cost,
    (o.freight / NULLIF(od.quantity,0)) AS freight_unit_cost,
    (se.order_cost + se.holding_cost + (o.freight / NULLIF(od.quantity,0))) AS total_cost
FROM silver.orders_final_valid o
JOIN silver.order_details_valid od ON o.orderid = od.orderid
JOIN silver.products_valid p ON od.productid = p.productid
JOIN silver.customers_clean c ON o.customerid = c.customerid
JOIN gold.dim_category dc ON p.categoryid = dc.categoryid
LEFT JOIN public.sales_eoq se ON dc.categoryname = se.category;

-- Crear Fact inventory 

CREATE TABLE gold.fact_inventory AS
SELECT 
    p.productid,
    p.categoryid,
    c.customerid,
    c.country,
    c.city,
    -- Generamos dateid artificial (ejemplo: hoy)
    to_char(current_date, 'YYYYMMDD')::int AS dateid,
    -- Medidas de inventario
    io.optimal_inventory_level,
    io.holding_cost,
    io.order_cost,
    (io.optimal_inventory_level * p.unitprice) AS inventory_value
FROM public.inventory_optimal io
JOIN gold.dim_category dc ON io.category = dc.categoryname
JOIN silver.products_valid p ON p.categoryid = dc.categoryid
LEFT JOIN silver.customers_clean c ON c.customerid IS NOT NULL;

-- Crear Fact supply chain

CREATE TABLE gold.fact_supplychain AS
SELECT 
    o.orderid,
    o.customerid,
    c.country,
    c.city,
    s.shipperid,
    to_char(o.orderdate, 'YYYYMMDD')::int AS dateid,
    -- Medidas de supply chain
    o.freight AS freight_cost,
    (o.shippeddate - o.orderdate) AS delivery_time_days,
    CASE WHEN o.shippeddate <= o.requireddate THEN 1 ELSE 0 END AS on_time_flag,
    o.freight AS total_logistics_cost  -- aquí puedes sumar otros costos si los tienes
FROM silver.orders_final_valid o
JOIN silver.customers_clean c ON o.customerid = c.customerid
JOIN silver.shippers_clean s ON o.shipperid = s.shipperid;

-- Crear Fact consumption 
CREATE TABLE gold.fact_consumption AS
SELECT 
    o.orderid,
    o.customerid,
    c.country,
    c.city,
    p.productid,
    p.categoryid,
    to_char(o.orderdate, 'YYYYMMDD')::int AS dateid,
    -- Medidas de consumo
    SUM(od.quantity) AS consumption_units,
    SUM(od.quantity * od.unitprice) AS consumption_value,
    COUNT(o.orderid) AS consumption_frequency
FROM silver.orders_final_valid o
JOIN silver.order_details_valid od ON o.orderid = od.orderid
JOIN silver.products_valid p ON od.productid = p.productid
JOIN silver.customers_clean c ON o.customerid = c.customerid
GROUP BY o.orderid, o.customerid, c.country, c.city, p.productid, p.categoryid, to_char(o.orderdate, 'YYYYMMDD')::int;
