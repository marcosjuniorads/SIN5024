import gurobipy as gp
from gurobipy import GRB
from functions_model import *
from functions_files import *
import os

def heuristica(lista_caminhos, variables):
    
    #puxar isso dinamico depois
    TAMANHO_ARRAY_ORIGINAL = 4
    
    copia_iteravel = lista_caminhos.get("Nome_vertices")
    caminhos_possiveis = []
    caminho = []
    L = 0
    
    v_adicionados = []
    
    while len(copia_iteravel) > 0:
        
        #se o novo item cabe no caminho
        if len(copia_iteravel[0]) + L <= TAMANHO_ARRAY_ORIGINAL and copia_iteravel[len(copia_iteravel) - 1] not in v_adicionados:
        
            aux = copia_iteravel[0]
            L = L + len(copia_iteravel[0])
            caminho.append(aux)        
            copia_iteravel.pop(0)
            
            for i in range(0, len(aux)):
                v_adicionados.append(aux[i])
        else:
            
            caminhos_possiveis.append(caminho)
            caminho = []
            L = 0

    
    return caminhos_possiveis


















def solve(model, lista_caminhos, variables):
    
    caminhos_possiveis = heuristica(lista_caminhos, variables)
    
    print("teste")
    
    

# path do arquivo
#diretorio = str('E:\\SIN5024\\convex recoloration\\instancias\\')
#diretorio_resultados = str('E:\\SIN5024\\convex recoloration\\py\\results\\')

diretorio = str('C:\\Users\\Matheus Ancelmo\\Documents\\Mestrado\\instancias\\')
diretorio_resultados = str('C:\\Users\\Matheus Ancelmo\\Documents\\Mestrado\\results\\')

# obtendo a lista de arquivos
# files = os.listdir(diretorio)

file = 'exemplo_simples.txt'

# Atualizando o caminho do cÃ³digo
path = diretorio + file

# Criando o modelo
m = gp.Model("recoloration_convex")

# obtendo dados dos arquivos
lista_caminhos = obter_caminho_possiveis_porcor(path)
lista_cores_vertices = obter_lista_cores(path, True)

# buscando os dados das coeficientes das respectivas variÃ¡veis
lista_caminhos = adicionar_coeficientes_caminho(lista_cores_vertices,
                                                lista_caminhos)


# CRIANDO AS VARIÃ�VEIS DO MODELO ------------------------------------------
# variables = adicionar_variaveis_modelo(m, lista_variaveis,
# "modelo_var")
variables = m.addVars(lista_caminhos["Nome"], vtype=GRB.BINARY, name="var")

# ADICIONANDO EXPRESSÃƒO LINEAR DA FUNÃ‡ÃƒO OBJETIVO -------------------------
# inicializando a expressÃ£o com a primeira variÃ¡vel
linear_expression = LinExpr()
for i in range(0, len(lista_caminhos)):
    linear_expression.add(variables.values()[i],
                          lista_caminhos["coeficientes"][i])
    m.setObjective(linear_expression, GRB.MINIMIZE)
    
#======================================================================
#depois que terminar de montar o modelo
#chamar o metodo solve ao inves de fazer model.solve()
solve(m, lista_caminhos, variables)

