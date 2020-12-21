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

# CRIANDO AS VARIÁVEIS DO MODELO ---------------------------------------------
# variables = adicionar_variaveis_modelo(m, lista_variaveis,
# "modelo_var")
variables = m.addVars(lista_caminhos["Nome"], vtype=GRB.BINARY, name="var")

# ADICIONANDO EXPRESSÃO LINEAR DA FUNÇÃO OBJETIVO -----------------------------
# inicializando a expressão com a primeira variável
linear_expression = LinExpr()
for i in range(0, len(lista_caminhos)):
    linear_expression.add(variables.values()[i],
                          lista_caminhos["coeficientes"][i])
m.setObjective(linear_expression, GRB.MINIMIZE)


# ADICIONANDO EXPRESSÃO LINEAR DA SEGUNDA RESTRICAO ---------------------------
caminhos_cor1 = list(filter(lambda k: '_cor1' in k, lista_caminhos['Nome']))
caminhos_cor2 = list(filter(lambda k: '_cor2' in k, lista_caminhos['Nome']))

for i in list(range(len(lista_caminhos['Nome']) - 1)):
    linear_expression = LinExpr()
    linear_expression.add(variables.values()[i], 1)
    m.addConstr(linear_expression, "==", 1)

# adicionando constraint para o respectivo value
m.addConstr(linear_expression, "==", 1)


# ENCONTRANDO CAMINHOS VÁLIDOS / HEURISTICA MATHEUS ---------------------------
heuristica = encontrar_caminhos_validos(lista_caminhos, variables,
                                        lista_cores_vertices)

# Depois que terminar de montar o modelo
# Chamar o metodo solve ao inves de fazer model.solve()
solve(m, lista_caminhos, variables, lista_cores_vertices)
# m.display()
