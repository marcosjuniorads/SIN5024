import gurobipy as gp
from gurobipy import GRB
from functions_model import *
from functions_files import *
import os

# path do arquivo
diretorio = str('E:\\SIN5024\\convex recoloration\\instancias\\')
diretorio_resultados = str('E:\\SIN5024\\convex recoloration\\py\\results\\')
#diretorio = str('C:\\Users\\Matheus Ancelmo\\Documents\\Mestrado\\instancias\\')
#diretorio_resultados = str('C:\\Users\\Matheus Ancelmo\\Documents\\Mestrado\\results\\')

# obtendo a lista de arquivos
# files = os.listdir(diretorio)

file = 'exemplo_simples.txt'

# Atualizando o caminho do código
path = diretorio + file

# Criando o modelo
m = gp.Model("recoloration_convex")

# obtendo dados dos arquivos
lista_caminhos = obter_caminho_possiveis_porcor(path)
lista_cores_vertices = obter_lista_cores(path, True)

# buscando os dados das coeficientes das respectivas variáveis
lista_caminhos = adicionar_coeficientes_caminho(lista_cores_vertices,
                                                lista_caminhos)

# CRIANDO AS VARIÁVEIS DO MODELO ----------------------------------------------
# variables = adicionar_variaveis_modelo(m, lista_variaveis,
# "modelo_var")
variables = m.addVars(lista_caminhos["Nome"], vtype=GRB.BINARY, name="var")

# ADICIONANDO EXPRESSÃO LINEAR DA FUNÇÃO OBJETIVO -----------------------------
# inicializando a expressão com a primeira variável
linear_expression = LinExpr()
for i in range(0, len(variables)):
    linear_expression.add(variables.values()[i],
                          lista_caminhos["coeficientes"][i])
    m.setObjective(linear_expression, GRB.MINIMIZE)


# ADICIONANDO EXPRESSÃO LINEAR DA PRIMEIRA RESTRICAO --------------------------
# Iterando sobre os vértices da solução para garantir que estejam apenas 1 cam.
for vertice in obter_lista_vertices(path):
    nome_vertice = 'vertice' + vertice + '_'
    # encontrando todos os caminhos que possuem o respectivo vertice
    index = encontrar_caminhos_com_vertice(lista_caminhos, nome_vertice)

    linear_expression = LinExpr()
    for idx in index:
        linear_expression.add(variables.values()[idx], 1)
    m.addConstr(linear_expression, "==", 1)


# ADICIONANDO EXPRESSÃO LINEAR DA SEGUNDA RESTRICAO ---------------------------
dictionary = {}
# Criando as variavéis no dicionario por cor, antes de popular os caminhos
for item in obter_lista_cores(path, False):
    dictionary['cor' + item] = []

# Preenchendo o dicionário com a lista de caminhos para cada cor
for cor in obter_lista_cores(path, False):
    nome_cor = '_cor' + cor
    dictionary['cor' + cor] = list(filter(lambda k: nome_cor in k,
                                              lista_caminhos['Nome']))

# Criando a resrtrição linear que IMPEDE com que um mesmo caminho seja pintado
# de duas ou mais cores
for row in list(range(len(dictionary["cor1"]))):
    linear_expression = LinExpr()
    for key in dictionary.keys():
        linear_expression.add(variables[dictionary[key][row]], 1)
    m.addConstr(linear_expression, "<=", 1)


# Depois que terminar de montar o modelo
# Chamar o metodo solve ao inves de fazer model.solve()
solve(m, lista_caminhos, variables, lista_cores_vertices, path)

m.optimize()
m.display()
for v in m.getVars():
    print('%s %g' % (v.varName, v.x))
