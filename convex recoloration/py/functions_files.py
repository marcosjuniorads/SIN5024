import pandas as pd
import numpy as np
import itertools
from itertools import combinations as comb


def obter_numero_vertices(path):
    df = pd.read_csv(path,  header=None, nrows=1)
    return int(df.iloc[0].str.slice(0, 1))


def obter_numero_cores(path):
    df = pd.read_csv(path,  header=None, nrows=1)
    return int(df.iloc[0].str.slice(1))


def obter_lista_vertices_cor(path):
    df = pd.read_csv(path,  header=None, names=['cor_atual'])
    df['vertice'] = df.index.values
    # removendo a primeira linha que não contém os dados da sequência.
    df = df.iloc[1:, ]
    return df


def obter_lista_cores(path, duplicated_values=True):
    df = pd.read_csv(path,  header=None, names=['cores'])
    # removendo a primeira linha que não contém os dados da sequência.
    df = df.iloc[1:, ]
    # transformando em uma lista
    df = df.values.tolist()
    # apenas simplicando a estrutura de lista / lista -> lista
    df = list(itertools.chain(*df))

    # dependendo do propósito, pode ser que queira obter a sequencia de cores
    # sem nenhuma manipulação, ou que para posterior permutação de listas as
    # cores não podem estar duplicadas. Portanto, faço esse check abaixo.
    if duplicated_values:
        return df
    else:
        cores_without_repetition = []
        for i in df:
            if i not in cores_without_repetition:
                cores_without_repetition.append(i)
        return cores_without_repetition


def obter_lista_vertices(path):
    df = pd.read_csv(path,  header=None, names=['cores'])
    # removendo a primeira linha que não contém os dados da sequência.
    df['ver'] = df.index.values
    # removendo a primeira linha que não contém os dados da sequência.
    df = df.iloc[1:, 1:]
    # transformando em uma lista
    df = df.values.tolist()
    # apenas simplicando a estrutura de lista / lista -> lista
    df = list(itertools.chain(*df))
    # convertendo lista de inteiro para string
    df = [str(i) for i in df]
    return df


def obter_combinacao_vertices(path):
    return list(comb(obter_lista_vertices(path), 3))


def obter_variaveis(path):
    # obtendo listas de vertices e cores
    vertices = obter_lista_vertices(path)
    cores = obter_lista_cores(path, duplicated_values=False)

    # encontrando a combinação entre todos os elementos de vertices e cores
    # possíveis, sem quaisquer repetições.
    vertice_cor = list([x + ' ' + y for x in vertices for y in cores])

    # convertendo para um dataframe para facilitar a manipulação e ordenando
    # pelo numero do vertice, para facilitar posterior validação.
    vertice_cor = pd.DataFrame(vertice_cor, columns=['vertice_cor'])
    vertice_cor[['vertice', 'cor']] = vertice_cor['vertice_cor'].str.\
                                      split(' ', expand=True)

    # criando uma nova coluna para armazenar o nome da variável a ser utilizada
    vertice_cor['nome_variavel'] = 'vertice' +\
                              vertice_cor["vertice"] +\
                              '_cor' + vertice_cor["cor"]
    vertice_cor['vertice'] = vertice_cor['vertice'].astype(str).astype(int)

    # criando uma nova coluna para armazenar o coeficiente dessa variável
    # que deverá ser utilizada para a função objetivo. Nesse caso, se a variável
    # já está pintada da mesma cor,
    df_cor_atual = obter_lista_vertices_cor(path)
    vertice_cor = pd.merge(vertice_cor,
                           df_cor_atual,
                           how='left',
                           on=['vertice'])

    vertice_cor['coeff'] = np.where(vertice_cor['cor_atual'] ==
                                    vertice_cor['cor'], 0, 1)

    return vertice_cor.loc[:, vertice_cor.columns != 'vertice_cor']

