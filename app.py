# -*- coding: utf-8 -*-
"""
Created on Thu May 28 09:42:06 2026

@author: juan.mayaf
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import pyreadstat

# 1. Configuración de la página
st.set_page_config(page_title="Análisis", page_icon="📊", layout="wide")

# 2. Función para cargar el archivo .sav
@st.cache_data
def cargar_datos_sav(archivo):
    # pyreadstat lee el archivo; regresamos solo el DataFrame
    df = pd.read_spss(archivo)
    return df

# 3. Título del Dashboard
st.title("📊 Para Análisis")
st.write("---")

# 4. Barra Lateral (Sidebar) para Carga de Archivos y Filtros
st.sidebar.header("📁 Carga de Datos")
archivo_subido = st.sidebar.file_uploader("Selecciona un archivo .sav", type=["sav"])

# Control de flujo: Si hay archivo, procesamos; si no, mostramos advertencia.
if archivo_subido is not None:
    df = cargar_datos_sav(archivo_subido)
    
    st.sidebar.write("---")
    st.sidebar.header("Filtros Disponibles")
    
    # Al ser una encuesta externa, dejamos que el usuario elija qué columnas filtrar
    columnas_disponibles = df.columns.tolist()
    
    col_filtro_1 = st.sidebar.selectbox("1. Variable para filtrar (Categoría A):", columnas_disponibles, index=0)
    opciones_filtro_1 = st.sidebar.multiselect(
        f"Valores de {col_filtro_1}:",
        options=df[col_filtro_1].dropna().unique(),
        default=df[col_filtro_1].dropna().unique()
    )
    
    # Intentamos seleccionar una segunda columna diferente por defecto si existe
    indice_defecto = min(1, len(columnas_disponibles) - 1)
    col_filtro_2 = st.sidebar.selectbox("2. Variable para filtrar (Categoría B):", columnas_disponibles, index=indice_defecto)
    opciones_filtro_2 = st.sidebar.multiselect(
        f"Valores de {col_filtro_2}:",
        options=df[col_filtro_2].dropna().unique(),
        default=df[col_filtro_2].dropna().unique()
    )

    # Aplicar filtros dinámicos
    df_filtrado = df[
        (df[col_filtro_1].isin(opciones_filtro_1)) & 
        (df[col_filtro_2].isin(opciones_filtro_2))
    ]

    # 5. Métricas Clave (KPIs básicas para encuestas)
    col1, col2, col3 = st.columns(3)
    
    if not df_filtrado.empty:
        total_respuestas = len(df_filtrado)
        total_original = len(df)
        porcentaje_Muestra = (total_respuestas / total_original) * 100
        
        col1.metric(label="Muestra Filtrada (n)", value=f"{total_respuestas:,}")
        col2.metric(label="Muestra Total Original", value=f"{total_original:,}")
        col3.metric(label="% del Total", value=f"{porcentaje_Muestra:.1f}%")
    else:
        st.warning("No hay datos que coincidan con los filtros seleccionados.")

    st.write("---")

    # 6. Gráficos Interactivos Adaptables
    st.subheader("📊 Análisis Visual de la Encuesta")
    
    columnas_numericas = df_filtrado.select_dtypes(include=['number']).columns.tolist()
    
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.write(f"### Distribución de: {col_filtro_1}")
        # Conteo de frecuencias para encuestas
        df_conteo = df_filtrado[col_filtro_1].value_counts().reset_index()
        df_conteo.columns = [col_filtro_1, 'Frecuencia']
        
        fig_bar = px.bar(
            df_conteo, 
            x=col_filtro_1, 
            y="Frecuencia", 
            color=col_filtro_1,
            title=f"Cantidad de respuestas por {col_filtro_1}"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_graf2:
        st.write("### Cruce de Variables / Tendencia")
        if columnas_numericas:
            # Si hay variables numéricas (ej. Edad, Escala de satisfacción), permitimos graficarla
            var_num = st.selectbox("Selecciona una variable numérica para el eje Y:", columnas_numericas)
            fig_box = px.box(
                df_filtrado, 
                x=col_filtro_2, 
                y=var_num, 
                color=col_filtro_2,
                title=f"Distribución de {var_num} según {col_filtro_2}"
            )
            st.plotly_chart(fig_box, use_container_width=True)
        else:
            # Si no hay numéricas, hacemos un gráfico de pastel del segundo filtro
            df_conteo2 = df_filtrado[col_filtro_2].value_counts().reset_index()
            df_conteo2.columns = [col_filtro_2, 'Frecuencia']
            fig_pie = px.pie(
                df_conteo2, 
                names=col_filtro_2, 
                values="Frecuencia", 
                title=f"Proporción de {col_filtro_2}"
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    # 7. Vista de la Tabla de Datos
    st.write("---")
    st.subheader("📋 Vista previa de los datos filtrados")
    st.dataframe(df_filtrado, use_container_width=True)

else:
    # Mensaje de espera si no se ha subido nada
    st.info("👋 Por favor, despliega la barra lateral y sube un archivo con extensión `.sav` para generar el reporte.")

