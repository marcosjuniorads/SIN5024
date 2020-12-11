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

# obtendo a lista de variaveis
lista_variaveis = obter_variaveis(path)
# definindo os coeficientes da função objetivo
lista_coeficientes = list(np.repeat(1, len(lista_variaveis)))

# Adicionando as variáveis ao modelo e obtendo modelo atualizado
variables = adicionar_variaveis_modelo(model=m,
                                       lista_variaveis=lista_variaveis,
                                       name="variaveis_modelo")

# Adicionando as variáveis ao modelo
# lista_variaveis = ["v1_cor1", "v1_cor2", "v2_cor1", "v2_cor2", "v3_cor1",
# "v3_cor2", "v4_cor1", "v4_cor2"]
# v1_cor1 = m.addVar(vtype=GRB.BINARY, name="v1_cor1")
# v1_cor2 = m.addVar(vtype=GRB.BINARY, name="v1_cor2")
# v2_cor1 = m.addVar(vtype=GRB.BINARY, name="v2_cor1")
# v2_cor2 = m.addVar(vtype=GRB.BINARY, name="v2_cor2")
# v3_cor1 = m.addVar(vtype=GRB.BINARY, name="v3_cor1")
# v3_cor2 = m.addVar(vtype=GRB.BINARY, name="v3_cor2")
# v4_cor1 = m.addVar(vtype=GRB.BINARY, name="v4_cor1")
# v4_cor2 = m.addVar(vtype=GRB.BINARY, name="v4_cor2")

# Criando a funcao objetivo, que no caso busca minimizar os custos
# m.setObjective(v1_cor2 + v2_cor1 + v3_cor1 + v4_cor2, GRB.MINIMIZE)

linear_expression = LinExpr(lista_coeficientes[0], variables.values()[0])
for i in range(1, len(lista_variaveis)):
    linear_expression.add(variables.values()[i], lista_coeficientes[i])
m.setObjective(linear_expression, GRB.MINIMIZE)


# PRIMEIRA RESTRIÇÃO > garantindo que todos os vértices sejam pintados
# lista_variaveis = [1, 1, 1, 1, 1, 1, 1, 1]
# lista_coeficientes = [1, 1, 1, 1, 1, 1, 1, 1]

# ENCONTRANDO OS INDICES DAS VARIÁVEIS
for numero_vertice in map(int, obter_lista_vertices(path)):
    # obtendo indices das variáveis do vertice N, que devem ser somados em
    # uma restrição linear para garantir que assumam apenas uma cor.
    indices = [n for n, l in enumerate(lista_variaveis) if
               l.startswith('vertice' + str(numero_vertice))]

    # criando a expressão linear, a partir dos indices encontrados.
    linear_expression = LinExpr(lista_coeficientes[0], variables.values()[0])

    for indices in range(1, len(indices)):
        linear_expression.add(variables.values()[indices], 1)

    # adicionando constraint para o respectivo value
    m.addConstr(linear_expression == 1)




m.addConstr(v1_cor1 + v1_cor2 == 1, "c0")
m.addConstr(v2_cor1 + v2_cor2 == 1, "c1")
m.addConstr(v3_cor1 + v3_cor2 == 1, "c2")
m.addConstr(v4_cor1 + v4_cor2 == 1, "c3")

# SEGUNDA RESTRIÇÃO > garantindo convexidade entre os vértices (PRIMEIRA COR)
m.addConstr(v1_cor1 - v2_cor1 + v3_cor1 <= 1, "c4")
m.addConstr(v1_cor1 - v2_cor1 + v4_cor1 <= 1, "c5")
m.addConstr(v1_cor1 - v3_cor1 + v4_cor1 <= 1, "c6")
m.addConstr(v2_cor1 - v3_cor1 + v4_cor1 <= 1, "c7")

# SEGUNDA RESTRIÇÃO > garantindo convexidade entre os vértices (SEGUNDA COR)
m.addConstr(v1_cor2 - v2_cor2 + v3_cor2 <= 1, "c8")
m.addConstr(v1_cor2 - v2_cor2 + v4_cor2 <= 1, "c9")
m.addConstr(v1_cor2 - v3_cor2 + v4_cor2 <= 1, "c10")
m.addConstr(v2_cor2 - v3_cor2 + v4_cor2 <= 1, "c11")

# Otimizando o problema
m.optimize()

for v in m.getObjective():
    print('%s %g' % (v.varName, v.x))

for v in m.getVars():
    print('%s %g' % (v.varName, v.x))

print('Obj: %g' % m.objVal)

teste = {'v1_cor1',
         'v1_cor2',
         'v2_cor1',
         'v2_cor2',
         'v3_cor1',
         'v3_cor2',
         'v4_cor1',
         'v4_cor2'}
