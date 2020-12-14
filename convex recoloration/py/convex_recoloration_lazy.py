import gurobipy as gp
from gurobipy import GRB
from functions_callback import *
from functions_model import *
from functions_files import *
from gurobipy.gurobipy import LinExpr
import os

# path do arquivo
diretorio = str('E:\\SIN5024\\convex recoloration\\instancias\\')
diretorio_resultados = str('E:\\SIN5024\\convex recoloration\\py\\results_l\\')

# obtendo a lista de arquivos
files = os.listdir(diretorio)
path = ''

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

    # Otimizando com lazy constraint e callback
    # APESAR DO CÓDIGO, TIVEMOS PROBLEMAS AQUI E NÃO CONSEGUIMOS OBTER EVID.
    m.setParam('LazyConstraints', 1, '')
    m.optimize(callback)
