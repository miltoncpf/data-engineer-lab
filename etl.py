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
        nome VARCHAR(100),
        cidade VARCHAR(100)
    )
""")

cursor.execute(""" 
    INSERT INTO clientes (nome, cidade) 
    VALUES (%s, %s)
""", ("Milton", "Rio Preto"))

conn.commit()

cursor.execute("""SELECT id, nome, cidade 
                  FROM clientes
                  ORDER BY id""")

registros = cursor.fetchall()

for registro in registros:
    print(registro)

cursor.close()
conn.close()