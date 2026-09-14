import psycopg2
from psycopg2.extras import execute_values
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

dados = list(
    df[["cliente_id", "nome", "cidade"]]
    .itertuples(index=False, name=None)
)

#inicio do cronômetro
inicio = time.perf_counter()

execute_values(
    cursor, 
    """
    INSERT INTO clientes (cliente_id, nome, cidade)
    VALUES %s
	ON CONFLICT(cliente_id)
	DO UPDATE SET
		nome = EXCLUDED.nome,
		cidade = EXCLUDED.cidade
    """, 
    dados)

conn.commit()

#final do cronometro
fim = time.perf_counter()
print(f"Tempo: {fim - inicio:.4f} segundos")