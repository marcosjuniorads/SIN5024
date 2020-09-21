# carregando as funções necessárias
source(paste0(getwd(), "/librarys.R"))
source(paste0(getwd(), "/maximum weighted matching/functions.R"))

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
# associa um peso a cada aresta de G. encontrar um emparelhamento de peso máximo
# em G.

# Formalizando o problema, temos que:
# FUN SOMATÓRIO de (WVi * Xi), onde: W = peso das arestas e
# X = indicador se está no emparelhamento

# PARA FORÇAR O EMPARALHAMENTO, ESTABELECE-SE COMO RESTRIÇÃO QUE:
# (Lembrando que um grafo esta emparelhado apenas quando possui caminhos
# alternantes = só tem uma aresta incidindo sobre um vertíce.)
# st. SOMATÒRIO de (arestas no vertíce) Xa <= 1 - ou seja, apenas uma aresta
# está sendo selecionada para o emparelhamento.
#                                   Modelo binário, portanto X deve ser = 1 ou 0

# GERANDO O MODELO.
model <- list()

# F. Objetivo = W1 * X1 + W2 * X2 + W3 * X3 ...... Wi * X1, onde W = Peso Aresta
