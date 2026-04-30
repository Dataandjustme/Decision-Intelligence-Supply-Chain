-- Crear dimensiones para ventas --

-- Crear tabla Dim_Categoría en la capa Gold
CREATE TABLE gold.dim_category AS
SELECT DISTINCT 
    p.categoryid,
    s.categoryname
FROM silver.products_valid p
JOIN gold.sales_by_category s
    ON p.categoryid = s.categoryid;

-- Crear tabla Dim_clientes en la capa g
CREATE TABLE gold.dim_customer AS
SELECT DISTINCT
    customerid,
    companyname,
    contactname,
    contacttitle,
    city,
    country
FROM silver.customers_clean
WHERE customerid IS NOT NULL;

-- Crear tabla Dim_region 

CREATE TABLE gold.dim_region AS
SELECT DISTINCT
    country,
    city
FROM silver.customers_clean
WHERE country IS NOT NULL;

--Crear Dim_Tiempo

CREATE TABLE gold.dim_time AS
SELECT 
    to_char(d::date, 'YYYYMMDD')::int AS dateid,
    d::date AS date,
    EXTRACT(DAY FROM d) AS day,
    EXTRACT(MONTH FROM d) AS month,
    EXTRACT(QUARTER FROM d) AS quarter,
    EXTRACT(YEAR FROM d) AS year,
    to_char(d, 'Day') AS weekday,
    CASE WHEN EXTRACT(ISODOW FROM d) IN (6,7) THEN true ELSE false END AS is_weekend
FROM generate_series(
    (SELECT MIN(orderdate) FROM silver.orders_final_valid),
    (SELECT MAX(orderdate) FROM silver.orders_final_valid),
    interval '1 day'
) d;

--Crear Dim_product

CREATE TABLE gold.dim_product AS
SELECT DISTINCT
    productid,
    productname,
    quantityperunit,
    unitprice,
    discontinued,
    categoryid
FROM silver.products_valid
WHERE productid IS NOT NULL;
