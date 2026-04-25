-- Capa Broce -- 
CREATE DATABASE supply_bi;

CREATE SCHEMA bronze;
CREATE SCHEMA silver;
CREATE SCHEMA gold;

CREATE TABLE bronze.categories (
    categoryID SERIAL PRIMARY KEY,
    categoryName VARCHAR(50),
    description TEXT
);

CREATE TABLE bronze.customers (
    customerID VARCHAR(10) PRIMARY KEY,
    companyName VARCHAR(100),
    contactName VARCHAR(100),
    contactTitle VARCHAR(50),
    city VARCHAR(50),
    country VARCHAR(50)
);

CREATE TABLE bronze.employees (
    employeeID SERIAL PRIMARY KEY,
    employeeName VARCHAR(100),
    title VARCHAR(50),
    city VARCHAR(50),
    country VARCHAR(50),
    reportsTo INT
);

CREATE TABLE bronze.orders (
    orderID SERIAL PRIMARY KEY,
    customerID VARCHAR(10),
    employeeID INT,
    orderDate DATE,
    requiredDate DATE,
    shippedDate DATE,
    shipperID INT,
    freight NUMERIC(10,2)
);



CREATE TABLE bronze.order_details (
    orderID INT,
    productID INT,
    unitPrice NUMERIC(10,2),
    quantity INT,
    discount NUMERIC(4,2),
    PRIMARY KEY(orderID, productID)
);

CREATE TABLE bronze.products (
    productID SERIAL PRIMARY KEY,
    productName VARCHAR(100),
    quantityPerUnit VARCHAR(50),
    unitPrice NUMERIC(10,2),
    discontinued BOOLEAN,
    categoryID INT
);


CREATE TABLE bronze.shippers (
    shipperID SERIAL PRIMARY KEY,
    companyName VARCHAR(100)
);



-- Contar duplicados en customers
SELECT customerid, COUNT(*)
FROM bronze.customers
GROUP BY customerid
HAVING COUNT(*) > 1;

-- Detectar nulos en orders
SELECT *
FROM bronze.orders
WHERE orderdate IS NULL
   OR customerid IS NULL
   OR employeeid IS NULL;

-- Validar rangos de precios en products
SELECT MIN(unitprice), MAX(unitprice)
FROM bronze.products;
