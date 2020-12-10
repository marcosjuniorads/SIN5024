def sep_ineq_convex_gen(v, e=0.01):
    mais = []
    menos = []
    indexIneq = []

    # inicializar arrays
    for i in range(0, len(v)):
        mais.append(0)
        menos.append(0)

    menos[0] = -0
    mais[0] = v[0]
    mais[1] = v[1]
    menos[1] = v[0] - v[1]

    for r in range(2, len(v)):
        p = argmax(mais[0: r])
        q = argmax(menos[1: r]) + 1
        mais[r] = maxCompare(v[r], menos[q] + v[r])
        menos[r] = mais[p] - v[r]

    # o maior valor do vetor mais diz se a inequacao ta violada
    n = len(v)

    if (maxarray(mais) > 1 + e):
        monta_inequacao(n - 1, '+', mais, menos, indexIneq)

    print(indexIneq)

    # buildConstraint(indexIneq, v)


def monta_inequacao(i, sinal, mais, menos, indexIneq):
    if (sinal == '+' and i >= 1):
        j = argmax(mais[0: i + 1])
        indexIneq.append(j)
        monta_inequacao(j - 1, '-', mais, menos, indexIneq)

    elif (i >= 2):
        j = argmax(menos[1: i + 1])

        if (menos[j + 1] > 0):
            indexIneq.append(j + 1)
            monta_inequacao(j, '+', mais, menos, indexIneq)


# def buildConstraint(indexIneq, v):

#     indexIneq = indexIneq[::-1]
#
#     expression = LinExpr(444)
#
#
#     r
#
#     #array que vai armazenar
#
#     v_pair = []
#
#     for i in range(0, len(v)):
#         v_pair.append(0)
#


# Add constraint: x + 2 y + 3 z <= 4
# m.addConstr(x + 2 * y + 3 * z <= 4, "c0")

#     sinal = '+'
#
#     for i in range(0, len(indexIneq)):
#
#         if (sinal == '+'):
#
#             index = indexIneq[i]
#
#
#
#         elif(sinal == '-'):

# https://www.gurobi.com/documentation/9.1/refman/py_lex.html
# https://www.gurobi.com/documentation/9.1/refman/py_lex2.html


# FUNCOES AUXILIARES
# =============================================================================

# ARGMAX -> retorna o indice do item com o maior valor
def argmax(array):
    return array.index(max(array))

# MAXCOMPARE -> maior valor na comparacao(os dois sao comparados como positivos)
def maxCompare(val1, val2):
    val1 = abs(val1)
    val2 = abs(val2)

    if (val1 > val2):
        return val1
    else:
        return val2

# MAXARRAY -> maior valor em um array
def maxarray(array):
    return max(array)



