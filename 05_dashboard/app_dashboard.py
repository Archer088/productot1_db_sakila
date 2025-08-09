import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title = "Dashboard Sakila",
    layout = "wide",
    initial_sidebar_state = "expanded"
)

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: #f8f9fa;
    }
    .section-title {
        font-size: 1.3rem;
        font-weight: bold;
        margin-top: 20px;
        color: #f8f9fa;
    }
    .metric-card {
        padding: 12px;
        border-radius: 10px;
        background-color: #1e1e1e;
        color: #ffffff;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
        margin: 5px;
    }
    h1, h2, h3 {
        color: #f8f9fa;
    }
    hr {
        border: 1px solid #444;
    }
    </style>
""", unsafe_allow_html = True)

# --- CARGA DE LOS CSV ---
@st.cache_data
def cargar_csv():
    df_detalle = pd.read_csv("detalle_alquileres_limpio.csv")
    df_alquileres_mes = pd.read_csv("alquileres_por_mes_categoria_limpio.csv")
    df_clientes = pd.read_csv("clientes_mas_frecuentes_limpio.csv")
    df_peliculas = pd.read_csv("peliculas_mas_rentables_limpio.csv")
    df_ingresos = pd.read_csv("ingresos_por_tienda_categoria_limpio.csv")
    return df_detalle, df_alquileres_mes, df_clientes, df_peliculas, df_ingresos

df_detalle, df_alquileres_mes, df_clientes, df_peliculas, df_ingresos = cargar_csv()

# --- TÍTULO ---
st.title("🎬 Dashboard - Análisis de la Base Sakila")
st.markdown("Explora los reportes organizados por pestañas. Selecciona el análisis que deseas visualizar.")

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Detalle Alquileres",
    "Alquileres por Mes y Categoría",
    "Clientes Más Frecuentes",
    "Películas Más Rentables",
    "Ingresos por Tienda y Categoría"
])

# --- TAB 1: DETALLE ALQUILERES ---
with tab1:
    st.markdown("<div class='section-title'>🎛️ Análisis de Detalle de Alquileres</div>", unsafe_allow_html = True)
    st.dataframe(df_detalle.head())
    
    # --- KPIs GENERALES ---
    st.markdown("<hr>", unsafe_allow_html = True)
    st.markdown("<div class='section-title'>📈 KPIs Generales</div>", unsafe_allow_html = True)

    total_alquileres = df_detalle.shape[0]
    categorias_unicas = df_detalle["categoria"].nunique()

    dias_mas_alquilados = df_detalle['weekday'].value_counts()
    dia_top = dias_mas_alquilados.idxmax()
    cantidad_top = dias_mas_alquilados.max()
    dia_bajo = dias_mas_alquilados.idxmin()
    cantidad_baja = dias_mas_alquilados.min()

    # KPIs como tarjetas
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.markdown(f"<div class='metric-card'><h3>🎬 Total Alquileres</h3><h2>{total_alquileres}</h2></div>", unsafe_allow_html = True)
    kpi2.markdown(f"<div class='metric-card'><h3>📂 Categorías Únicas</h3><h2>{categorias_unicas}</h2></div>", unsafe_allow_html = True)
    kpi3.markdown(f"<div class='metric-card'><h3>📅 Día con más alquileres</h3><h2>{dia_top} ({cantidad_top})</h2></div>", unsafe_allow_html = True)
    kpi4.markdown(f"<div class='metric-card'><h3>📉 Día con menos alquileres</h3><h2>{dia_bajo} ({cantidad_baja})</h2></div>", unsafe_allow_html = True)

    # --- GRÁFICOS ---
    st.markdown("<hr>", unsafe_allow_html = True)
    st.markdown("<div class='section-title'>📊✨ Visualizaciones</div>", unsafe_allow_html = True)

    # --- Gráfico de Horas ---
    if 'hour' in df_detalle.columns:
        conteo_horas = df_detalle['hour'].value_counts().sort_index().reset_index()
        conteo_horas.columns = ['Hora', 'Cantidad de Alquileres']

        fig = px.bar(
            conteo_horas, x = 'Hora', y = 'Cantidad de Alquileres',
            text = 'Cantidad de Alquileres', color = 'Cantidad de Alquileres',
            color_continuous_scale = 'Viridis',
            title = "Frecuencia de Alquileres por Hora del Día",
            template = "plotly_dark"
        )
        fig.update_traces(texttemplate = '%{text}', textposition = 'outside')
        fig.update_layout(xaxis = dict(tickmode = 'linear'))

    # --- Gráfico de Género ---
    if 'genero_estimado' in df_detalle.columns:
        conteo_genero = df_detalle['genero_estimado'].value_counts().reset_index()
        conteo_genero.columns = ['Género', 'Cantidad']

        fig_genero = px.bar(
            conteo_genero, x = 'Género', y = 'Cantidad',
            text = 'Cantidad', color = 'Género',
            color_discrete_sequence = px.colors.qualitative.Set2,
            title = "Distribución de Alquileres por Género Estimado",
            template = "plotly_dark"
        )
        fig_genero.update_traces(texttemplate = '%{text}', textposition = 'outside')

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig, use_container_width = True)
        st.caption("🔍 **Insight:** Las horas pico de alquileres se concentran entre 14:00 y 21:00 horas.")
    with col2:
        st.plotly_chart(fig_genero, use_container_width = True)
        st.caption("🔍 **Insight:** Predomina el género masculino en las estimaciones.")

    # --- Gráfico de Categorías ---
    if 'categoria' in df_detalle.columns:
        conteo_cats = df_detalle.groupby(['categoria', 'genero_estimado']).size().reset_index(name = 'Cantidad')

        fig_top_cats = px.bar(
            conteo_cats, x = 'categoria', y = 'Cantidad',
            color = 'genero_estimado', barmode = 'group',
            text = 'Cantidad', color_discrete_sequence = px.colors.sequential.Magma,
            title = "Categorías por Género Estimado",
            template = "plotly_dark"
        )
        fig_top_cats.update_traces(texttemplate = '%{text}', textposition = 'outside')
        fig_top_cats.update_layout(
            xaxis_title = "Categoría", yaxis_title = "Cantidad de Alquileres",
            xaxis_tickangle = -45, legend_title_text = 'Género',
            legend = dict(x = 1.05, y = 1, traceorder = 'normal', orientation = 'v')
        )

    # --- Gráfico de Días ---
    if 'weekday' in df_detalle.columns:
        conteo_dias = df_detalle['weekday'].value_counts().reindex(
            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        ).reset_index()
        conteo_dias.columns = ['Día', 'Cantidad']

        fig_dias = px.bar(
            conteo_dias, x = 'Cantidad', y = 'Día',
            orientation = 'h', text = 'Cantidad', color = 'Cantidad',
            color_continuous_scale = 'Plasma',
            title = "Alquileres por Día de la Semana",
            template = "plotly_dark"
        )
        fig_dias.update_traces(texttemplate = '%{text}', textposition = 'outside')

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(fig_top_cats, use_container_width = True)
        st.caption("🔍 **Insight:** Acción, Animación y Sports dominan el top de categorías.")
    with col4:
        st.plotly_chart(fig_dias, use_container_width = True)
        st.caption("🔍 **Insight:** Los fines de semana muestran mayor actividad, pero se observa un pico de alquileres el día Martes.")


    


   

# --- TAB 2: ALQUILERES POR MES Y CATEGORÍA ---
with tab2:
    st.markdown("<div class='section-title'>📆 Alquileres por Mes y Categoría</div>", unsafe_allow_html = True)
    st.dataframe(df_alquileres_mes.head())
    
    
    # --- KPIs GENERALES ---
    st.markdown("<hr>", unsafe_allow_html = True)
    st.markdown("<div class='section-title'>📈 KPIs Generales</div>", unsafe_allow_html = True)
    
    meses_analizados = df_alquileres_mes["mes"].nunique()
    n_alquileres = df_alquileres_mes["total_alquileres"].sum()
    prom_alquileres_mensuales = df_alquileres_mes["total_global_mes"].mean()
    
    fila_max_alquileres = df_alquileres_mes.loc[df_alquileres_mes['total_global_mes'].idxmax()]
    mes_mayor_alquiler = fila_max_alquileres['nombre_mes']
    cantidad_mayor_alquiler = fila_max_alquileres['total_global_mes']

    
    # KPIs como tarjetas
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.markdown(f"<div class='metric-card'><h3>📅 Meses analizados</h3><h2>{meses_analizados}</h2></div>", unsafe_allow_html = True)
    kpi2.markdown(f"<div class='metric-card'><h3>📀 Alquileres Totales</h3><h2>{n_alquileres}</h2></div>", unsafe_allow_html = True)
    kpi3.markdown(f"<div class='metric-card'><h3>🛒 Alquiler promedio mensual</h3><h2>{prom_alquileres_mensuales}</h2></div>", unsafe_allow_html = True)
    kpi4.markdown(f"<div class='metric-card'><h3>📈 Mes con mayores alquileres</h3><h2>{mes_mayor_alquiler} ({cantidad_mayor_alquiler})</h2></div>", unsafe_allow_html = True)
 
    # --- GRÁFICOS ---
    st.markdown("<hr>", unsafe_allow_html = True)
    st.markdown("<div class='section-title'>📊✨ Visualizaciones</div>", unsafe_allow_html = True)

    
    # --- Gráfico: Tendencia global de alquileres por mes ---
    if 'mes' in df_alquileres_mes.columns and 'total_global_mes' in df_alquileres_mes.columns:
        df_mes = df_alquileres_mes.drop_duplicates(subset = 'mes')

        fig_tendencia_mes = px.line(
            df_mes,
            x = 'mes',
            y = 'total_global_mes',
            markers = True,
            text = 'total_global_mes',
            title = "📅 Tendencia Global de Alquileres por Mes",
            template = 'plotly_dark'
        )

        fig_tendencia_mes.update_traces(textposition = "top center")
        fig_tendencia_mes.update_layout(
            xaxis_title = "Mes",
            yaxis_title = "Alquileres Totales",
            xaxis_tickangle = -45,
            showlegend = False
        )



    # --- Gráfico: Participación de las categorías Top 4 ---
    if 'categoria' in df_alquileres_mes.columns and 'total_alquileres' in df_alquileres_mes.columns:

        # Top 4 categorías con más alquileres totales
        top4_cats = df_alquileres_mes.groupby('categoria')['total_alquileres'].sum().nlargest(4).index
        df_top4 = df_alquileres_mes[df_alquileres_mes['categoria'].isin(top4_cats)].copy()

        # Pivotear los datos para gráfico de área
        pivot_top4 = (
            df_top4.pivot(index = 'mes', columns = 'categoria', values = 'total_alquileres')
                .fillna(0)
                .reset_index()
        )

        # Crear gráfico de área apilada interactivo
        fig_top4_area = px.area(
            pivot_top4,
            x = 'mes',
            y = top4_cats,
            title = "📦 Participación de las Categorías Top 4 en Alquileres",
            template = 'plotly_dark',
            labels = {'value': 'Cantidad de Alquileres', 'variable': 'Categoría'},
        )

        fig_top4_area.update_layout(
            xaxis_title = "Mes",
            yaxis_title = "Alquileres Totales",
            xaxis_tickangle = -45,
            legend_title_text = 'Categorías',
            hovermode = "x unified"
        )

        
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_tendencia_mes, use_container_width = True)
        st.caption("🔍 **Insight:** Esta visualización muestra la evolución mensual de los alquileres.")
    with col2:
        st.plotly_chart(fig_top4_area, use_container_width = True)
        st.caption("🔍 **Insight:** Este gráfico muestra cómo evoluciona la participación de las 4 categorías más populares a lo largo del tiempo.")
        

    # --- Gráfico: Estacionalidad de alquileres ---
    if 'nombre_mes' in df_alquileres_mes.columns and 'total_alquileres' in df_alquileres_mes.columns:

        # Orden correcto de los meses 
        orden_meses = df_alquileres_mes[['num_mes', 'nombre_mes']].drop_duplicates().sort_values('num_mes')['nombre_mes'].tolist()

        # Agrupación por nombre del mes y cálculo del promedio
        df_estacionalidad = (
            df_alquileres_mes.groupby('nombre_mes', observed = True)['total_alquileres']
                .mean()
                .reindex(orden_meses)  # Asegura el orden correcto
                .reset_index(name = 'promedio_alquileres')
        )

        # Crear gráfico de barras con Plotly
        fig_estacionalidad = px.bar(
            df_estacionalidad,
            x = 'nombre_mes',
            y = 'promedio_alquileres',
            text = 'promedio_alquileres',
            title = '📊 Promedio de Alquileres por Mes Calendario (Estacionalidad)',
            template = 'plotly_dark',
            color = 'promedio_alquileres',
            color_continuous_scale = 'Viridis',
        )

        fig_estacionalidad.update_traces(
            texttemplate = '%{text:.2f}',
            textposition = 'outside'
        )

        fig_estacionalidad.update_layout(
            xaxis_title = 'Mes',
            yaxis_title = 'Promedio de Alquileres',
            xaxis_tickangle = -45,
            coloraxis_showscale = False
        )

        # Mostrar en Streamlit
        st.plotly_chart(fig_estacionalidad, use_container_width = True)
        st.caption("🔍 **Insight:** Este gráfico revela patrones estacionales al mostrar el promedio de alquileres por cada mes del calendario.")



# --- TAB 3: CLIENTES MÁS FRECUENTES ---
with tab3:
    st.markdown("<div class='section-title'> 👥 Análisis de Clientes mas Frecuentes</div>", unsafe_allow_html = True)
    st.dataframe(df_clientes.head())
    
    # --- KPIs GENERALES ---
    st.markdown("<hr>", unsafe_allow_html = True)
    st.markdown("<div class='section-title'>📈 KPIs Generales</div>", unsafe_allow_html = True)

    total_clientes = df_clientes.shape[0]
    ingreso_total = df_clientes["total_gastado"].sum()

    max_gastado = df_clientes.loc[df_clientes['total_gastado'].idxmax()]
    cliente_max = max_gastado["cliente"]
    cantidad_max = max_gastado["total_gastado"]
    
    mas_frecuente = df_clientes.loc[df_clientes["total_transacciones"].idxmax()]
    cliente_mas_frecuente = mas_frecuente["cliente"]
    cliente_frecuencia = mas_frecuente["total_transacciones"]

    # KPIs como tarjetas
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.markdown(f"<div class='metric-card'><h3>🧍‍♂️ Total Clientes</h3><h2>{total_clientes}</h2></div>", unsafe_allow_html = True)
    kpi2.markdown(f"<div class='metric-card'><h3>💰 Ingreso Total</h3><h2>${ingreso_total:,.2f}</h2></div>", unsafe_allow_html = True)
    kpi3.markdown(f"<div class='metric-card'><h3>🤑 Cliente que mas gastó</h3><h2>{cliente_max} <br> (${cantidad_max:,.2f})</h2></div>", unsafe_allow_html = True)
    kpi4.markdown(f"<div class='metric-card'><h3>👑 Cliente mas frecuente</h3><h2>{cliente_mas_frecuente} ({cliente_frecuencia} transacciones)</h2></div>", unsafe_allow_html = True)

    # --- GRÁFICOS ---
    st.markdown("<hr>", unsafe_allow_html = True)
    st.markdown("<div class='section-title'>📊✨ Visualizaciones</div>", unsafe_allow_html = True)
    
    if "total_gastado" in df_clientes.columns and "cliente" in df_clientes.columns:
        
        # Top 10 clientes que gastaron mas
        top10 = df_clientes.sort_values('total_gastado', ascending = False).head(10)

        fig_top10_gasto = px.bar(
            top10,
            x = 'total_gastado',
            y = 'cliente',
            orientation = 'h',
            text = 'total_gastado',
            color = 'total_gastado',
            title = "💸 Top 10 Clientes con Mayor Gasto",
            template = 'plotly_dark',
            labels = {'total_gastado': 'Gasto Total ($)', 'cliente': 'Cliente'}
        )

        fig_top10_gasto.update_traces(
            texttemplate = '$%{text:,.2f}',
            textposition = 'outside'
        )

        fig_top10_gasto.update_layout(
            xaxis_title = "Cantidad Total Gastada ($)",
            yaxis_title = "Cliente",
            yaxis = dict(autorange = "reversed"),  
            coloraxis_showscale = False,
            margin = dict(l = 100, r = 40, t = 60, b = 40)
        )

      
      
    # --- Gráfico: Top 15 Clientes por Transacciones ---
    if 'cliente' in df_clientes.columns and 'total_transacciones' in df_clientes.columns:
        top15 = df_clientes.sort_values("total_transacciones", ascending = False).head(15)

        fig_top15 = px.bar(
            top15,
            x = 'cliente',
            y = 'total_transacciones',
            text = 'total_transacciones',
            color = 'cliente',
            color_discrete_sequence = px.colors.sequential.Viridis,
            title = "🧾 Top 15 Clientes por Cantidad de Transacciones",
            template = "plotly_dark"
        )

        fig_top15.update_traces(
            textposition = 'outside',
            hovertemplate = '<b>%{x}</b><br>Transacciones: %{y}<extra></extra>'
        )

        fig_top15.update_layout(
            xaxis_title = "Cliente",
            yaxis_title = "Cantidad de Transacciones",
            xaxis_tickangle = -45,
            showlegend = False,
            margin = dict(l = 40, r = 40, t = 60, b = 40)
        )

  
  
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_top10_gasto, use_container_width = True)
        st.caption("🔍 **Insight:** Estos son los 10 clientes que han generado más ingresos en total.")
    with col2:
        st.plotly_chart(fig_top15, use_container_width = True)
        st.caption("🔍 **Insight:** Los clientes con más transacciones pueden representar mayor fidelización o rentabilidad.")
        


    # --- Gráfico: Relación entre Frecuencia y Gasto (Bubble Chart) ---
    if 'total_transacciones' in df_clientes.columns and 'total_gastado' in df_clientes.columns:

        fig_scatter = px.scatter(
            df_clientes,
            x = 'total_transacciones',
            y = 'total_gastado',
            color = 'total_gastado',
            hover_name = 'cliente',
            size_max = 60,
            template = 'plotly_dark',
            title = "💸 Relación entre Cantidad de Transacciones y Total Gastado"
        )

        fig_scatter.update_layout(
            xaxis_title = "Cantidad de Transacciones",
            yaxis_title = "Total Gastado ($)",
            margin = dict(l = 40, r = 40, t = 60, b = 40)
        )

        st.plotly_chart(fig_scatter, use_container_width = True)
        st.caption("🔍 **Insight:** Este gráfico permite observar la correlación entre frecuencia de alquileres y el gasto total. Cada burbuja representa un cliente.")



    # --- Filtrar Clientes de Interés ---
    umbral_transacciones_pocas = df_clientes['total_transacciones'].quantile(0.50)
    umbral_gasto_alto = df_clientes['total_gastado'].quantile(0.75)

    clientes_interes = df_clientes[
        (df_clientes['total_transacciones'] <= umbral_transacciones_pocas) &
        (df_clientes['total_gastado'] >= umbral_gasto_alto)
    ].copy()
    clientes_interes['tipo'] = '🎯 Clientes de Interés'

    otros_clientes = df_clientes[~df_clientes.index.isin(clientes_interes.index)].copy()
    otros_clientes['tipo'] = 'Clientes Generales'

    # Combinar en un solo DataFrame
    df_plot = pd.concat([clientes_interes, otros_clientes])

    # --- Gráfico con Plotly ---
    fig_clientes_interes = px.scatter(
        df_plot,
        x = 'total_transacciones',
        y = 'total_gastado',
        color = 'tipo',
        hover_name = 'cliente',
        size_max = 60,
        color_discrete_map = {
            'Clientes Generales': 'lightgreen',
            '🎯 Clientes de Interés': 'red'
        },
        template = 'plotly_dark',
        title = "🎯 Clientes con Pocas Transacciones y Alto Gasto"
    )

    fig_clientes_interes.update_layout(
        xaxis_title = "Cantidad de Transacciones",
        yaxis_title = "Total Gastado ($)",
        legend_title_text = "Tipo de Cliente",
        margin = dict(l = 40, r = 40, t = 60, b = 40)
    )

    # --- Mostrar gráfico e insight ---
    st.plotly_chart(fig_clientes_interes, use_container_width = True)
    st.caption("🔍 **Insight:** Este gráfico destaca a los clientes que, a pesar de tener pocas transacciones, realizan un gasto considerable. Representan oportunidades de fidelización.")

    # --- Mostrar tabla de clientes de interés ---
    st.subheader("📋 Clientes de Interés")
    st.dataframe(clientes_interes[['cliente', 'total_transacciones', 'total_gastado']])

    # --- Mostrar porcentaje representado ---
    porcentaje = len(clientes_interes) / len(df_clientes) * 100
    st.markdown(f"Estos **{len(clientes_interes)} clientes** representan aproximadamente el **{porcentaje:.2f}%** del total.")






# --- TAB 4: PELÍCULAS MÁS RENTABLES ---
with tab4:

    st.markdown("<div class='section-title'> 🎥 Análisis de Películas Más Rentables</div>", unsafe_allow_html = True)
    st.dataframe(df_peliculas.head())
    
    # --- KPIs GENERALES ---
    st.markdown("<hr>", unsafe_allow_html = True)
    st.markdown("<div class='section-title'>📈 KPIs Generales</div>", unsafe_allow_html = True)

    total_peliculas = df_peliculas.shape[0]
    ingreso_medio = df_peliculas["total_ingresos"].mean()

    max_ingresos = df_peliculas.loc[df_peliculas['total_ingresos'].idxmax()]
    peli_max = max_ingresos["pelicula"]
    peli_cantidad_max = max_ingresos["total_ingresos"]
    
    mas_alquileres = df_peliculas.loc[df_peliculas["total_alquileres"].idxmax()]
    peli_mas_alquilada = mas_alquileres["pelicula"]
    peli_frecuencia = mas_alquileres["total_alquileres"]

    # KPIs como tarjetas
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.markdown(f"<div class='metric-card'><h3>🎬 Total películas</h3><h2>{total_peliculas}</h2></div>", unsafe_allow_html = True)
    kpi2.markdown(f"<div class='metric-card'><h3>💵 Ingreso Promedio</h3><h2>${ingreso_medio:,.2f}</h2></div>", unsafe_allow_html = True)
    kpi3.markdown(f"<div class='metric-card'><h3>💹 Película con más ingresos</h3><h2>{peli_max} <br> (${peli_cantidad_max:,.2f})</h2></div>", unsafe_allow_html = True)
    kpi4.markdown(f"<div class='metric-card'><h3>📈 Película más alquilada</h3><h2>{peli_mas_alquilada} ({peli_frecuencia} alquileres)</h2></div>", unsafe_allow_html = True)

    # --- GRÁFICOS ---
    st.markdown("<hr>", unsafe_allow_html = True)
    st.markdown("<div class='section-title'>📊✨ Visualizaciones</div>", unsafe_allow_html = True)
    
    
    if 'pelicula' in df_peliculas.columns and 'total_ingresos' in df_peliculas.columns:
        top8_income = df_peliculas.sort_values('total_ingresos', ascending = False).head(8)

        fig_top8_peliculas = px.bar(
            top8_income,
            x = 'total_ingresos',
            y = 'pelicula',
            orientation = 'h',
            text='total_ingresos',
            title = '🎬 Top 8 Películas por Ingresos Totales',
            template = 'plotly_dark',
            color = 'total_ingresos',
            color_continuous_scale = 'Blues'
        )

        fig_top8_peliculas.update_layout(
            xaxis_title = 'Ingresos Totales ($)',
            yaxis_title = 'Película',
            yaxis = {'categoryorder':'total ascending'}, 
            coloraxis_showscale = False
        )

        fig_top8_peliculas.update_traces(texttemplate = '$%{text:,.2f}', textposition = 'outside')

        # Mostrar en dashboard
        st.plotly_chart(fig_top8_peliculas, use_container_width = True)
        st.caption("🔍 **Insight:** Estas son las 8 películas que han generado mayores ingresos totales en la historia de la base de datos.")
        
        
    if 'pelicula' in df_peliculas.columns and 'total_alquileres' in df_peliculas.columns:
        top8_rentals = df_peliculas.sort_values('total_alquileres', ascending = False).head(8)

        fig_top8_alquileres = px.bar(
            top8_rentals,
            x = 'pelicula',
            y = 'total_alquileres',
            text = 'total_alquileres',
            title = '🎥 Top 8 Películas por Número de Alquileres',
            template = 'plotly_dark',
            color = 'total_alquileres',
            color_continuous_scale = 'Plasma'
        )

        fig_top8_alquileres.update_layout(
            xaxis_title = 'Película',
            yaxis_title = 'Total de Alquileres',
            xaxis_tickangle = -45,
            coloraxis_showscale = False
        )

        fig_top8_alquileres.update_traces(
            texttemplate = '%{text:.0f}',
            textposition = 'outside'
        )

        # Mostrar en el dashboard
        st.plotly_chart(fig_top8_alquileres, use_container_width = True)
        st.caption("🔍 **Insight:** Estas películas son las más alquiladas del catálogo, lo cual refleja su alta popularidad entre los clientes.")



    # --- Definir umbrales para análisis estratégico ---
    if "total_alquileres" in df_peliculas.columns and "total_ingresos" in df_peliculas.columns:
        # --- Definir umbrales para "películas estratégicas" ---
        umbral_alquileres_pocos = df_peliculas['total_alquileres'].quantile(0.35)
        umbral_ingreso_alto = df_peliculas['total_ingresos'].quantile(0.75)

        # --- Filtrar películas de interés ---
        peliculas_interes = df_peliculas[
            (df_peliculas['total_alquileres'] <= umbral_alquileres_pocos) &
            (df_peliculas['total_ingresos'] >= umbral_ingreso_alto)
        ].copy()
        peliculas_interes['tipo'] = '🎯 Películas Estratégicas'

        # --- Clasificar el resto ---
        otras_peliculas = df_peliculas[~df_peliculas.index.isin(peliculas_interes.index)].copy()
        otras_peliculas['tipo'] = 'Películas Generales'

        # --- Combinar en un solo DataFrame para el gráfico ---
        df_plot_peliculas = pd.concat([peliculas_interes, otras_peliculas])

        # --- Gráfico de dispersión con estilo unificado ---
        fig_peliculas_interes = px.scatter(
            df_plot_peliculas,
            x = 'total_alquileres',
            y = 'total_ingresos',
            color = 'tipo',
            hover_name = 'pelicula',
            size_max = 60,
            color_discrete_map = {
                'Películas Generales': 'lightgreen',
                '🎯 Películas Estratégicas': 'red'
            },
            template = 'plotly_dark',
            title = "🎯 Películas Estratégicas: Altos Ingresos con Pocos Alquileres"
        )

        fig_peliculas_interes.update_layout(
            xaxis_title = "Cantidad de Alquileres",
            yaxis_title = "Ingresos Totales ($)",
            legend_title_text = "Tipo de Película",
            margin = dict(l = 40, r = 40, t = 60, b = 40)
        )

        # --- Mostrar gráfico en el dashboard ---
        st.plotly_chart(fig_peliculas_interes, use_container_width = True)

        # --- Insight profesional ---
        st.caption("🔍 **Insight:** Estas películas tienen pocos alquileres pero generan ingresos altos. Podrían tratarse de títulos premium, de nicho o con precios elevados. Merecen especial atención en la estrategia de distribución.")

        # --- Mostrar tabla de películas estratégicas ---
        st.subheader("📋 Películas Estratégicas")
        st.dataframe(peliculas_interes[['pelicula', 'total_alquileres', 'total_ingresos']])

        # --- Mostrar porcentaje representado ---
        porcentaje_peliculas = len(peliculas_interes) / len(df_peliculas) * 100
        st.markdown(f"Estas **{len(peliculas_interes)} películas** representan aproximadamente el **{porcentaje_peliculas:.2f}%** del total analizado.")



    

# --- TAB 5: INGRESOS POR TIENDA Y CATEGORÍA ---
with tab5:
    
    st.markdown("<div class='section-title'>🏬 Análisis de Ingresos por Tienda y Categoría</div>", unsafe_allow_html = True)
    st.dataframe(df_ingresos.head())
    
    # --- KPIs GENERALES ---
    st.markdown("<hr>", unsafe_allow_html = True)
    st.markdown("<div class='section-title'>📈 KPIs Generales</div>", unsafe_allow_html = True)

    total_tiendas = df_ingresos["store_id"].nunique()
    categorias_unicas_ing = df_ingresos["categoria"].nunique()

    top_cat_global = df_ingresos.loc[df_ingresos["ingresos"].idxmax()]
    cat_top = top_cat_global["categoria"]
    monto_top = top_cat_global["ingresos"]
    tienda_top = top_cat_global["store_id"]
   
    # KPIs como tarjetas
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.markdown(f"<div class='metric-card'><h3>🏢 Tiendas analizadas</h3><h2>{total_tiendas}</h2></div>", unsafe_allow_html = True)
    kpi2.markdown(f"<div class='metric-card'><h3>🛍️ Categorías distintas</h3><h2>{categorias_unicas_ing}</h2></div>", unsafe_allow_html = True)
    kpi3.markdown(f"<div class='metric-card'><h3>🏆 Categoría lider global</h3><h2>{cat_top} <br> (${monto_top:,.2f}) <br> (Tienda {tienda_top}) </h2></div>", unsafe_allow_html = True)
    
    # --- GRÁFICOS ---
    st.markdown("<hr>", unsafe_allow_html = True)
    st.markdown("<div class='section-title'>📊✨ Visualizaciones</div>", unsafe_allow_html = True)
    
    
    # --- Seleccionar las 5 categorías con mayores ingresos globales ---
    top5_cats = (
        df_ingresos.groupby('categoria')['ingresos']
                .sum().nlargest(5).index
    )
    df_top5 = df_ingresos[df_ingresos['categoria'].isin(top5_cats)].copy()

    # --- Gráfico de barras agrupadas con Plotly ---
    fig_ingresos_tienda_cat = px.bar(
        df_top5,
        x = 'store_id',
        y = 'ingresos',
        color = 'categoria',
        barmode = 'group',
        text = 'ingresos',
        title = '🏬 Ingresos por Tienda - Top 5 Categorías',
        template = 'plotly_dark',
        color_discrete_sequence = px.colors.qualitative.Set2,
        labels = {'store_id': 'Tienda', 'ingresos': 'Ingresos ($)', 'categoria': 'Categoría'}
    )

    fig_ingresos_tienda_cat.update_traces(
        texttemplate = '%{text:.2f}', textposition = 'outside'
    )

    fig_ingresos_tienda_cat.update_layout(
        xaxis_title = 'ID de Tienda',
        yaxis_title = 'Ingresos ($)',
        legend_title_text='Categoría',
        margin = dict(l = 40, r = 40, t = 60, b = 40)
    )

    # --- Mostrar gráfico ---
    st.plotly_chart(fig_ingresos_tienda_cat, use_container_width = True)

    # --- Insight profesional ---
    st.caption("🔍 **Insight:** Este gráfico compara los ingresos generados por las principales categorías de películas en cada tienda. Permite identificar fortalezas o carencias por tienda y especializar estrategias de catálogo.")

        
        
        
        
    # --- Crear pivot table con % de ingresos por categoría y tienda ---
    
    pivot_pct = (
        df_ingresos.pivot(index = 'categoria', columns = 'store_id', values = 'pct_ingreso_tienda')
                .fillna(0).round(1)
    ).reset_index()

    # Convertir columnas numéricas a string para que Plotly las trate como categóricas
    pivot_pct.columns = pivot_pct.columns.astype(str)

    # Melt para plotly
    df_heatmap = pivot_pct.melt(id_vars = 'categoria', var_name = 'store_id', value_name = 'pct_ingreso')

    # --- Gráfico tipo Heatmap con corrección ---
    fig_heatmap_pct = px.density_heatmap(
        df_heatmap,
        x = 'store_id',
        y = 'categoria',
        z = 'pct_ingreso',
        text_auto = True,
        color_continuous_scale = 'Viridis',
        title = '🔥 Heatmap: % de Ingresos por Categoría y Tienda',
        labels = {'store_id': 'Tienda', 'categoria': 'Categoría', 'pct_ingreso': '% Ingreso'},
        template = 'plotly_dark'
    )

    fig_heatmap_pct.update_layout(
        xaxis_title = 'Tienda',
        yaxis_title = 'Categoría',
        margin = dict(l = 40, r = 40, t = 60, b = 40),
        coloraxis_colorbar = dict(title = "% Ingreso")
    )

    # Mostrar en dashboard
    st.plotly_chart(fig_heatmap_pct, use_container_width = True)
    st.caption("🔍 **Insight:** Este heatmap resalta el porcentaje que representa cada categoría en el total de ingresos por tienda.")

        
## para ejecutar el script:  python -m streamlit run app_dashboard.py

