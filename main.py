# Projeto Analises De Vendas"
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import warnings
warnings.filterwarnings("ignore")

#locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

# Cofiguração para o carregamento dos dados
@st.cache_data(ttl=1800)
def Dados():
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


# Carregando os dados Teste
df = Dados()
representantes = sorted(df['Nome_representante'].unique())
estados = sorted(df['Estado_cliente'].unique())

# Configurando a Página do Streamlit
st.set_page_config(
  "Dash Executivo de Vendas",
  layout='wide',
  page_icon='📊',
  initial_sidebar_state='expanded')

st.title("💯 Inteligencia de Negocios e Analises Preditivas")
st.divider()


# Filtros de Analises
st.sidebar.header("Filtros Para Analises")
F_estados = st.sidebar.multiselect("Selecione Estado", estados,default=estados)
F_representante = st.sidebar.multiselect("Selecione Representante",representantes,default=representantes)

#-------------------------------------------------------------------------------------------------------
# Esse comando usamos para o selectbox
#df_Filtrado = df[(df["Estado_cliente"] == F_estados) & (df["Nome_representante"] == F_representante)] 
#-------------------------------------------------------------------------------------------------------
# Esse comando usamos para o multiselect
df_Filtrado = df[(df["Estado_cliente"].isin(F_estados)) & (df["Nome_representante"].isin(F_representante))] 
st.dataframe(df_Filtrado)

# KPI Financeiro Metricas Principais
st.subheader("🎯 KPI Pricipais")
col1, col2, col3, col4 = st.columns(4)
faturamento_total = df_Filtrado['Valor_total_venda'].sum()
ticket_medio = df_Filtrado['Valor_total_venda'].mean()
total_pedidos = df_Filtrado['Id_pedido'].nunique()
clientes_ativos = df_Filtrado['Nome_cliente'].nunique()

col1.metric("Faturamento Total", f"R$ {faturamento_total:,.2f}")
col2.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")
col3.metric("Total de Pedidos", f"{total_pedidos}")
col4.metric("Clientes Ativos", f"{clientes_ativos}")
st.divider()

# Analise de desempenho
st.subheader('📈 Analises de Desempenho')
tab1, tab2, tab3, tab4 = st.tabs(["Regional & Comercial", "Produtos", "Série Temporal", "Simulação Crescimento"]) 

with tab1:
  col_1, col_2 = st.columns(2)
  figura_Estado = px.bar(df_Filtrado.groupby('Estado_cliente')['Valor_total_venda']
                        .sum().reset_index(),
                        x = 'Estado_cliente', 
                        y = 'Valor_total_venda',
                        title = 'Receita por Estado',
                        color = 'Valor_total_venda'
  )
  
  figura_representante = px.bar( df_Filtrado.groupby('Nome_representante')['Valor_total_venda']
                              .sum()
                              .sort_values()
                              .reset_index(),
                              y = 'Nome_representante',
                              x = 'Valor_total_venda',
                              orientation= 'h',
                              title = 'Ranking Representantes'

  ) 

  col_1.plotly_chart(figura_Estado,use_container_width=True)
  col_2.plotly_chart(figura_representante,use_container_width=True)


with tab2:
  figura_produto = px.treemap(df_Filtrado, path=['Nome_produto'],
                  values='Valor_total_venda',
                  title='Participação por Produtos')

  st.plotly_chart(figura_produto,use_container_width=True)

with tab3:
  faturamento_Mensal = df_Filtrado.groupby('Mes_ano')['Valor_total_venda'].sum().reset_index()
  figura_Line = px.line(faturamento_Mensal,
                        x='Mes_ano',
                        y='Valor_total_venda',
                        title="Evolução Mensal do Faturamento", markers=True)  
  
  st.plotly_chart(figura_Line,use_container_width=True)


# Criando a area preditiva
with tab4:
  col_sim1, col_sim2 = st.columns([1, 2])

  with col_sim1:
      st.write("**Parâmetros de Simulação**")
      crescimento_volume = st.slider("Crescimento no Volume (%)", -50, 100, 10)
      ajuste_preco = st.slider("Ajuste no Preço Unitário (%)", -50, 50, -5)

      # Cálculos da Simulação
      faturamento_base = df_Filtrado['Valor_total_venda'].sum()
      faturamento_simulado = (df_Filtrado['Valor_produto'] * (1 + ajuste_preco/100) * df_Filtrado['Quantidade_vendida'] * (1 + crescimento_volume/100)).sum()
      variacao = ((faturamento_simulado / faturamento_base) - 1) * 100

  with col_sim2:
      fig_sim = go.Figure(go.Indicator(
          mode = "gauge+number+delta",
          value = faturamento_simulado,
          title = {'text': "Faturamento Projetado (R$)"},
          delta = {'reference': faturamento_base, 'relative': True, 'position': "top"},
          gauge = {'axis': {'range': [None, faturamento_base * 2]},
                   'bar': {'color': "darkblue"},
                   'steps': [
                       {'range': [0, faturamento_base], 'color': "lightgray"},
                       {'range': [faturamento_base, faturamento_base * 2], 'color': "lightgreen"}]}))
      st.plotly_chart(fig_sim, use_container_width=True)
  st.info(f"🚨O impacto real no caixa com essas alterações será de **{variacao:.2f}%** em relação ao faturamento atual.")

  