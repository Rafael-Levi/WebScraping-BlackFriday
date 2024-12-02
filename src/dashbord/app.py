import sqlite3
import pandas as pd
import streamlit as st
# Conectar ao banco
conn = sqlite3.connect('../../data/mercadolivre_items.db')
#Carregar os dados da tabela 'mercadolivre_items' em um DF pandas
df = pd.read_sql_query("SELECT * FROM mercadolivre_items",conn)
#Fehcar a conexão
conn.close()
#Titulo
st.title("Levantamento de dados - Itens Mercado Livre")
#Melhorar o layout
st.subheader("Principais KPI's da análise")
col1,col2,col3 = st.columns(3)

#KPI 1:Número de itens
total_items = df.shape[0]
col1.metric("Total de Itens",value=total_items)

#KPI 2: Número de marcas únicas
unique_brands = df['brand'].nunique()
col2.metric("Número de marcas únicas.",value=unique_brands)

#KPI 3: Preço médio novo (em reais)
media_preco = df['new_price'].mean()
col3.metric("Média de preço (R$)",value=f"{media_preco:.2f}")

#Quais marcas são mais encontradas
st.subheader("Marcas mais encontradas")
col1,col2 = st.columns([4,2])

top_brands = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_brands)
col2.write(top_brands)

#Média de preço por marca
st.subheader("Médias de preço por marca")

col1,col2 = st.columns([4,2])
media_preco_marca = df.groupby('brand')['new_price'].mean().round(2)
col1 = st.bar_chart(media_preco_marca)
col2 = st.write(media_preco_marca)

#Satisfação por marca
st.subheader("Satisfação por marca")
col1,col2 = st.columns([4,2])
df_non_zero_reviews = df[df['rating_num']>0]
satisfacao_marca = df_non_zero_reviews.groupby('brand')['rating_num'].mean().sort_values(ascending=False).round(2)
col1.bar_chart(satisfacao_marca)
col2.write(satisfacao_marca)