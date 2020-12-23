import gurobipy as gp
from gurobipy import GRB
from functions_model import *
from functions_files import *
import os
import pandas as pd
import time
pd.set_option('max_colwidth', 100000)

# Path do arquivo de entrada fornecidos como insumo para o processamento
diretorio = str('E:\\SIN5024\\convex recoloration\\instancias\\')
diretorio_resultados = str('E:\\SIN5024\\convex recoloration\\py\\results\\')

# obtendo a lista de arquivos no respectivo diretório
files = os.listdir(diretorio)

# Criando um dataframe para armazenar o tempo de processamento de cada arquivo
df_tempo_processamento = pd.DataFrame(columns=['Nome_instancia',
                                               'Tempo_processamento_segundos'])

for file in files:
    start = time.time()
    print(file)

    # Atualizando o caminho do código
    path = diretorio + file

    # Criando o modelo
    m = gp.Model("recoloration_convex_with_pattern")

    # obtendo dados dos arquivos
    lista_caminhos = obter_caminho_possiveis_porcor(path, False)
    lista_cores_vertices = obter_lista_cores(path, True)

    # buscando os dados das coeficientes das respectivas variáveis
    lista_caminhos = adicionar_coeficientes_caminho(lista_cores_vertices,
                                                    lista_caminhos)

    # CRIANDO AS VARIÁVEIS DO MODELO ------------------------------------------
    # variables = adicionar_variaveis_modelo(m, lista_variaveis,
    # "modelo_var")
    variables = m.addVars(lista_caminhos["Nome"], vtype=GRB.BINARY, name="var")

    # ADICIONANDO EXPRESSÃO LINEAR DA FUNÇÃO OBJETIVO -------------------------
    # inicializando a expressão com a primeira variável
    linear_expression = LinExpr()
    for i in range(0, len(variables)):
        linear_expression.add(variables.values()[i],
                              lista_caminhos["coeficientes"][i])
        m.setObjective(linear_expression, GRB.MINIMIZE)

    # ADICIONANDO EXPRESSÃO LINEAR DA PRIMEIRA RESTRICAO ----------------------
    # Iterando sobre os vértices da solução para garantir que estejam apenas
    # 1 cam.
    for vertice in obter_lista_vertices(path):
        nome_vertice = 'vertice' + vertice + '_'
        # encontrando todos os caminhos que possuem o respectivo vertice
        index = encontrar_caminhos_com_vertice(lista_caminhos, nome_vertice)

        linear_expression = LinExpr()
        for idx in index:
            linear_expression.add(variables.values()[idx], 1)
        m.addConstr(linear_expression, "==", 1)

    # ADICIONANDO EXPRESSÃO LINEAR DA SEGUNDA RESTRICAO -----------------------
    # Impedindo que um mesmo caminho, composto pelos mesmos vértices, porém de
    # cores distintas sejam pintados de mais de uma cor. Todos os caminhos =
    # com cores diferentes tem que ser <= 1.
    dictionary = {}
    # Criando as variavéis no dicionario por cor, antes de popular os caminhos
    for item in obter_lista_cores(path, False):
        dictionary['cor' + item] = []

    # Preenchendo o dicionário com a lista de caminhos para cada cor.
    # Abaixo, busco todos os caminhos que são pintados de uma mesma cor e os
    # adiciono em uma lista que tem o nome da cor.
    for cor in obter_lista_cores(path, False):
        nome_cor = '_cor' + cor
        tmp_list = list(filter(lambda k: nome_cor in k, lista_caminhos['Nome']))
        dictionary['cor' + cor] = [string for string in tmp_list if
                                   string.endswith('cor' + cor)]

    # Criando a resrtrição linear que IMPEDE com que um mesmo caminho seja
    # pintado de duas ou mais cores
    for row in list(range(len(dictionary["cor" +
                                         str(obter_primeira_cor(path))]))):
        linear_expression = LinExpr()
        for key in dictionary.keys():
            linear_expression.add(variables[dictionary[key][row]], 1)
        m.addConstr(linear_expression, "<=", 1)

    gerando_relatorio_otimizacao(diretorio_resultados,
                                 file,
                                 m,
                                 obter_numero_vertices(path),
                                 obter_numero_cores(path),
                                 obter_lista_vertices_cor(path),
                                 path_model=True,
                                 lista_caminhos=lista_caminhos,
                                 lista_cores=obter_lista_cores(path)
                                 )

    # Armazenando / salvando arquivo com resultados consolidados de processame
    df_tempo_processamento = df_tempo_processamento.append({
        'Nome_instancia': file,
        'Tempo_processamento_segundos': time.time() - start
    }, ignore_index=True)
    df_tempo_processamento.to_csv(diretorio_resultados +
                                  '_tempo_processamento.csv',
                                  index=False,
                                  header=True)


# Depois que terminar de montar o modelo
# Chamar o metodo solve ao inves de fazer model.solve()
# solve(m, lista_caminhos, variables, lista_cores_vertices, path)
