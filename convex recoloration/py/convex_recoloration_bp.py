import gurobipy as gp
from gurobipy import GRB
from functions_model import *
from functions_files import *
import os

# path do arquivo
diretorio = str('E:\\SIN5024\\convex recoloration\\instancias\\')
diretorio_resultados = str('E:\\SIN5024\\convex recoloration\\py\\results\\')

# obtendo a lista de arquivos
# files = os.listdir(diretorio)

file = 'exemplo_simples.txt'

# Atualizando o caminho do código
path = diretorio + file

# Criando o modelo
m = gp.Model("recoloration_convex")

# obtendo dados dos arquivos
lista_caminhos = obter_caminho_possiveis_porcor(path)
lista_cores_vertices = obter_lista_cores(path, False)

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
for i in range(0, len(lista_caminhos)):
    linear_expression.add(variables.values()[i],
                          lista_caminhos["coeficientes"][i])
    m.setObjective(linear_expression, GRB.MINIMIZE)
