import pandas as pd
import numpy as np
import itertools
from itertools import combinations as comb


def obter_numero_vertices(path):
    df = pd.read_csv(path, header=None, nrows=1)
    return int(df.iloc[0].str.split(' ', 1, expand=True)[0])


def obter_numero_cores(path):
    df = pd.read_csv(path, header=None, nrows=1)
    return int(df.iloc[0].str.split(' ', 1, expand=True)[1])


def obter_lista_vertices_cor(path):
    df = pd.read_csv(path, header=None, names=['cor_atual'])
    df['vertice'] = df.index.values
    # removendo a primeira linha que não contém os dados da sequência.
    df = df.iloc[1:, ]
    return df


def obter_lista_cores(path, duplicated_values=True):
    df = pd.read_csv(path, header=None, names=['cores'])
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
    df = pd.read_csv(path, header=None, names=['cores'])
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
    vertice_cor[['vertice', 'cor']] = vertice_cor['vertice_cor'].str. \
        split(' ', expand=True)

    # criando uma nova coluna para armazenar o nome da variável a ser utilizada
    vertice_cor['nome_variavel'] = 'vertice' + \
                                   vertice_cor["vertice"] + \
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


def obter_caminho_possiveis_porcor(path):
    # Retornando todas as combinações possíves de caminho em um grafo
    combinacoes = []
    vertices = obter_lista_vertices(path)
    cores = obter_lista_cores(path, False)

    # Para cada cor, encontrando os caminhos possíveis
    for cor in cores:
        combinacoes.append(list(itertools.combinations([k + cor for k in
                                                        vertices], 2)))

    # Adicionando caminhos únicos também dentre as combinações possíveis
    paths_unicos = [str(v) + str(c) for v in vertices for c in cores]
    for p in paths_unicos:
        combinacoes.append([[p, p]])

    combinacoes = list(itertools.chain(*combinacoes))

    # Percorrendo a lista novamente e melhorando a estrutura
    path_dictionary = {"Nome": [], "Cor": [], "Nome_vertices": [],
                       "Vertices_caminho": []}
    n = 0

    for item in combinacoes:
        vertice_inicio = int(item[0][0:1])
        vertice_fim = int(item[1][0:1])
        cor = int(item[1][1:2])
        n += 1
        nome = 'caminho' + str(n) + '_cor' + str(cor)

        if vertice_inicio + 1 == vertice_fim:
            path = ['vertice' + str(vertice_inicio) + '_cor' + str(cor),
                    'vertice' + str(vertice_fim) + '_cor' + str(cor)]
            vert = [vertice_inicio, vertice_fim]

            # adicionando os dados do problema ao dicionário
            path_dictionary["Nome"].append(nome)
            path_dictionary["Cor"].append(cor)
            path_dictionary["Nome_vertices"].append(path)
            path_dictionary["Vertices_caminho"].append(vert)
        else:
            # dado um intervalo, cria uma sequência de números de x -> Y
            # incrementando sempre 1
            vert = [k for k in list(range(vertice_inicio, vertice_fim + 1, 1))]
            path = ['vertice' + str(k) + '_cor' + str(cor) for k in vert]

            # adicionando os dados do problema ao dicionário
            path_dictionary["Nome"].append(nome)
            path_dictionary["Cor"].append(cor)
            path_dictionary["Nome_vertices"].append(path)
            path_dictionary["Vertices_caminho"].append(vert)

    return path_dictionary


def adicionar_coeficientes_caminho(lista_cores_vertices, lista_caminhos):
    # Criando uma nova chave para armazenar os coeficientes
    lista_caminhos["coeficientes"] = []

    # os coeficientes refletiram a quantidade de trocas necessárias,
    # possivelmente, para o caminho assumir a cor de referência.
    for item in list(range(0, len(lista_caminhos["Vertices_caminho"]))):
        cor = str(lista_caminhos['Cor'][item])
        coef = 0
        for vertice_caminho in list(range(0, len(lista_caminhos[
                                                   "Vertices_caminho"][item]))):
            if lista_cores_vertices[vertice_caminho] == cor:
                coef = coef + 1
        lista_caminhos['coeficientes'].append(coef)

    return(lista_caminhos)


def adicionar_coluna(caminho):
    print("parei aqui")


# Verifica se nenhum elemento do comparavel se repete na base
def check_repetido(base, comparavel, lista_caminhos):
    retorno = False

    for i in range(0, len(base)):

        aux = base[i]

        for j in range(0, len(comparavel)):

            if comparavel[j] in base or comparavel[j][0:8] in aux:
                retorno = True

    return retorno


# Pega todas as combinações de caminho e monta combinações válidas.
# Essas devem respeitar as seguintes regras: começar sempre do primeiro vértice
# Não repetir cor, ter sempre o tamanho do caminho original (tal como dado no
# problema), ser convexo e não ter vértices repetidos!
def encontrar_caminhos_validos(lista_caminhos, variables, lista_cores):
    # puxar isso dinamico depois
    TAMANHO_ARRAY_ORIGINAL = len(lista_cores)

    # copia_iteravel = lista_caminhos.get('Nome_vertices')
    copia_iteravel = lista_caminhos['Nome_vertices']

    caminhos_possiveis = []
    caminho = []
    L = 0

    v_adicionados = []

    for i in range(0, len(copia_iteravel)):

        aux = copia_iteravel[0]
        caminho = []
        caminho.append(aux)
        acumulador_contagem = copia_iteravel[0]

        # verificar se o caminho e apto a comecar uma sequencia
        if 'vertice1' in aux[0]:

            v_adicionados = v_adicionados + aux
            copia_iteravel.pop(0)

            for j in range(0, len(copia_iteravel)):

                # verificar se nao foi adicionado ainda
                if not check_repetido(aux, copia_iteravel[j],
                                      lista_caminhos):

                    # procurar um caminho que se combine com aux
                    if len(aux) + len(
                            copia_iteravel[j]) <= TAMANHO_ARRAY_ORIGINAL:
                        caminho.append(copia_iteravel[j])
                        acumulador_contagem = acumulador_contagem + \
                                              copia_iteravel[j]

                        if len(acumulador_contagem) == TAMANHO_ARRAY_ORIGINAL:
                            caminhos_possiveis.append(caminho)
                            acumulador_contagem = aux
                            caminho = []
                            caminho.append(aux)

                    if j == len(copia_iteravel) - 1 and len(
                            aux) == TAMANHO_ARRAY_ORIGINAL:
                        caminhos_possiveis.append(caminho)
                        acumulador_contagem = aux
                        caminho = []
                        caminho.append(aux)
        else:
            copia_iteravel.pop(0)

    return caminhos_possiveis


def solve(model, lista_caminhos, variables, lista_cores):
    caminhos_possiveis = encontrar_caminhos_validos(lista_caminhos,
                                                    variables,
                                                    lista_cores)

    # pra cada caminho possivel, achar uma coluna
    for i in range(0, len(caminhos_possiveis)):
        coluna = adicionar_coluna(caminhos_possiveis[i])

    print("teste")
