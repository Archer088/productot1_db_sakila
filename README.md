# ![Sakila Dashboard](banner_sakila_readme.png)

# 📊 Proyecto Completo: Análisis de la Base de Datos Sakila

Este proyecto representa un **flujo de trabajo profesional** de análisis de datos partiendo desde consultas SQL a la base de datos **Sakila**, hasta la creación de un dashboard interactivo en **Streamlit**.  
El objetivo es mostrar un ejemplo completo, ideal para portafolio o producto listo para ofrecer a clientes.

---

## 🗂️ Estructura del Proyecto

```
producto1_db_sakila/
│
├── 01_data_raw/           # Base de datos Sakila
├── 02_sql_scripts/           # Scripts para extraer datos y archivos CSV generados por las consultas SQL
├── 03_notebooks/             # Plantillas de Google Colab para limpieza y EDA
├── 04_output_csv_sakila_limpio/       # Archivos csv comprimidos,  limpios y generados de la plantilla de Google Colab.
├── 05_dashboard/             # Dashboard interactivo en Streamlit
│   ├── app_dashboard.py
│   └── README.md
├── requirements.txt          # Librerías necesarias para todo el proyecto
└── README.md                 # Este archivo
```

---

## 🚀 Flujo de Trabajo

1. **Extracción de Datos (SQL)**  
   - Se realizan consultas complejas a la base de datos Sakila usando MySQL.
   - Exportación de resultados a **CSV**.

2. **Limpieza y EDA (Google Colab)**  
   - Se cargan los CSV.
   - Limpieza de datos, análisis exploratorio y generación de visualizaciones.

3. **Dashboard Interactivo (Streamlit)**  
   - Integración de gráficos dinámicos con **Plotly** y tablas interactivas.
   - Sección de KPIs, insights y análisis detallado.

---

## 🛠️ Tecnologías Usadas

- **Base de Datos:** MySQL
- **Lenguaje:** Python 3
- **Análisis:** Pandas, NumPy
- **Visualización:** Matplotlib, Seaborn, Plotly
- **Dashboard:** Streamlit
- **Automatización SQL:** mysql.connector
- **Entorno Colaborativo:** Google Colab

---

## 📦 Instalación

1. Clonar este repositorio:
```bash
git clone https://github.com/Archer088/producto1_db_sakila.git
cd producto1_db_sakila
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar el script consultas sql:
```bash
cd 05_dashboard
python -m streamlit run sql_sakila_script.py
```

4. Ejecutar el dashboard:
```bash
cd 05_dashboard
python -m streamlit run app_dashboard.py
```
---

## 📊 Ejemplo del Dashboard

El dashboard incluye:

- KPIs generales
- Gráficos comparativos
- Tendencias
- Insights estratégicos

---

## 📧 Contacto del Autor

- **Autor:** Juan Aranguren  
- **Email:** juanjo88arangurenl@gmail.com  
- **GitHub:** [Archer088](https://github.com/Archer088)

---

## 🏷️ Licencia

Este proyecto está bajo la licencia MIT.  
Puedes usarlo libremente, dando crédito al autor.

---
