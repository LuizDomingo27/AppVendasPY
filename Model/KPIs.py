#%%
import pandas as pd
import streamlit as st
from Model import Repository as rp

# Agrupando os top 10 produtos
#%%
@st.cache_data(ttl=1200)
def TopThenProducts():
  DF = rp.df
  df_topThen = DF.groupby(['Id_produto', 'Nome_produto'], as_index=False).agg(
    Faturamento=('Valor_total_venda', 'sum'),
    Quantidade =('Quantidade_vendida', 'sum'),
    Pedido= ('Id_pedido', 'nunique')  
  ).sort_values('Faturamento',ascending=False)
  
  return df_topThen


@st.cache_data(ttl=1000)
def ClientesCanal():
  DF = rp.df
  df_ClienteCanal = DF.groupby('Nome_cliente', as_index=False).agg(
    Faturamento = ('Valor_total_venda','sum'),
    Quantidade = ('Quantidade_vendida','sum'),
    Pedidos = ('Id_pedido', 'nunique')
  ).sort_values('Faturamento', ascending=False)

  return df_ClienteCanal



dfRepresentante = ClientesCanal()
dfProducts = TopThenProducts()    