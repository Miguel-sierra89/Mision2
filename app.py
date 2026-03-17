import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Climate & Energy Dashboard", layout="wide")

# Intentar conexión a MySQL
def get_data_from_sql():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Metallica89.", # <--- Pon tu clave
        database="climate_energy_db"
    )
    query = """
        SELECT c.country_name as country, cl.report_date as date, 
               cl.co2_emissions, e.energy_consumption, e.renewable_share
        FROM countries c
        JOIN climate_metrics cl ON c.country_id = cl.country_id
        JOIN energy_metrics e ON c.country_id = e.country_id AND cl.report_date = e.report_date
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.title("🌍 Dashboard de Clima y Energía")

try:
    # Intentamos SQL primero (Plan A)
    df = get_data_from_sql()
    st.success("✅ Conectado a MySQL exitosamente")
except Exception as e:
    # Si falla, usamos el CSV (Plan B - ¡Salvavidas!)
    st.warning("⚠️ No se pudo conectar a MySQL. Cargando datos desde el archivo CSV para la demostración.")
    df = pd.read_csv('global_climate_energy_2020_2024.csv')

# --- El resto del dashboard es igual ---
pais_seleccionado = st.selectbox("Selecciona un País:", df['country'].unique())
df_filtrado = df[df['country'] == pais_seleccionado]

col1, col2 = st.columns(2)
with col1:
    fig1 = px.line(df_filtrado, x='date', y='co2_emission' if 'co2_emission' in df.columns else 'co2_emissions', title="Emisiones de CO2")
    st.plotly_chart(fig1)

with col2:
    fig2 = px.bar(df_filtrado, x='date', y='energy_consumption', title="Consumo de Energía")
    st.plotly_chart(fig2)