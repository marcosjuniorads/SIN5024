import gurobipy as gp
from gurobipy import GRB
from functions_files import *
from gurobipy.gurobipy import LinExpr, quicksum
import sys
import pandas as pd


def adicionar_variaveis_modelo(model, lista_variaveis, name):
    return model.addVars(lista_variaveis, vtype=GRB.BINARY, name=name)


def criar_funcao_objetivo(model, lista_variaveis, variables, lista_coef):
    # inicializando a expressão com a primeira variável
    linear_expression = LinExpr()
    for i in range(1, len(lista_variaveis)):
        linear_expression.add(variables.values()[i], lista_coef[i])
    model.setObjective(linear_expression, GRB.MINIMIZE)
    return model


def gerando_relatorio_otimizacao(diretorio_resultados, nome_arquivo, m,
                                 numero_vertices, numero_cores,
                                 lista_vertice_cor, path_model=False,
                                 lista_caminhos='',
                                 lista_cores=''
                                 ):
    # criando o arquivo
    f = open(diretorio_resultados + nome_arquivo, "w")

    # apenas redirecionando a saída (prints) para o rquivo e não console
    original_stdout = sys.stdout  # Save a reference to the original standard
    sys.stdout = f  # Change the standard output to the file we created.

    f.write("Iniciando o processamento do arquivo: " + nome_arquivo + '\n\n')

    # imprimindo os dados de entrada
    f.write('************* LENDO OS DADOS DE ENTRADA *************\n\n')
    f.write('Número de vértices informados: ' + str(numero_vertices) + '\n')
    f.write('Número de cores informadas: ' + str(numero_cores) + '\n')
    f.write('Número de cores REALMENTE DISTINTAS: ' +
            str(len(lista_vertice_cor['cor_atual'].unique())) + '\n')
    f.write('Lista de vértices e cores:\n' +
            lista_vertice_cor.to_string(index=False) + '\n\n\n')

    mes = '\nATENÇÃO !!!! O TOTAL DE CORES INFORMADAS NO CABEÇALHO É DISTINTO' \
          ' DO INFORMADO NA LISTA DE CORES DISPONIBILIZADA POR VÉRTICE. ' \
          'BUSCAMOS CONTORNAR A INCONSISTÊNCIA, VENDO APENAS A LISTA DE ' \
          'CORES POR VÉRTICE.\n\n'
    if numero_cores != len(lista_vertice_cor['cor_atual'].unique()): print(mes)

    if path_model:
        f.write('*** CRIANDO CAMINHOS COM COMBINAÇÃO DE TODOS VÉRTICES E ' +
                'CORES ****\n\n')
        df = pd.DataFrame(lista_caminhos)
        df = df[['Nome', 'Nome_vertices']]
        f.write('Combinação de TODOS OS caminhos e vértices possíveis:\n' +
                df.to_string(index=False) + '\n\n\n')

        f.write('*** HEURÍSTICA DESENVOLVIDA PARA ENCONTRAR CAMINHOS ' +
                'POSSÍVEIS ****\n\n')
        f.write('Lista de caminhos possíveis SIMPLIFICADOS POR HEURISTICA:\n' +
                str(encontrar_caminhos_validos(lista_caminhos, lista_cores)) +
                '\n\n\n')

    f.write('************* DETALHES PROCESSAMENTO REALIZADO *******\n\n')
    print(m.optimize())
    f.write('\n\n\n')

    f.write('************* SOLUÇÃO ENCONTRADA APÓS EXECUÇÃO *******\n\n')
    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))
    f.write('\n\n')

    f.write('******* EQUAÇÕES LINEARES UTILIZADAS NO MODELO ********\n\n')
    print(m.display())

    sys.stdout = original_stdout  # Reset the standard output to its original
    f.close()
