import gurobipy as gp
from gurobipy import GRB
from functions_model import *
from functions_files import *
import numpy as np

# path do arquivo
filename = '\exemplo_simples.txt'
path = 'E:\SIN5024\convex recoloration\instancias' + filename

# Criando o modelo
m = gp.Model("recoloration_convex")

# obtendo dados dos arquivos
df = obter_variaveis(path)

# obtendo a lista de variaveis e respectivos coeficientes para função objetivo
lista_variaveis = df['nome_variavel']
lista_coeficientes = df['coeff']

# CRIANDO AS VARIÁVEIS DO MODELO ----------------------------------------------
variables = adicionar_variaveis_modelo(model=m,
                                       lista_variaveis=lista_variaveis,
                                       name="variaveis_modelo")

# ADICIONANDO EXPRESSÃO LINEAR DA FUNÇÃO OBJETIVO -----------------------------
linear_expression = LinExpr()
for i in range(1, len(lista_variaveis)):
    linear_expression.add(variables.values()[i], lista_coeficientes[i])
m.setObjective(linear_expression, GRB.MINIMIZE)

# ADICIONANDO EXPRESSÃO LINEAR DA PRIMEIRA RESTRIÇÃO --------------------------
# Garantindo que todos os vértices sejam pintados.

for numero_vertice in map(int, obter_lista_vertices(path)):
    # Abaixo, obtendo indices das variáveis do vertice N, que devem ser somados
    # em uma restrição linear para garantir que assumam apenas uma cor.
    # Nesse caso, itero por cada vertice X de cor 'qualquer', para
    # posteriomente somar todos quando construo a restrição.
    indices = [n for n, l in enumerate(lista_variaveis) if
               l.startswith('vertice' + str(numero_vertice))]

    # Inicializando o objeto que irá armazenar a expressão linear.
    linear_expression = LinExpr()

    # iterando sobre os indices encontrados (anteriormente) e adicionando na
    # expressão linear que irá definir a primeira restrição. Coeficiente
    # deafult é +1, esse não será alterado.
    for i in indices:
        linear_expression.add(variables.values()[i], 1)

    # adicionando constraint para o respectivo value
    m.addConstr(linear_expression, "==", 1)

# ADICIONANDO EXPRESSÃO LINEAR DA SEGUNDA RESTRIÇÃO ---------------------------
# garantindo convexidade entre os vértices

# buscando o total de cores - sem repetição - existentes.
cores = [int(i) for i in obter_lista_cores(path, duplicated_values=False)]

# iterando, em cada cor, para criar as expressões lineares de restrição
for cor_i in cores:
    # encontrado todas as combinações entre vértices possíveis, de 3 em 3
    v_combinations = list(itertools.combinations([k for k in lista_variaveis if
                                                  'cor'+str(1) in k], 3))

    # iterando sobre todas as combinações de cores e criando as expressões
    for com_i in v_combinations:
        # Inicializando o objeto que irá armazenar a expressão linear.
        linear_expression = LinExpr()

        # Ok, vou tentar fazer o possível para explicar um pouco do código
        # abaixo. Preciso construir uma equação que tenha o segunte formato:
        # Vx - Vy + Vw -> o que irá garantir a convexidade das cores.
        # Isso por si só explica os coeficientes finais do código (1, - 1 e 1)
        # As instruções anteriores são para que eu consiga iterar por cada
        # combinação da respectiva cor (representado por com_i) e encontre qual
        # é o respetivo indice dessa variável no GUROBI. Por esse motivo eu
        # busco o indice no vetor de referência e uso esse índice para acessar
        # a respectiva variável dentro do Gurobi. De qualquer modo, um
        # refactoring não ia mal :).
        linear_expression.add(variables.values()[[i for i, s in enumerate(lista_variaveis) if com_i[0] in s][0]], 1)
        linear_expression.add(variables.values()[[i for i, s in enumerate(lista_variaveis) if com_i[1] in s][0]], -1)
        linear_expression.add(variables.values()[[i for i, s in enumerate(lista_variaveis) if com_i[2] in s][0]], 1)

        m.addConstr(linear_expression, "<=", 1)

# Otimizando o problema
m.optimize()

for v in m.getVars():
    print('%s %g' % (v.varName, v.x))

