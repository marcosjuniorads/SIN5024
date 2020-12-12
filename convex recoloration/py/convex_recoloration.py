import gurobipy as gp
from gurobipy import GRB
from functions_model import *
from functions_files import *
import numpy as np

# path do arquivo
filename = '\exemplo_simples.txt'
path = 'E:\SIN5024\convex recoloration\instancias' + filename

# Criando o modelo
m = gp.Model("recoloration_convex")

# obtendo dados dos arquivos
df = obter_variaveis(path)

# obtendo a lista de variaveis e respectivos coeficientes para função objetivo
lista_variaveis = df['nome_variavel']
lista_coeficientes = df['coeff']

# CRIANDO AS VARIÁVEIS DO MODELO ----------------------------------------------
variables = adicionar_variaveis_modelo(model=m,
                                       lista_variaveis=lista_variaveis,
                                       name="variaveis_modelo")

# ADICIONANDO EXPRESSÃO LINEAR DA FUNÇÃO OBJETIVO -----------------------------
linear_expression = LinExpr()
for i in range(1, len(lista_variaveis)):
    linear_expression.add(variables.values()[i], lista_coeficientes[i])
m.setObjective(linear_expression, GRB.MINIMIZE)


# PRIMEIRA RESTRIÇÃO > garantindo que todos os vértices sejam pintados
# ENCONTRANDO OS INDICES DAS VARIÁVEIS
for numero_vertice in map(int, obter_lista_vertices(path)):
    # obtendo indices das variáveis do vertice N, que devem ser somados em
    # uma restrição linear para garantir que assumam apenas uma cor.
    # Nesse caso, itero por cada vertice X de cor 'qualquer', para
    # posteriomente somar todos quando construo a restrição.
    indices = [n for n, l in enumerate(lista_variaveis) if
               l.startswith('vertice' + str(numero_vertice))]

    # criando a expressão linear, a partir dos indices encontrados.
    linear_expression = LinExpr()

    for i in indices:
        linear_expression.add(variables.values()[i], 1)

    # adicionando constraint para o respectivo value
    m.addConstr(linear_expression, "==", 1)

# SEGUNDA RESTRIÇÃO > garantindo convexidade entre os vértices (PRIMEIRA COR)


# Otimizando o problema
m.optimize()

for v in m.getVars():
    print('%s %g' % (v.varName, v.x))

