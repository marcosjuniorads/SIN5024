# Função que retorna o indice do item com o maior valor
def argmax(array):
    return array.index(max(array))


# Função que retorna o maior valor dentre dois números positivos
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


def sep_ineq_convex_gen(v, e=0.01):
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

    return(index_inequacao)


def callback(model, where):
    print("breakdown")

    # USERCUT
    if where == GRB.Callback.MIPNODE and model.cbGet(
            GRB.Callback.MIPNODE_STATUS) == GRB.OPTIMAL:
        print("USERCUT DA GALERA")
        # x = model.cbGetNodeRel(model._vars)
        # model.cbSetSolution(model.getVars(), x)

    # LAZYCONSTRAINT
    if where == GRB.Callback.MIPSOL:
        print("LAZY CONSTRINT BOLADA")
