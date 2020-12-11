# supondo a entrada como:
# 4 vertices, 2 cores
# COR_1, COR_2, COR_2, COR_1

import gurobipy as gp
from gurobipy import GRB

# Criando o modelo
m = gp.Model("recoloration_convex")

# Adicionando as variáveis ao modelo
# lista_variaveis = ["v1_cor1", "v1_cor2", "v2_cor1", "v2_cor2", "v3_cor1", "v3_cor2", "v4_cor1", "v4_cor2"]
v1_cor1 = m.addVar(vtype=GRB.BINARY, name="v1_cor1")
v1_cor2 = m.addVar(vtype=GRB.BINARY, name="v1_cor2")
v2_cor1 = m.addVar(vtype=GRB.BINARY, name="v2_cor1")
v2_cor2 = m.addVar(vtype=GRB.BINARY, name="v2_cor2")
v3_cor1 = m.addVar(vtype=GRB.BINARY, name="v3_cor1")
v3_cor2 = m.addVar(vtype=GRB.BINARY, name="v3_cor2")
v4_cor1 = m.addVar(vtype=GRB.BINARY, name="v4_cor1")
v4_cor2 = m.addVar(vtype=GRB.BINARY, name="v4_cor2")

# Criando a funcao objetivo, que no caso busca minimizar os custos
# lista_coeficientes = [1, 1, 1, 1, 1, 1, 1, 1]
m.setObjective(v1_cor2 + v2_cor1 + v3_cor1 + v4_cor2, GRB.MINIMIZE)

# PRIMEIRA RESTRIÇÃO > garantindo que todos os vértices sejam pintados
# lista_variaveis = [1, 1, 1, 1, 1, 1, 1, 1]
# lista_coeficientes = [1, 1, 1, 1, 1, 1, 1, 1]
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

teste={'v1_cor1',
       'v1_cor2',
       'v2_cor1',
       'v2_cor2',
       'v3_cor1',
       'v3_cor2',
       'v4_cor1',
       'v4_cor2'}
