-- Capa Silver --

CREATE TABLE silver.customers_clean AS
SELECT DISTINCT ON (customerid)
    customerid,
    INITCAP(companyname) AS companyname,
    INITCAP(contactname) AS contactname,
    contacttitle,
    INITCAP(city) AS city,
    INITCAP(country) AS country
FROM bronze.customers
WHERE customerid IS NOT NULL
ORDER BY customerid, companyname;

CREATE TABLE silver.orders_clean AS
SELECT DISTINCT
    orderid,
    customerid,
    employeeid,
    orderdate,
    requireddate,
    shippeddate,
    shipperid,
    freight
FROM bronze.orders
WHERE orderdate IS NOT NULL
  AND customerid IS NOT NULL
  AND employeeid IS NOT NULL;

CREATE TABLE silver.products_clean AS
SELECT DISTINCT
    productid,
    INITCAP(productname) AS productname,
    quantityperunit,
    unitprice,
    discontinued,
    categoryid
FROM bronze.products
WHERE unitprice > 0;

-- Normalización de datos -- 

-- Orders con customers válidos
CREATE TABLE silver.orders_valid AS
SELECT o.*
FROM silver.orders_clean o
JOIN silver.customers_clean c
  ON o.customerid = c.customerid;

-- Products con categorías válidas
CREATE TABLE silver.products_valid AS
SELECT p.*
FROM silver.products_clean p
JOIN bronze.categories c
  ON p.categoryid = c.categoryid;

-- validar ids --
CREATE TABLE silver.order_details_valid AS
SELECT od.*
FROM bronze.order_details od
JOIN silver.orders_valid o
  ON od.orderid = o.orderid
JOIN silver.products_valid p
  ON od.productid = p.productid;

  CREATE TABLE silver.employees_clean AS
SELECT DISTINCT
    employeeid,
    INITCAP(employeename) AS employeename,
    INITCAP(title) AS title,
    INITCAP(city) AS city,
    INITCAP(country) AS country,
    reportsto
FROM bronze.employees
WHERE employeeid IS NOT NULL;

-- Validar jerarquía
CREATE TABLE silver.employees_valid AS
SELECT e.*
FROM silver.employees_clean e
LEFT JOIN silver.employees_clean m
  ON e.reportsto = m.employeeid
WHERE e.reportsto IS NULL OR m.employeeid IS NOT NULL;

CREATE TABLE silver.shippers_clean AS
SELECT DISTINCT
    shipperid,
    INITCAP(companyname) AS companyname
FROM bronze.shippers
WHERE shipperid IS NOT NULL;

-- Orders con shippers válidos
CREATE TABLE silver.orders_final AS
SELECT o.*
FROM silver.orders_valid o
JOIN silver.shippers_clean s
  ON o.shipperid = s.shipperid;

-- Orders con employees válidos
CREATE TABLE silver.orders_final_valid AS
SELECT o.*
FROM silver.orders_final o
JOIN silver.employees_valid e
  ON o.employeeid = e.employeeid;
