# ---------------------------------------- DOCUMENTAÇÃO ---------------------------------------------------------
# OBJETIVO: Este projeto tem como objetivo processar dados de IoT, armazená-los em um banco de dados
# PostgreSQL rodando em container Docker, e exibi-los por meio de um dashboard interativo construído com Streamlit.
# URL dos dados: https://www.kaggle.com/datasets/atulanandjha/temperature-readings-iot-devices
# AUTOR: Pâmela Xisto
# DATA: 01/08/2025
# ----------------------------------------------------------------------------------------------------------------

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import os
from dotenv import load_dotenv


# Carregar variáveis do .env
load_dotenv()

# Utiliza SQLAlchemy para conectar ao PostgreSQL
def get_db_connection():
    return create_engine(os.getenv("DATABASE_URL"))

# Função para carregar dados de uma view
def load_data(view_name):
    engine = get_db_connection()
    return pd.read_sql(f"SELECT * FROM {view_name}", engine)

# Título do dashboard
st.title("Dashboard de Temperaturas IoT")

# Lê diretamente o CSV local
df = pd.read_csv("data/IOT-temp.csv")

# Renomear colunas do CSV
if 'room_id/id' in df.columns:
    df = df.rename(columns={'room_id/id': 'room_id'})
if 'out/in' in df.columns:
    df = df.rename(columns={'out/in': 'in_out'})
if 'noted_date' in df.columns:
    df['noted_date'] = pd.to_datetime(df['noted_date'], dayfirst=True)

st.write("Estrutura do Dataset:")
st.dataframe(df)

# Criar tabela no banco
engine = get_db_connection()
df.to_sql('temperature_logs', engine, if_exists='replace', index=False)
st.success("Dados enviados para o banco de dados.")

# Gráfico 1: Média de temperatura por dispositivo 
st.header("Média de Temperatura por Dispositivo")
df_avg_temp = load_data("avg_temp_por_dispositivo")
fig1 = px.bar(df_avg_temp, x="device_id", y="avg_temp", labels={"avg_temp":"Temperatura Média", "device_id":"Dispositivo"})
st.plotly_chart(fig1)

# Gráfico 2: Leituras por hora 
st.header("Leituras por Hora do Dia")
df_leituras_hora = load_data("leituras_por_hora")
fig2 = px.line(df_leituras_hora, x="hora", y="contagem", labels={"contagem":"Número de Leituras"})
st.plotly_chart(fig2)

# Gráfico 3: Temperaturas Máximas e Mínimas por dia 
st.header("Temperaturas Máximas e Mínimas por Dia")
df_temp_max_min = load_data("temp_max_min_por_dia")
fig3 = px.line(df_temp_max_min, x="data", y=["temp_max","temp_min"], labels={"value":"Temperatura"})
st.plotly_chart(fig3)
