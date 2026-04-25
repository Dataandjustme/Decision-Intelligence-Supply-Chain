-- KPIs---

--Ventas totales--

CREATE TABLE gold.kpi_total_sales AS
SELECT SUM(od.unitprice * od.quantity) AS total_sales
FROM silver.order_details_valid od;

--Ticket promedio--
CREATE TABLE gold.kpi_avg_order_value AS
SELECT 
    SUM(od.unitprice * od.quantity) / COUNT(DISTINCT o.orderid) AS avg_order_value
FROM silver.order_details_valid od
JOIN silver.orders_final_valid o ON od.orderid = o.orderid;


--Tiempo promedio de entrega--
CREATE TABLE gold.kpi_avg_delivery_time AS
SELECT 
    AVG(shippeddate - orderdate) AS avg_delivery_days
FROM silver.orders_final_valid
WHERE shippeddate IS NOT NULL AND orderdate IS NOT NULL;

--Ranking de clientes por venta--
CREATE TABLE gold.kpi_top_customers AS
SELECT 
    c.customerid,
    c.companyname,
    SUM(od.unitprice * od.quantity) AS total_sales
FROM silver.orders_final_valid o
JOIN silver.order_details_valid od ON o.orderid = od.orderid
JOIN silver.customers_clean c ON o.customerid = c.customerid
GROUP BY c.customerid, c.companyname
ORDER BY total_sales DESC
LIMIT 5;

--Ranking de productos por venta--
CREATE TABLE gold.kpi_top_products AS
SELECT 
    p.productid,
    p.productname,
    SUM(od.unitprice * od.quantity) AS total_sales
FROM silver.order_details_valid od
JOIN silver.products_valid p ON od.productid = p.productid
GROUP BY p.productid, p.productname
ORDER BY total_sales DESC
LIMIT 5;
