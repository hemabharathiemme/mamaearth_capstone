-- sql/reports.sql

-- a) Order totals
SELECT 
    COUNT(*) AS total_orders,
    ROUND(SUM(quantity * price * (1 - COALESCE(discount_pct, 0) / 100.0)), 2) AS total_revenue,
    ROUND(AVG(quantity * price * (1 - COALESCE(discount_pct, 0) / 100.0)), 2) AS avg_order_value
FROM orders o JOIN products p ON o.product_id = p.product_id;

-- b) COUNT(*) vs COUNT(column)
SELECT COUNT(*) AS total_rows, COUNT(rating) AS rated_rows, (COUNT(*) - COUNT(rating)) AS difference FROM orders;

-- c) LEFT JOIN with a genuine zero-match row
SELECT c.customer_id, c.name FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id, c.name HAVING COUNT(o.order_id) = 0;

-- d) GROUP BY + HAVING
SELECT c.city, COUNT(o.order_id) AS total_orders, SUM(o.returned) AS returned_orders, ROUND(SUM(o.returned) / COUNT(o.order_id) * 100, 1) AS return_rate_pct
FROM customers c JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.city HAVING return_rate_pct > 20 ORDER BY return_rate_pct DESC;

-- e) Ranking with ORDER BY + LIMIT / OFFSET
SELECT c.customer_id, c.name, ROUND(SUM(o.quantity * p.price * (1 - COALESCE(o.discount_pct, 0) / 100.0)), 2) AS total_spend
FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN products p ON o.product_id = p.product_id GROUP BY c.customer_id, c.name ORDER BY total_spend DESC, c.customer_id ASC LIMIT 5;

SELECT c.customer_id, c.name, ROUND(SUM(o.quantity * p.price * (1 - COALESCE(o.discount_pct, 0) / 100.0)), 2) AS total_spend
FROM customers c JOIN orders o ON c.customer_id = o.customer_id JOIN products p ON o.product_id = p.product_id GROUP BY c.customer_id, c.name ORDER BY total_spend DESC, c.customer_id ASC LIMIT 3 OFFSET 2;

-- f) Three-table JOIN with GROUP BY
SELECT p.category, COUNT(o.order_id) AS order_count, ROUND(SUM(o.quantity * p.price * (1 - COALESCE(o.discount_pct, 0) / 100.0)), 2) AS category_revenue
FROM orders o JOIN products p ON o.product_id = p.product_id JOIN customers c ON o.customer_id = c.customer_id GROUP BY p.category ORDER BY category_revenue DESC;

-- g) LIKE pattern match
SELECT * FROM customers WHERE name LIKE 'A%';

-- h) DISTINCT values
SELECT DISTINCT acquisition_source FROM customers ORDER BY acquisition_source ASC;

-- i) ALTER TABLE + UPDATE with CASE
ALTER TABLE customers ADD COLUMN loyalty_tier VARCHAR(10);
UPDATE customers SET loyalty_tier = CASE WHEN city_tier = 1 THEN 'Gold' ELSE 'Silver' END;
SELECT loyalty_tier, COUNT(*) AS tier_count FROM customers GROUP BY loyalty_tier;
