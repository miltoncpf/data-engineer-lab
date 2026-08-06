import psycopg2

conn = psycopg2.connect(
    host="postgres",
    port="5432",
    dbname="postgres",
    user="postgres",
    password="postgres",
)

print("Conexãi realizada com sucesso")

conn.close()

print("Conexão encerrada")