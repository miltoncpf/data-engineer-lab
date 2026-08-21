import pandas as pd

df = pd.read_csv("clientes.csv")
df["cidade"] = df["cidade"].fillna("Não informado")

print(df)