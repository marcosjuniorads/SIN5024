import gurobipy as gp
from gurobipy import GRB
from functions_model import *
from functions_files import *
import os


#GERADOR DE COLUNAS ==========================================================================================

def adicionar_coluna(caminho):
    print("parei aqui")
#FUNCOES DA HEURISTICA =======================================================================================

#verifica se nenhum elemento do comparavel se repete na base
def check_repetido(base, comparavel, lista_caminhos):
    
    retorno = False
    
    for i in range(0, len(base)):
        
        aux = base[i]
        
        for j in range(0, len(comparavel)):
            
            if comparavel[j] in base or comparavel[j][0:8] in aux:
                
                retorno = True
    
    return retorno
      

def heuristica(lista_caminhos, variables, lista_cores):

    #puxar isso dinamico depois
    TAMANHO_ARRAY_ORIGINAL = len(lista_cores)
    
    #copia_iteravel = lista_caminhos.get('Nome_vertices')
    copia_iteravel = [['vertice1_cor1', 'vertice2_cor1'], 
                      ['vertice1_cor1', 'vertice2_cor1', 'vertice3_cor1'], 
                      ['vertice1_cor1', 'vertice2_cor1', 'vertice3_cor1', 'vertice4_cor1'], 
                      ['vertice2_cor1', 'vertice3_cor1'], 
                      ['vertice2_cor1', 'vertice3_cor1', 'vertice4_cor1'], 
                      ['vertice3_cor1', 'vertice4_cor1'], 
                      ['vertice1_cor2', 'vertice2_cor2'], 
                      ['vertice1_cor2', 'vertice2_cor2', 'vertice3_cor2'], 
                      ['vertice1_cor2', 'vertice2_cor2', 'vertice3_cor2', 'vertice4_cor2'], 
                      ['vertice2_cor2', 'vertice3_cor2'], 
                      ['vertice2_cor2', 'vertice3_cor2', 'vertice4_cor2'], 
                      ['vertice3_cor2', 'vertice4_cor2'],
                      ['vertice1_cor1'],
                      ['vertice2_cor1'],
                      ['vertice3_cor1'],
                      ['vertice4_cor1'],
                      ['vertice1_cor2'],
                      ['vertice2_cor2'],
                      ['vertice3_cor2'],
                      ['vertice4_cor2']]
    
    caminhos_possiveis = []
    caminho = []
    L = 0
    
    v_adicionados = []

    for i in range(0, len(copia_iteravel)):

        aux = copia_iteravel[0]
        caminho = []
        caminho.append(aux)
        acumulador_contagem = copia_iteravel[0]

        #verificar se o caminho e apto a comecar uma sequencia
        if 'vertice1' in aux[0]:

            v_adicionados = v_adicionados + aux
            copia_iteravel.pop(0)

            for j in range(0, len(copia_iteravel)):

                #verificar se nao foi adicionado ainda
                if check_repetido(aux, copia_iteravel[j], lista_caminhos) == False:
                
                    #procurar um caminho que se combine com aux
                    if len(aux) + len(copia_iteravel[j]) <= TAMANHO_ARRAY_ORIGINAL:
                        caminho.append(copia_iteravel[j])
                        acumulador_contagem = acumulador_contagem + copia_iteravel[j]
                        
                        if len(acumulador_contagem) == TAMANHO_ARRAY_ORIGINAL:
                            
                            caminhos_possiveis.append(caminho)
                            acumulador_contagem = aux 
                            caminho = []
                            caminho.append(aux)
                    
                    if j == len(copia_iteravel) - 1 and len(aux) == TAMANHO_ARRAY_ORIGINAL:
                        
                        caminhos_possiveis.append(caminho)
                        acumulador_contagem = aux 
                        caminho = []
                        caminho.append(aux)
        else:
            copia_iteravel.pop(0)       
       

    return caminhos_possiveis

# FUNCOES RESOLUCAO =========================================================================================

def solve(model, lista_caminhos, variables, lista_cores):
    
    caminhos_possiveis = heuristica(lista_caminhos, variables, lista_cores)
    
    #pra cada caminho possivel, achar uma coluna
    for i in range(0, len(caminhos_possiveis)):
        coluna = adicionar_coluna(caminhos_possiveis[i])
    
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
solve(m, lista_caminhos, variables, lista_cores_vertices)

