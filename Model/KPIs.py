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

# Vamos criar uma categoria macro de produto com base no nome_produto
def Categorizar_produto(nome):
    nome = str(nome).lower()
    if "notebook" in nome:
        return "Notebook"
    if "celular" in nome:
        return "Celular"
    if "smart tv" in nome or "tv" in nome:
        return "Smart TV"
    if "tablet" in nome:
        return "Tablet"
    if "mouse" in nome:
        return "Mouse"
    if "teclado" in nome:
        return "Teclado"
    if "ssd" in nome:
        return "SSD"
    if "webcam" in nome:
        return "Webcam"
    if "headphone" in nome:
        return "Headphone"
    if "carregador" in nome:
        return "Carregador"
    if "e-reader" in nome:
        return "E-Reader"
    if "caixa de som" in nome:
        return "Caixa de Som"
    return "Outros"


def ProdutoCategorizado():
   DF = rp.df
   DF['Categoria'] = DF['Nome_produto'].apply(Categorizar_produto)
   dfCategorizado = DF.groupby('Categoria', as_index=False).agg(
      Faturamento = ('Valor_total_venda','sum'),
      Quantidade = ('Quantidade_vendida','sum')
   ).sort_values('Faturamento',ascending=True)
   return dfCategorizado


def Faturamento_MesANo():
   DF = rp.df
   DF['Categoria'] = DF['Nome_produto'].apply(Categorizar_produto)
   df_Fatu_Mes_Cat = DF.groupby(['Ano','Mes_num','Mes_nome','Categoria'], as_index=False).agg(
      Faturamento = ('Valor_total_venda','sum')
   )
   return df_Fatu_Mes_Cat



dfFaturamentoMesANo = Faturamento_MesANo()
dfCategorizar = ProdutoCategorizado()
dfRepresentante = ClientesCanal()
dfProducts = TopThenProducts()  
dfFaturamentoCidade = FaturamantoCiddeCliente() 
