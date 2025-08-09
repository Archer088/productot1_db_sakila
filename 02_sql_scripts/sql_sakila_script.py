
import mysql.connector
import pandas as pd
import os

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Aeacucho",
    database="sakila"
)

cursor = conexion.cursor()

# Crear carpeta de salida
output_folder = "output_csv_sakila"
os.makedirs(output_folder, exist_ok=True)

# Lista de consultas mejoradas
consultas = {
    "detalle_alquileres.csv": """
        SELECT
            r.rental_id,
            CONCAT(c.first_name, ' ', c.last_name) AS cliente,
            f.title AS pelicula,
            cat.name AS categoria,
            r.rental_date
        FROM rental r
        JOIN customer c ON r.customer_id = c.customer_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category cat ON fc.category_id = cat.category_id;
    """,

    "alquileres_por_mes_categoria.csv": """
        SELECT
            DATE_FORMAT(r.rental_date, '%Y-%m') AS mes,
            cat.name AS categoria,
            COUNT(*) AS total_alquileres
        FROM rental r
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category cat ON fc.category_id = cat.category_id
        GROUP BY mes, categoria
        ORDER BY mes, total_alquileres DESC;
    """,

    "ingresos_por_tienda_categoria.csv": """
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
    """,

    "peliculas_mas_rentables.csv": """
        SELECT
            f.title AS pelicula,
            COUNT(p.payment_id) AS total_alquileres,
            SUM(p.amount) AS total_ingresos
        FROM payment p
        JOIN rental r ON p.rental_id = r.rental_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        GROUP BY f.title
        ORDER BY total_ingresos DESC;
    """,

    "clientes_mas_frecuentes.csv": """
        SELECT
            c.customer_id,
            CONCAT(c.first_name, ' ', c.last_name) AS cliente,
            COUNT(p.payment_id) AS total_transacciones,
            SUM(p.amount) AS total_gastado
        FROM customer c
        JOIN payment p ON c.customer_id = p.customer_id
        GROUP BY c.customer_id
        ORDER BY total_gastado DESC;
    """
}

# Ejecutar consultas y exportar a CSV
for nombre_archivo, consulta in consultas.items():
    cursor.execute(consulta)
    resultados = cursor.fetchall()
    columnas = [col[0] for col in cursor.description]
    df = pd.DataFrame(resultados, columns=columnas)
    df.to_csv(os.path.join(output_folder, nombre_archivo), index=False)
    print(f"✅ Exportado: {nombre_archivo} ({len(df)} filas)")

# Cerrar conexiones
cursor.close()
conexion.close()
