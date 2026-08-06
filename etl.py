import psycopg2

con = psycopg2.connect(
    host='postgres',
    database='etl',
    user='postgres'
    password='postgres'
)

print ('Conctado com sucesso!!!')

con.close()