import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# Configuración de conexión
def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root", # Tu usuario de MySQL
        password="Metallica89.", # Tu contraseña
        database="climate_energy_db",
        port=3306
    )

st.set_page_config(page_title="EcoData Dashboard", layout="wide")
st.title("🌍 Dashboard de Clima y Energía")

try:
    conn = get_connection()
    
    # 1. Gráfico de Emisiones de CO2
    st.subheader("Emisiones de CO2 por País")
    query1 = """
    SELECT c.country_name, cl.co2_emissions, cl.report_date 
    FROM countries c 
    JOIN climate_metrics cl ON c.country_id = cl.country_id
    """
    df1 = pd.read_sql(query1, conn)
    fig1 = px.bar(df1, x="country_name", y="co2_emissions", color="country_name")
    st.plotly_chart(fig1)

    # 2. Comparativa Energía Renovable
    st.subheader("Cuota de Energía Renovable (%)")
    query2 = """
    SELECT c.country_name, e.renewable_share 
    FROM countries c 
    JOIN energy_metrics e ON c.country_id = e.country_id
    """
    df2 = pd.read_sql(query2, conn)
    fig2 = px.pie(df2, values='renewable_share', names='country_name')
    st.plotly_chart(fig2)

    conn.close()
except Exception as e:
    st.error(f"Error de conexión: {e}")
