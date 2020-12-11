import gurobipy as gp
from gurobipy import GRB
from gurobipy.gurobipy import LinExpr

def adicionar_variaveis_modelo(model, lista_variaveis, name):
    return model.addVars(lista_variaveis, vtype=GRB.BINARY, name=name)


def criar_funcao_objetivo(model, lista_coeficientes, lista_variaveis):
    # inicializando a expressão com a primeira casela do vetor
    expr = LinExpr(lista_coeficientes[0], lista_variaveis[0])

    # iterando sobre as listas para criar a expressão linear
    for i in range(1, len(lista_variaveis)):
        expr.add(lista_variaveis[i], lista_coeficientes[i])

    # definindo a função objetivo
    return model.setObjective(expr, GRB.MAXIMIZE)
