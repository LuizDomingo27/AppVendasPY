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

#%%
@st.cache_data(ttl=1000)
def ClientesCanal():
   DF = rp.df
   df_ClienteCanal = DF.groupby('Nome_cliente', as_index=False).agg(
    Faturamento = ('Valor_total_venda','sum'),
    Quantidade = ('Quantidade_vendida','sum'),
    Pedidos = ('Id_pedido', 'nunique')
   ).sort_values('Faturamento', ascending=False)

   return df_ClienteCanal

#%%
def FaturamantoCiddeCliente():
   DF = rp.df
   dfCidade = DF.groupby('Cidade_cliente',as_index=False).agg(
      Faturamento = ('Valor_total_venda','sum'),
      Quantidade = ('Quantidade_vendida', 'sum'),
      Pedido = ('Id_pedido','nunique')
   ).sort_values('Faturamento', ascending=False)
  
   return dfCidade


def TopConcentracao(dfRank, colFaturamento, topN=5):
   total = dfRank[colFaturamento].sum()
   top = dfRank.head(topN)[colFaturamento].sum()
   return top, total, top/total 



dfRepresentante = ClientesCanal()
dfProducts = TopThenProducts()  
dfFaturamentoCidade = FaturamantoCiddeCliente()  