import pandas as pd
import json

# Ler o arquivo CSV
df = pd.read_csv("test.csv", encoding='latin1', sep=';')

# Substituir NaN por None (que se torna null no JSON)
df = df.where(pd.notnull(df), None)

# Forçar as colunas numéricas para o tipo string, se necessário
df['NUMERO_REGISTRO_PRODUTO'] = df['NUMERO_REGISTRO_PRODUTO'].astype(str)
df['NUMERO_PROCESSO'] = df['NUMERO_PROCESSO'].astype(str)

# Converter o DataFrame para uma lista de dicionários (registros JSON)
data = df.to_dict(orient='records')

# Serializar os dados para JSON com caracteres especiais legíveis
with open("dados.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)