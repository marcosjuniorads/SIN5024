from functions_files import *
import os

# path do arquivo
diretorio = str('C:\\Users\\Matheus Ancelmo\\Documents\\Mestrado\\instancias\\')

# obtendo a lista de arquivos
files = os.listdir(diretorio)

for file in files:
    # Atualizando o caminho do código
    path = diretorio + file

    # obtendo dados dos arquivos
    df = obter_variaveis(path)

    # obtendo a lista de variaveis e respectivos coeficientes para função
    # obj.
    lista_variaveis = df['nome_variavel']
    lista_coeficientes = df['coeff']
    
    print(path)
    print(lista_variaveis)
    print(lista_coeficientes)
