import psycopg2

conn = psycopg2.connect(
    host="postgres",
    port=5432,
    dbname="etl",
    user="postgres",
    password="postgres"
)

print("Conectado com sucesso!!!")

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id SERIAL PRIMARY KEY,
	cliente_id INTEGER UNIQUE,
        nome VARCHAR(100),
        cidade VARCHAR(100)
    )
""")

conn.commit()

cursor.execute("""SELECT id, cliente_id, nome, cidade 
                  FROM clientes
                  ORDER BY id""")

registros = cursor.fetchall()

for registro in registros:
    print(registro)

cursor.close()
conn.close()
