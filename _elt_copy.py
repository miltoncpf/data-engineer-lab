import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
from io import StringIO
import time


df = pd.read_csv("clientes2.csv")
df.columns = df.columns.str.strip().str.lower()

#Criando conexão com o banco de dados Postgres
conn = psycopg2.connect(
    host="postgres",
    port=5432,
    dbname="etl",
    user="postgres",
    password="postgres"
)

print("Conectado com sucesso!!!")
cursor = conn.cursor()

#Criando a tabela raw_clientes caso não exista
cursor.execute(
	"""CREATE TABLE IF NOT EXISTS raw_clientes(
	cliente_id INTEGER,
	nome VARCHAR(200),
	cidade VARCHAR(100)
	)"""
)
#Criando a view stg_clientes para tratar os dados da tabela raw_clientes
cursor.execute (
    """CREATE OR REPLACE VIEW stg_clientes AS
	SELECT
    	cliente_id,
    	nome,
    	COALESCE(cidade, 'Não informado') AS cidade
	FROM raw_clientes;""")

#Limpando a tabela raw_clientes antes de inserir novos dados
cursor.execute("TRUNCATE TABLE raw_clientes")

#inicio do cronômetro
inicio = time.perf_counter()

buffer = StringIO()

#Convertendo o  df para um fluxo CSV em memória para fazer o copy
df[["cliente_id", "nome", "cidade"]].to_csv(
	buffer,
	index=False,
	header=False
)

buffer.seek(0)

#======= 1) carrega snapshot atual na RAW
cursor.copy_expert(
    """
	COPY raw_clientes (cliente_id, nome, cidade)
	FROM STDIN
	WITH(
		FORMAT CSV
	)
    """, buffer)

#========= 2) INSERT / UPDATE / REATIVAÇÃO
cursor.execute(
	"""
	INSERT INTO clientes (cliente_id, nome, cidade, ativo)
	SELECT cliente_id, nome, cidade, TRUE
	FROM stg_clientes

	ON CONFLICT (cliente_id)
	DO UPDATE SET
		nome = EXCLUDED.NOME,
		cidade = EXCLUDED.cidade,
        ativo = TRUE
        
    -----Melhorando o UPSERT para de fato só atualizar os registros que tiveram alterações, 
	-----evitando atualizações desnecessárias
    WHERE
		clientes.nome IS DISTINCT FROM EXCLUDED.nome
		OR clientes.cidade IS DISTINCT FROM EXCLUDED.cidade
		OR clientes.ativo IS DISTINCT FROM TRUE
	""")

#======= 3) INATIVA quem não veio no snapshot atual
cursor.execute(
	"""
	UPDATE clientes c
    SET ativo = FALSE
    WHERE c.ativo = TRUE 
    	AND NOT EXISTS (
			SELECT 1
			FROM raw_clientes r
			WHERE r.cliente_id = c.cliente_id
	)
	"""
)

conn.commit()

#final do cronometro
fim = time.perf_counter()
print(f"Tempo: {fim - inicio:.4f} segundos")
