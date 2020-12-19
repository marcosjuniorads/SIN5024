import gurobipy as gp
from gurobipy import GRB
from functions_callback import *
from functions_model import *
from functions_files import *
from gurobipy.gurobipy import LinExpr, quicksum
import os

# path do arquivo
diretorio = str('E:\\SIN5024\\convex recoloration\\instancias\\')
diretorio_resultados = str('E:\\SIN5024\\convex recoloration\\py\\results_u\\')

# obtendo a lista de arquivos
files = os.listdir(diretorio)
path = ''


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



for file in files:
    # Atualizando o caminho do código
    path = diretorio + file

    # Criando o modelo
    m = gp.Model("recoloration_convex")

    # obtendo dados dos arquivos
    df = obter_variaveis(path)

    # obtendo a lista de variaveis e respectivos coeficientes para função
    # obj.
    lista_variaveis = df['nome_variavel']
    lista_coeficientes = df['coeff']

    # CRIANDO AS VARIÁVEIS DO MODELO ------------------------------------------
    # variables = adicionar_variaveis_modelo(m, lista_variaveis,
    # "modelo_var")
    variables = m.addVars(lista_variaveis, vtype=GRB.BINARY, name="variables")

    # ADICIONANDO EXPRESSÃO LINEAR DA FUNÇÃO OBJETIVO -------------------------
    # inicializando a expressão com a primeira variável
    linear_expression = LinExpr()
    for i in range(1, len(lista_variaveis)):
        linear_expression.add(variables.values()[i], lista_coeficientes[i])
        m.setObjective(linear_expression, GRB.MINIMIZE)

    # ADICIONANDO EXPRESSÃO LINEAR DA PRIMEIRA RESTRIÇÃO ------------------
    # Garantindo que todos os vértices sejam pintados.
    for numero_vertice in map(int, obter_lista_vertices(path)):
        # Abaixo, obtendo indices das variáveis do vertice N, que devem ser
        # somados em uma restrição linear para garantir que assumam
        # apenas uma
        # cor. Nesse caso, itero por cada vertice X de cor 'qualquer', para
        # posteriomente somar todos quando construo a restrição.
        lista_temp = [r[0] for r in
                     [i.lower().split('_') for i in lista_variaveis]]
        indices = [n for n, l in enumerate(lista_temp) if
                       l == ('vertice' + str(numero_vertice))]

        # Inicializando o objeto que irá armazenar a expressão linear.
        linear_expression = LinExpr()

        # iterando sobre os indices encontrados (anteriormente) e adicionando na
        # expressão linear que irá definir a primeira restrição. Coeficiente
        # deafult é +1, esse não será alterado.
        for i in indices:
            linear_expression.add(variables.values()[i], 1)

        # adicionando constraint para o respectivo value
        m.addConstr(linear_expression, "==", 1)

    # ADICIONANDO EXPRESSÃO LINEAR DA SEGUNDA RESTRIÇÃO -----------------------
    # garantindo convexidade entre os vértices

    # buscando o total de cores - sem repetição - existentes.
    cores = [int(i) for i in obter_lista_cores(path, duplicated_values=False)]

    # iterando, em cada cor, para criar as expressões lineares de restrição
    v_combinations = []
    for cor_i in cores:
        # encontrado todas as combinações entre vértices possíveis, de 3 em 3
        v_combinations = v_combinations + list(itertools.combinations(
            [k for k in lista_variaveis if 'cor' + str(cor_i) in k], 3)
        )

        # iterando sobre todas as combinações de cores e criando as expressões
        for com_i in v_combinations:
            # Inicializando o objeto que irá armazenar a expressão linear.
            linear_expression = LinExpr()

            # Ok, vou tentar fazer o possível para explicar um pouco do código
            # abaixo. Preciso construir uma equação que tenha o segunte formato:
            # Vx - Vy + Vw -> o que irá garantir a convexidade das cores.
            # Isso por si só explica os coeficientes finais do código (1,
            # - 1 e 1)
            # As instruções anteriores são para que eu consiga iterar por cada
            # combinação da respectiva cor (representado por com_i) e
            # encontre qual
            # é o respetivo indice dessa variável no GUROBI. Por esse motivo eu
            # busco o indice no vetor de referência e uso esse índice para
            # acessar
            # a respectiva variável dentro do Gurobi. De qualquer modo, um
            # refactoring não ia mal :).
            linear_expression.add(variables.values()[
                                      [i for i, s in enumerate(lista_variaveis)
                                       if com_i[0] in s][0]], 1)
            linear_expression.add(variables.values()[
                                      [i for i, s in enumerate(lista_variaveis)
                                       if com_i[1] in s][0]], -1)
            linear_expression.add(variables.values()[
                                      [i for i, s in enumerate(lista_variaveis)
                                       if com_i[2] in s][0]], 1)

            m.addConstr(linear_expression, "<=", 1)

    # OTIMIZANDO com USER CUT
    # APESAR DO CÓDIGO, TIVEMOS PROBLEMAS AQUI E NÃO CONSEGUIMOS OBTER EVID.
    m.optimize(callback)

