import pandas as pd

# Ler o arquivo CSV
df = pd.read_csv('D:\downloads\goeldi_2.csv', delimiter=';')

# Dividir cada coluna em um arquivo separado
for coluna in df.columns:
    df[coluna].to_csv(f'{coluna}.csv', sep=';', index=False, header=True)
