
-- 1. Detalle de alquileres con cliente, película, categoría y fecha
SELECT
    r.rental_id,
    c.first_name || ' ' || c.last_name AS cliente,
    f.title AS pelicula,
    cat.name AS categoria,
    r.rental_date
FROM rental r
JOIN customer c ON r.customer_id = c.customer_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category cat ON fc.category_id = cat.category_id;

-- 2. Alquileres por mes y categoría
SELECT
    strftime('%Y-%m', rental_date) AS mes,
    cat.name AS categoria,
    COUNT(*) AS total_alquileres
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category cat ON fc.category_id = cat.category_id
GROUP BY mes, categoria
ORDER BY mes, total_alquileres DESC;

-- 3. Ingresos por tienda y categoría
SELECT
    st.store_id,
    cat.name AS categoria,
    SUM(p.amount) AS ingresos
FROM payment p
JOIN rental r ON p.rental_id = r.rental_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category cat ON fc.category_id = cat.category_id
JOIN store st ON i.store_id = st.store_id
GROUP BY st.store_id, cat.name
ORDER BY ingresos DESC;

-- 4. Ranking de películas más rentables
SELECT
    f.title AS pelicula,
    COUNT(p.payment_id) AS total_alquileres,
    SUM(p.amount) AS total_ingresos
FROM payment p
JOIN rental r ON p.rental_id = r.rental_id
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
GROUP BY f.title
ORDER BY total_ingresos DESC
LIMIT 50;

-- 5. Clientes más frecuentes con total gastado
SELECT
    c.customer_id,
    c.first_name || ' ' || c.last_name AS cliente,
    COUNT(p.payment_id) AS total_transacciones,
    SUM(p.amount) AS total_gastado
FROM customer c
JOIN payment p ON c.customer_id = p.customer_id
GROUP BY c.customer_id
ORDER BY total_gastado DESC
LIMIT 50;
