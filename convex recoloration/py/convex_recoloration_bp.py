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

# CRIANDO AS VARIÁVEIS DO MODELO ------------------------------------------
# variables = adicionar_variaveis_modelo(m, lista_variaveis,
# "modelo_var")
variables = m.addVars(list(lista_caminhos.keys()), vtype=GRB.BINARY, name="var")

# ADICIONANDO EXPRESSÃO LINEAR DA FUNÇÃO OBJETIVO -------------------------
# inicializando a expressão com a primeira variável
linear_expression = LinExpr()
for i in range(0, len(lista_caminhos)):
    linear_expression.add(variables.values()[i], 1)
    m.setObjective(linear_expression, GRB.MINIMIZE)
