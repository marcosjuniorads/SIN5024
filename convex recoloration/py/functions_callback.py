import gurobipy as gp
from gurobipy import GRB
from functions_model import *
from functions_files import *
from gurobipy.gurobipy import LinExpr, quicksum
import numpy as np
import pandas as pd
import itertools
from itertools import combinations as comb
from numpy.lib.index_tricks import index_exp

# ESSE PARAMETRO DEVE SER USADO QUANDO O PROGRAMA FOR USAR LAZY CONSTRAINT, ANTES DO M.OPTIMIZE()
m.setParam('LazyConstraints', 1, '')

# PARA LAZY CONSTRAINT, DESATIVAR OS CORTES DA R2
# PARA USERCUT, CHAMAR NORMALMENTE

# CHAMADA QUANDO USAR CALLBACK
m.optimize(callback)


# NAO SEI SE OS IMPORTS ESTAO CORRETOS PQ NAO CONSEGUI TESTAR ASSIM,
# ENTAO TEM QUE VER SE FUNCIONA


def colorSeparation(model):
    variaveis = model.getVars()

    cores = len(obter_lista_cores(path, duplicated_values=False))
    j = 0

    colunasXCores = []
    aux_colunasXCores = []

    for i in range(0, cores):

        j = i

        while j < len(variaveis):
            aux_colunasXCores.append(variaveis[j])
            j = j + cores

        colunasXCores.append(aux_colunasXCores)
        aux_colunasXCores = []

    return (colunasXCores)


def colorRelaxation(colunasXCores, model):
    arrayRetorno = []
    aux_arrayRetorno = []

    # Remover a restricao de integralidade das cores
    for i in range(0, len(colunasXCores)):
        for j in range(0, len(colunasXCores[i])):
            model.getVarByName(colunasXCores[i][j].VarName).VType = 'C'
            model.update()

            aux_arrayRetorno.append(
                model.getVarByName(colunasXCores[i][j].VarName))

        arrayRetorno.append(aux_arrayRetorno)
        aux_arrayRetorno = []

    return (arrayRetorno)


# CONSTROI AS INEQUACOES DE CORTE
def equationBuilder(index_inequacao, v, modelVars):
    index_inequacao.reverse()

    sinal = '+'
    expr = LinExpr()

    for i in range(0, len(index_inequacao)):

        if (sinal == '+'):
            var = modelVars[index_inequacao[i]]

            # adicionar variavel a expressao
            expr.add(var, 1)

            # alterar sinal
            sinal = '-'

        elif (sinal == '-'):
            var = modelVars[index_inequacao[i]]

            # adicionar variavel a expressao
            expr.add(var, -1)

            # alterar sinal
            sinal = '+'

    return (expr)


# ALGORITMO DE SEPARACAO
# Funcao que retorna o indice do item com o maior valor
def argmax(array):
    return array.index(max(array))


# Funcao que retorna o maior valor dentre dois numeros positivos
def get_maximum_number(val1, val2):
    if abs(val1) > abs(val2):
        return val1
    else:
        return val2


def monta_inequacao(i, sinal, mais, menos, index_inequacao):
    if sinal == '+' and i >= 1:
        j = argmax(mais[0: i + 1])
        index_inequacao.append(j)
        monta_inequacao(j - 1, '-', mais, menos, index_inequacao)

    elif i >= 2:
        j = argmax(menos[1: i + 1])

        if menos[j + 1] > 0:
            index_inequacao.append(j + 1)
            monta_inequacao(j, '+', mais, menos, index_inequacao)


def sep_ineq_convex_gen(vVars, modelVars, e=0.01):
    v = vVars

    # iniciando os vetores auxiliares
    mais = []
    menos = []
    index_inequacao = []

    # inicializar arrays
    for i in range(0, len(v)):
        mais.append(0)
        menos.append(0)

    menos[0] = -0
    mais[0] = v[0]
    mais[1] = v[1]
    menos[1] = v[0] - v[1]

    # percorrendo o vetor criado.
    for r in range(2, len(v)):
        p = argmax(mais[0: r])
        q = argmax(menos[1: r]) + 1
        mais[r] = get_maximum_number(v[r], menos[q] + v[r])
        menos[r] = mais[p] - v[r]

    # o maior valor do vetor mais diz se a inequacao ta violada
    n = len(v)

    if max(mais) > 1 + e:
        monta_inequacao(n - 1, '+', mais, menos, index_inequacao)

        corte = equationBuilder(index_inequacao, vVars, modelVars)

        return (corte)
    else:

        return ('--')


# FUNCTIONS_CALLBACK
def callback(model, where):
    # USERCUT
    if where == GRB.Callback.MIPNODE and model.cbGet(
            GRB.Callback.MIPNODE_STATUS) == GRB.OPTIMAL:

        # Selecionar variaveis que serao cortadas
        # remover a restricao de binario
        vArray = colorRelaxation(colorSeparation(model), model)

        cortes = []

        for i in range(0, len(vArray)):
            v = model.cbGetNodeRel(vArray[i])

            # chamar o algoritmo de separacao
            retornoSeparacao = sep_ineq_convex_gen(v)

            if (isinstance(retornoSeparacao, str) == False):
                model.cbCut(retornoSeparacao, GRB.LESS_EQUAL, 1)

    # LAZYCONSTRAINT
    if where == GRB.Callback.MIPSOL:
        # Selecionar variaveis que serao cortadas
        # remover a restricao de binario
        vArray = colorRelaxation(colorSeparation(model), model)

        cortes = []

        for i in range(0, len(vArray)):
            v = model.cbGetSolution(vArray[i])

            # chamar o algoritmo de separacao
            retornoSeparacao = sep_ineq_convex_gen(v, vArray[i])

            if (isinstance(retornoSeparacao, str) == False):
                model.cbLazy(retornoSeparacao, GRB.LESS_EQUAL, 1)
