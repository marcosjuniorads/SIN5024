import gurobipy as gp
from gurobipy import GRB
from gurobipy.gurobipy import LinExpr, quicksum
import numpy as np

def adicionar_variaveis_modelo(model, lista_variaveis, name):
    return model.addVars(lista_variaveis, vtype=GRB.BINARY, name=name)


def criar_funcao_objetivo(model, lista_variaveis, lista_coeficientes):
    # inicializando a expressão com a primeira variável
    linear_expression = LinExpr(lista_coeficientes[0],
                                lista_variaveis.values()[0])

    for i in range(1, len(lista_variaveis)):
        linear_expression.add(lista_variaveis.values()[i],
                              lista_coeficientes[i])

    model.setObjective(linear_expression, GRB.MINIMIZE)
    return model
