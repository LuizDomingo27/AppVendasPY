import pandas as pd
import streamlit as st


@st.cache_data(ttl=1800)
def Load_Data():
  path = "datasets/Vendas.xlsx"
  DF = pd.read_excel(path, skiprows = 1)

  # Padronizando as colunas"
  DF.columns = [col.strip().capitalize() for col in DF.columns]
  DF.columns.tolist()

  # Tratamento dos tipos de features de datas"
  DF['Data_pedido'] = pd.to_datetime(DF['Data_pedido'], errors='coerse', dayfirst=True)

  # Criando as colunas Ano - Mês_num - Mês_nome - Dia
  DF.drop('Mês', axis=1,inplace=True) # Excluindo a coluna ano 
  DF['Ano'] = DF['Data_pedido'].dt.year
  DF['Mes_num'] = DF['Data_pedido'].dt.month
  DF['Mes_ano'] = DF['Data_pedido'].dt.to_period('M').astype('str')
  DF['Mes_nome'] = DF['Data_pedido'].dt.month_name(locale='pt_BR').str.capitalize()
  DF['Dia'] = DF['Data_pedido'].dt.day
  return DF

df = Load_Data()