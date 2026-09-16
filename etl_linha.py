import psycopg2
import pandas as pd
import time

df = pd.read_csv("clientes2.csv")
df["cidade"] = df["cidade"].fillna("Não informado")

conn = psycopg2.connect(
    host="postgres",
    port=5432,
    dbname="etl",
    user="postgres",
    password="postgres"
)

print("Conectado com sucesso!!!")

cursor = conn.cursor()

#inicio do cronometro
inicio = time.perf_counter()

for indice, linha in df.iterrows():

    cursor.execute("""
        INSERT INTO clientes (cliente_id, nome, cidade)
        VALUES (%s, %s, %s)

	ON CONFLICT(cliente_id)
	DO UPDATE SET
		nome = EXCLUDED.nome,
		cidade = EXCLUDED.cidade
    """, (
	linha["cliente_id"], 
	linha["nome"],
	linha["cidade"]
	))

conn.commit()

#final do cronometro
fim = time.perf_counter()

print(f"Tempo: {fim - inicio:.4f} segundos")