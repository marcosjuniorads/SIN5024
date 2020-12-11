import pandas as pd
import os

# path de exemplo:
# os.getcwd() + '\convex recoloration\instancias\exemplo_simples.txt'
def obter_numero_vertices(path):
    df = pd.read_csv(path,  header=None, nrows=1)
    return int(df.iloc[0].str.slice(0, 1))


# path de exemplo:
# os.getcwd() + '\convex recoloration\instancias\exemplo_simples.txt'
def obter_numero_cores(path):
    df = pd.read_csv(path,  header=None, nrows=1)
    return int(df.iloc[0].str.slice(1))


# path de exemplo:
# os.getcwd() + '\convex recoloration\instancias\exemplo_simples.txt'
def obter_lista_vertices(path):
    df = pd.read_csv(path,  header=None, names=['cores'])
    df['ver'] = df.index.values
    df['variaveis'] = 'vertice_' + df["ver"].astype(str) + '_cor_' + df["cores"]
    # removendo a primeira linha que não contém os dados da sequência.
    df = df.iloc[1:, 2:]
    return df.values.tolist()
