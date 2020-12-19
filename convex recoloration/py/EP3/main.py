from functions_files import *
import os

def getInput(diretorio, file):
    # Atualizando o caminho do codigo
    path = diretorio + file

    # obtendo dados dos arquivos
    df = obter_variaveis(path)

    # obtendo a lista de variaveis e respectivos coeficientes para função
    # obj.
    lista_variaveis = df['nome_variavel']
    lista_coeficientes = df['coeff']
    
    modelDict = {}
    
    for i in range(0, len(lista_variaveis)):
        modelDict[lista_variaveis[i]] = lista_coeficientes[i]
        
    return modelDict


def solve(input):
    
    print("parei aqui")


def main():
    # path do arquivo
    diretorio = str('C:\\Users\\Matheus Ancelmo\\Documents\\Mestrado\\instancias\\')
    
    # obtendo a lista de arquivos
    files = os.listdir(diretorio)
    
    for file in files:
        
        input = getInput(diretorio, file)
        solve(input)    
    
main()

    
        
    
    
#     if path == 'C:\\Users\\Matheus Ancelmo\\Documents\\Mestrado\\instancias\\rand_10_2.txt':
#         print(path)
#         print(lista_variaveis)
#         print(lista_coeficientes)
    
    
