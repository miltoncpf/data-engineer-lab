import psycopg2
import pandas as pd

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
    df[['cliente_id', 'nome', 'cidade']]
    .itertuples(index=False, name=None)
)

cursor.executemany("""
    INSERT INTO clientes (cliente_id, nome, cidade)
    VALUES (%s, %s, %s)

	ON CONFLICT(cliente_id)
	DO UPDATE SET
		nome = EXCLUDED.nome,
		cidade = EXCLUDED.cidade
    """, dados)



conn.commit()
