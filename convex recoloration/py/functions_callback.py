import gurobipy as gp
from gurobipy import GRB
from functions_model import *
from functions_files import *
from gurobipy.gurobipy import LinExpr, quicksum

#testegit

def color_separation(model):
    variaveis = model.getVars()
    cores = len(obter_lista_cores(path, duplicated_values=False))
    j = 0

    colunas_cores = []
    aux_colunas_cores = []

    for i in range(0, cores):
        j = i
        while j < len(variaveis):
            aux_colunas_cores.append(variaveis[j])
            j = j + cores

        colunas_cores.append(aux_colunas_cores)
        aux_colunas_cores = []

    return colunas_cores


def color_relaxation(colunas_cores, model):
    array_retorno = []
    aux_array_retorno = []

    # Remover a restricao de integralidade das cores
    for i in range(0, len(colunas_cores)):
        for j in range(0, len(colunas_cores[i])):
            model.getVarByName(colunas_cores[i][j].VarName).VType = 'C'
            model.update()

            aux_array_retorno.append(
                model.getVarByName(colunas_cores[i][j].VarName))

        array_retorno.append(aux_array_retorno)
        aux_array_retorno = []

    return array_retorno


# CONSTROI AS INEQUACOES DE CORTE
def equationBuilder(index_inequacao, model_vars):
    index_inequacao.reverse()
    sinal = '+'
    expr = LinExpr()

    for i in range(0, len(index_inequacao)):
        if sinal == '+':
            var = model_vars[index_inequacao[i]]
            # adicionar variavel a expressao
            expr.add(var, 1)
            # alterar sinal
            sinal = '-'
        elif sinal == '-':
            var = model_vars[index_inequacao[i]]
            # adicionar variavel a expressao
            expr.add(var, -1)
            # alterar sinal
            sinal = '+'
    return expr


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


def sep_ineq_convex_gen(v_vars, model_vars, e=0.01):
    v = v_vars

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
        corte = equationBuilder(index_inequacao, v_vars, model_vars)

        return corte
    else:
        return '--'


# FUNCTIONS_CALLBACK
def callback(model, where):
    # USERCUT
    if where == GRB.Callback.MIPNODE and model.cbGet(
            GRB.Callback.MIPNODE_STATUS) == GRB.OPTIMAL:

        # Selecionar variaveis que serao cortadas
        # remover a restricao de binario
        v_array = color_relaxation(color_separation(model), model)

        cortes = []

        for i in range(0, len(v_array)):
            v = model.cbGetNodeRel(v_array[i])

            # chamar o algoritmo de separacao
            retorno_separacao = sep_ineq_convex_gen(v)

            if isinstance(retorno_separacao, str) == False:
                model.cbCut(retorno_separacao, GRB.LESS_EQUAL, 1)

    # LAZYCONSTRAINT
    if where == GRB.Callback.MIPSOL:
        # Selecionar variaveis que serao cortadas
        # remover a restricao de binario
        v_array = color_relaxation(color_separation(model), model)

        cortes = []

        for i in range(0, len(v_array)):
            v = model.cbGetSolution(v_array[i])

            # chamar o algoritmo de separacao
            retorno_separacao = sep_ineq_convex_gen(v, v_array[i])

            if isinstance(retorno_separacao, str) == False:
                model.cbLazy(retorno_separacao, GRB.LESS_EQUAL, 1)
