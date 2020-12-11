import gurobipy as gp
from gurobipy import GRB
from gurobipy.gurobipy import LinExpr, quicksum


def adicionar_variaveis_modelo(model, lista_variaveis, name):
    return model.addVars(lista_variaveis, vtype=GRB.BINARY, name=name)


def criar_funcao_objetivo(model, lista_variaveis):
    return model.setObjective(quicksum(lista_variaveis), GRB.MINIMIZE)
