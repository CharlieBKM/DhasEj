# -*- coding: utf-8 -*-
"""
Created on Thu May 28 09:42:06 2026

@author: juan.mayaf
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Dashboard de Ventas", page_icon="📊", layout="wide")

# 2. Generación de datos de prueba (Simulación)
@st.cache_data
def cargar_datos():
    np.random.seed(42)
    fechas = pd.date_range(start="2026-01-01", periods=100, freq="D")
    productos = ["Producto 1", "Producto 2", "Producto 3"]
    regiones = ["Norte", "Sur", "Este", "Oeste"]
    
    datos = {
        "Fecha": np.random.choice(fechas, 500),
        "Producto": np.random.choice(productos, 500),
        "Región": np.random.choice(regiones, 500),
        "Ventas": np.random.randint(100, 1000, 500),
        "Ganancia": np.random.randint(20, 300, 500)
    }
    return pd.DataFrame(datos)

df = cargar_datos()

# 3. Título del Dashboard
st.title("📊 Dashboard Interactivo de Ventas")
st.markdown("Bienvenido al panel de control. Filtra los datos usando la barra lateral.")
st.write("---")

# 4. Barra Lateral (Sidebar) para Filtros
st.sidebar.header("Filtros Disponibles")
region_seleccionada = st.sidebar.multiselect(
    "Selecciona la Región:",
    options=df["Región"].unique(),
    default=df["Región"].unique()
)

producto_seleccionado = st.sidebar.multiselect(
    "Selecciona el Producto:",
    options=df["Producto"].unique(),
    default=df["Producto"].unique()
)

# Aplicar filtros a los datos
df_filtrado = df[(df["Región"].isin(region_seleccionada)) & (df["Producto"].isin(producto_seleccionado))]

# 5. Métricas Clave (KPIs)
col1, col2, col3 = st.columns(3)

if not df_filtrado.empty:
    total_ventas = df_filtrado["Ventas"].sum()
    total_ganancias = df_filtrado["Ganancia"].sum()
    margen_promedio = (total_ganancias / total_ventas) * 100
    
    col1.metric(label="Ventas Totales", value=f"${total_ventas:,}")
    col2.metric(label="Ganancias Totales", value=f"${total_ganancias:,}")
    col3.metric(label="Margen Promedio", value=f"{margen_promedio:.1f}%")
else:
    st.warning("No hay datos que coincidan con los filtros seleccionados.")

st.write("---")

# 6. Gráficos Interactivos
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Ventas por Producto")
    fig_bar = px.bar(
        df_filtrado, 
        x="Producto", 
        y="Ventas", 
        color="Región", 
        barmode="group",
        title="Total Ventas por Producto y Región"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_graf2:
    st.subheader("Evolución de Ventas en el Tiempo")
    df_linea = df_filtrado.groupby("Fecha")["Ventas"].sum().reset_index()
    fig_line = px.line(
        df_linea, 
        x="Fecha", 
        y="Ventas", 
        title="Tendencia de Ventas Diarias"
    )
    st.plotly_chart(fig_line, use_container_width=True)

# 7. Vista de la Tabla de Datos
st.write("---")
st.subheader("📋 Vista previa de los datos filtrados")
st.dataframe(df_filtrado, use_container_width=True)

