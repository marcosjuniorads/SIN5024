import gurobipy as gp
from gurobipy import GRB
from gurobipy.gurobipy import LinExpr

# Create a new model
m = gp.Model("mip1")

# Create the set of variables
lista_variaveis = ['x', 'y', 'z']
vertices = m.addVars(lista_variaveis, vtype=GRB.BINARY, name="lista_variaveis")

#  FO: Maximize the linear expression
#        x +   y + 2 z
expr = LinExpr([1], [vertices['x']])
expr.add(vertices['y'], 1)
expr.add(vertices['z'], 2)
m.setObjective(expr, GRB.MAXIMIZE)
# (outra maneira de passar o mesmo código acima, seria:
    # expr = LinExpr([1, 1, 2], [vertices['x'],
    #                            vertices['y'],
    #                            vertices['z']])

# Adding contraints
# Add constraint: x + 2 y + 3 z <= 4
expr = LinExpr([1], [vertices['x']])
expr.add(vertices['y'], 2)
expr.add(vertices['z'], 3)
m.addConstr(expr, "<=", 4)
# (outra maneira de passar o mesmo código acima, seria:
    #expr = LinExpr([1, 2, 3], [vertices['x'],
    #                           vertices['y'],
    #                           vertices['z']])

# Adding constraint: x + y >= 1
expr = LinExpr([1], [vertices['x']])
expr.add(vertices['y'], 1)
m.addConstr(expr, ">=", 1)
# (outra maneira de passar o mesmo código acima, seria:
    # expr = LinExpr([1, 1, 0], [vertices['x'],
    #                            vertices['y'],
    #                            vertices['z']])

# Optimize model
m.optimize()

# Print the result
for v in m.getVars():
    print('%s %g' % (v.varName, v.x))
print('Obj: %g' % m.objVal)
