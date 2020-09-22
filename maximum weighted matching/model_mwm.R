# carregando as funções necessárias
source(paste0(getwd(), "/librarys.R"))
source(paste0(getwd(), "/maximum weighted matching/functions_mwm.R"))

# PROBLEMA:

# chamando funções para resolução do problema de otimização
nome_arq <- "instancia1.txt"

n_vertices   <- obter_numero_vertices(nome_arq)
n_arestas    <- obter_numero_arestas(nome_arq)
peso_arestas <- obter_dados_grafo(nome_arq)
lista_adjac  <- obter_lista_adjacencia(peso_arestas)

# apenas para facilitar visuaização / entendimento do problema
visualizar_grafo(peso_arestas)

# PROBLEMA: Dado um grafo não-dirigido G = (V, A) e uma função W:V -> R que
# associa um peso a cada aresta de G. encontrar um emparelhamento de peso máx.
# em G.

# Formalizando o problema, temos que:
# FUN SOMATÓRIO de (WVi * Xi), onde: W = peso das arestas e
# X = indicador se está no emparelhamento

# PARA FORÇAR O EMPARALHAMENTO, ESTABELECE-SE COMO RESTRIÇÃO QUE:
# (Lembrando que um grafo esta emparelhado apenas quando possui caminhos
# alternantes = só tem uma aresta incidindo sobre um vertíce.)
# st. SOMATÒRIO de (arestas no vertíce) Xa <= 1 - ou seja, apenas uma aresta
# está sendo selecionada para o emparelhamento.
#                                  Modelo binário, portanto X deve ser = 1 ou 0

# GERANDO O MODELO.
model <- list()

model$obj <- peso_arestas$peso

# criando uma matriz esparsa 
model$A   <- spMatrix(n_vertices,
                      n_arestas,
                      x = rep(1, 12),                            # automatizar
                      j = c(1, 2, 1, 3, 2, 4, 5, 3, 4, 6, 5, 6), # automatizar
                      i = c(1, 1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5)) # automatizar

model$rhs         <- rep(1, 5)
model$sense       <- rep('<=')
model$modelname   <- 'maximum_weighted_matching'
model$modelsense  <- 'max'
model$vtype       <- "B"

# Adding constraint: at most 6 servings of dairy this is the matrix part of the
# constraint
# B <- spMatrix(1, nCategories + nFoods,
#               i = rep(1,2),
#               j = (nCategories+c(8,9)),
#               x = rep(1,2))
# append B to A
# model$A           <- rbind(model$A,       B)
# extend row-related vectors
# model$constrnames <- c(model$constrnames, 'limit_dairy')
# model$rhs         <- c(model$rhs,         6)
# model$sense       <- c(model$sense,       '<')

# Optimize
res <- gurobi(model)
imprime_weighted_matching(res)
