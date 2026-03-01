# Projeto Analises De Vendas"
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from Model import Repository as rp
from Model import KPIs as kp
import warnings

warnings.filterwarnings("ignore")

df = rp.df
representantes = sorted(df['Nome_representante'].unique())
estados = sorted(df['Estado_cliente'].unique())

# Configurando a Página do Streamlit
st.set_page_config(
  "Dash Executivo de Vendas",
  layout='wide',
  page_icon='📊',
  initial_sidebar_state='expanded')

st.title("💯 Inteligência de Negócios e Analises Preditivas")
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

# KPI Financeiro Metricas Principais
st.subheader("🎯 KPIs Principais")
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
tab1, tab2, tab3, tab4, tab5,tab6 = st.tabs(["Regional & Comercial",
               "Produtos", "Série Temporal",
               "Simulação Crescimento","Top 5 - 10",
               "% Concentração TOP CLientes"]) 

# Representante e Estado 
with tab1:
   col_1, col_2 = st.columns(2)
   figura_Estado = px.bar(df_Filtrado.groupby('Estado_cliente')['Valor_total_venda']
                        .sum().reset_index(),
                        x = 'Estado_cliente', 
                        y = 'Valor_total_venda',
                        title = 'Receita por Estado',
                        color = 'Valor_total_venda')
  
   figura_representante = px.bar( df_Filtrado.groupby('Nome_representante')['Valor_total_venda']
                              .sum()
                              .sort_values()
                              .reset_index(),
                              y = 'Nome_representante',
                              x = 'Valor_total_venda',
                              orientation= 'h',
                              title = 'Ranking Representantes') 

   col_1.plotly_chart(figura_Estado,use_container_width=True)
   col_2.plotly_chart(figura_representante,use_container_width=True)


# Participação dos Produtos 
with tab2:
   figura_produto = px.treemap(df_Filtrado, path=['Nome_produto'],
                  values='Valor_total_venda',
                  title='Participação por Produtos')

   st.plotly_chart(figura_produto,use_container_width=True)


# Faturamento Mensal
with tab3:
   faturamento_Mensal = df_Filtrado.groupby('Mes_ano')['Valor_total_venda'].sum().reset_index()
   figura_Line = px.line(faturamento_Mensal,
                        x='Mes_ano',
                        y='Valor_total_venda',
                        title="Evolução Mensal do Faturamento", markers=True)  

   faturamentoCidade = kp.dfFaturamentoCidade.head(4) 
   figuraCidade = px.bar(faturamentoCidade,
                        x='Cidade_cliente',
                        y='Faturamento',
                        title= 'Faturamento Top 4 Cidades', 
                      )

   figpiorCidades = px.bar(kp.dfFaturamentoCidade.tail(4),
                          x='Cidade_cliente',
                          y='Faturamento',
                          title='Faturamento Top 4 - Piores Cidade') 


   st.plotly_chart(figura_Line,use_container_width=True)
   st.plotly_chart(figuraCidade, use_container_width=True)
   st.plotly_chart(figpiorCidades)


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


# Top 5 Clientes - Top 10 Representantes
with tab5:
   Faturamento_Cliente = kp.dfRepresentante.head(5)  
   figura_Cliente = px.bar(data_frame=Faturamento_Cliente,
                           x='Nome_cliente',
                           y='Faturamento',
                           title= 'Top 5 CLientes' )
  
   topthenProducts = kp.dfProducts.head(10)
   figuraToprodutos = px.bar(data_frame=topthenProducts,
                       x='Nome_produto',
                       y='Faturamento',
                       title='Top 10 Produtos Por Faturamento')

   st.plotly_chart(figuraToprodutos,use_container_width=True)
   st.plotly_chart(figura_Cliente,use_container_width=True)


with tab6:
   topcolCliente, topColProduto, topColRepresentante = st.columns(3, gap="small", border=True)
   with topcolCliente:
      topcli, totalCli, perclCli = kp.TopConcentracao(kp.dfRepresentante,'Faturamento',5)
      st.metric("Top 5 Clientes Representa",f" R${topcli:,.2f}")
      st.metric("com uma participação de ",f"{perclCli:.1%} da receita")

   with topColRepresentante:
      repre = rp.df.groupby('Nome_representante', as_index=False).agg(Faturamento = ('Valor_total_venda','sum'))
      toprepre, totalrepre, percrepre = kp.TopConcentracao(repre,'Faturamento',5)   
      st.metric("Top 5 Representante Representa",f"R${toprepre:,.2f}")
      st.metric("com uma participação de",f"{percrepre:.1%} da receita")

   with topColProduto:
      toprod, totprod, percprod = kp.TopConcentracao(kp.dfProducts,'Faturamento',5) 
      st.metric("Os top 5 Produtos Representa ",f'R${toprod:,.2f}')
      st.metric("com uma participação de ",f'{percprod:.1%} da receita')
   
   # Grafico para Faturamento por categoria
   st.subheader("Faturamento por Categoria")
   dfCategoria = kp.dfCategorizar
   figuraCategoria = px.bar(data_frame=dfCategoria,
               x='Faturamento',
               y='Categoria',
               text_auto=True).update_traces(
                  textfont_size=15,
                  textangle=0,
                  textposition="outside")
   
   st.plotly_chart(figuraCategoria, use_container_width=True)   

   #Grafico para Faturamento por Mês, Ano
   dfMesAno = kp.dfFaturamentoMesANo
   ano = dfMesAno['Ano'].unique()[0]
   st.subheader(f"Faturamento Por Mês - Ano {ano} da Categoria")
   figuraMesAno = px.line(data_frame=dfMesAno,
               x='Mes_nome',
               y='Faturamento',
               hover_name='Categoria',
               color='Categoria',
               markers=True
            ).update_layout(xaxis_title='Mês'
            ).update_traces(mode='markers', marker=dict(size=19, symbol='circle')
            ).update_xaxes(showgrid=False
            ).update_yaxes(showgrid=False)

   st.plotly_chart(figuraMesAno,use_container_width=True)