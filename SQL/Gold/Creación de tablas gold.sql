CREATE TABLE gold.sales_by_customer AS
SELECT 
    c.customerid,
    c.companyname,
    SUM(od.unitprice * od.quantity) AS total_sales,
    COUNT(DISTINCT o.orderid) AS total_orders
FROM silver.orders_final_valid o
JOIN silver.order_details_valid od ON o.orderid = od.orderid
JOIN silver.customers_clean c ON o.customerid = c.customerid
GROUP BY c.customerid, c.companyname
ORDER BY total_sales DESC;


CREATE TABLE gold.sales_by_product AS
SELECT 
    p.productid,
    p.productname,
    SUM(od.unitprice * od.quantity) AS total_sales,
    SUM(od.quantity) AS total_units
FROM silver.order_details_valid od
JOIN silver.products_valid p ON od.productid = p.productid
GROUP BY p.productid, p.productname
ORDER BY total_sales DESC;


CREATE TABLE gold.sales_by_category AS
SELECT 
    c.categoryid,
    c.categoryname,
    SUM(od.unitprice * od.quantity) AS total_sales
FROM silver.order_details_valid od
JOIN silver.products_valid p ON od.productid = p.productid
JOIN bronze.categories c ON p.categoryid = c.categoryid
GROUP BY c.categoryid, c.categoryname
ORDER BY total_sales DESC;


CREATE TABLE gold.sales_by_employee AS
SELECT 
    e.employeeid,
    e.employeename,
    SUM(od.unitprice * od.quantity) AS total_sales,
    COUNT(DISTINCT o.orderid) AS total_orders
FROM silver.orders_final_valid o
JOIN silver.order_details_valid od ON o.orderid = od.orderid
JOIN silver.employees_valid e ON o.employeeid = e.employeeid
GROUP BY e.employeeid, e.employeename
ORDER BY total_sales DESC;


CREATE TABLE gold.sales_by_shipper AS
SELECT 
    s.shipperid,
    s.companyname,
    COUNT(DISTINCT o.orderid) AS total_orders,
    SUM(od.unitprice * od.quantity) AS total_sales
FROM silver.orders_final_valid o
JOIN silver.order_details_valid od ON o.orderid = od.orderid
JOIN silver.shippers_clean s ON o.shipperid = s.shipperid
GROUP BY s.shipperid, s.companyname
ORDER BY total_sales DESC;

