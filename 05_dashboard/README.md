# 🎮 Dashboard - Análisis Profesional de la Base de Datos Sakila

Este proyecto presenta un análisis completo de la base de datos **Sakila**, orientado a mostrar cómo transformar datos brutos en visualizaciones interactivas y paneles útiles para la toma de decisiones. Se construyó como parte de un portafolio profesional en análisis de datos, usando Python, Pandas y Streamlit.

---

## 📊 DEMO en Vivo

* 🌐 [Versión en Streamlit](https://sakiladashboard-kew88fsna32dspctw7amef.streamlit.app)
* ☁️ [Versión en Render](https://sakila-dashboard-90x9.onrender.com)

---

## 🧰 Tecnologías y Librerías

* Python 3.10+
* Pandas
* Streamlit
* Plotly
* Git & GitHub
* Render y Streamlit Cloud (para despliegue)

---

## 📂 Estructura del Proyecto

```
├── app_dashboard.py              # Aplicación principal en Streamlit
├── requirements.txt             # Dependencias del proyecto
├── alquileres_por_mes_categoria_limpio.csv
├── clientes_mas_frecuentes_limpio.csv
├── detalle_alquileres_limpio.csv
├── ingresos_por_tienda_categoria_limpio.csv
└── peliculas_mas_rentables_limpio.csv
```

---

## 🚀 ¿Cómo ejecutar el dashboard localmente?

1. Clona el repositorio:

```bash
git clone https://github.com/Archer088/Sakila_dashboard.git
cd Sakila_dashboard
```

2. Crea un entorno virtual y actívalo:

```bash
python -m venv venv
source venv/bin/activate       # En Linux/Mac
venv\Scripts\activate          # En Windows
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Ejecuta la app:

```bash
python -m streamlit run app_dashboard.py
```

---

## 📂 Descripción del Dashboard

El panel está organizado por pestañas que muestran diferentes tipos de análisis basados en los datos de la base Sakila:

1. **Detalle Alquileres**
   Visualiza información granular de cada alquiler, como cliente, película y fecha.

2. **Alquileres por Mes y Categoría**
   Muestra tendencias mensuales y comparación por géneros cinematográficos.

3. **Clientes Más Frecuentes**
   Lista de los clientes con mayor cantidad de alquileres.

4. **Películas Más Rentables**
   Ordenadas por ingresos totales generados.

5. **Ingresos por Tienda y Categoría**
   Comparación de ingresos según la tienda y tipo de película.

---

## 🧠 Aprendizajes y Enfoque

* Práctica profesional con flujo de trabajo completo:

  * Extracción y limpieza de datos
  * Análisis exploratorio (EDA)
  * Creación de visualizaciones efectivas
  * Despliegue en la nube sin costo
* Optimización del `requirements.txt` para despliegue correcto en Render y Streamlit
* Estructuración de proyecto replicable para otras bases de datos

---

## 🧑‍💻 Autor

* **Juan Aranguren**
* Físico, Científico de Datos y Analista en formación
* 💼 [GitHub Portfolio](https://github.com/Archer088)
* 📨 Contacto: [juanjo88arangurenl@gmail.com](mailto:juanjo88arangurenl@gmail.com) 

---

## ⚖️ Licencia

Este proyecto se publica bajo la licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente, mencionando la autoría.

---

> 💡 ¿Te gustó este proyecto? ¡Puedes darle ⭐ en GitHub o usarlo como base para tus propios dashboards!


