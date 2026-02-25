
#%%
import pandas as pd
import streamlit as st


@st.cache_data(ttl=1800)
def LoadData():
  path = "datasets/Vendas.csv"
  DF = pd.read_csv(path, sep=';')
  return DF

df = LoadData()
