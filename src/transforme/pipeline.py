import pandas as pd
from datetime import datetime
import sqlite3

#Definir o caminho para o arquivo json
file_path = "../../data/data.json"
#Ler os dados do arquivo json
df = pd.read_json(file_path)

#Adicionar a coluna _source com o valor fixo
df['_source'] = "https://lista.mercadolivre.com.br/tenis-masculino"

#Add a coluna data_coleta com a data e hora atuais
df['data_coleta'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#Tratar os valores nulos para colunas numéricas e de texto
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_cents'] = df['old_cents'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_cents'] = df['new_cents'].fillna(0).astype(float)
df['rating_num'] = df['rating_num'].fillna(0).astype(float)

#tratar os preços como float e calcular os valores totais
df['old_price'] = df['old_price_reais'] + df['old_cents'] / 100
df['new_price'] = df['new_price_reais'] + df['new_cents'] / 100

#Excluir colunas de preço antigas
df_consolidado = df.drop(columns=['old_price_reais', 'old_cents', 'new_price_reais', 'new_cents'])

#conexão com o banco
conn = sqlite3.connect('../../data/mercadolivre_items.db')

#Salvar o DF no banco
df_consolidado.to_sql('mercadolivre_items', conn, if_exists='replace', index=False)

#Fechar conexão
conn.close()