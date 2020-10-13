# carregando as funções necessárias
source(paste0(getwd(), "/librarys.R"), encoding = "UTF-8")
source(paste0(getwd(), "/maximum weighted matching/functions_mwm.R"),
       encoding = "UTF-8")

# chamando funções para resolução do problema de otimização
nome_arq <- "instancia1.txt"

n_vertices   <- obter_numero_vertices(nome_arq)
n_arestas    <- obter_numero_arestas(nome_arq)
peso_arestas <- obter_dados_grafo(nome_arq)

# apenas para facilitar visuaização / entendimento do problema
visualizar_grafo(peso_arestas)

# criando a matriz de restrição para resolução do problema.
matriz_rest  <- criar_matriz_restricao(peso_arestas, n_vertices, n_arestas)

# PROBLEMA:
# Dado um grafo não-dirigido G = (V, A) e uma função W:V -> R que associa um
# peso a cada aresta de G. encontrar um emparelhamento de peso máximo em G.

# Formalizando o problema, temos que:
# FUN SOMATÓRIO de (WVi * Xi), onde: 
#                W = peso das arestas e X = indicador se está no emparelhamento

# PARA FORÇAR O EMPARALHAMENTO, ESTABELECE-SE COMO RESTRIÇÃO QUE:
# (Lembrando que um grafo esta emparelhado apenas quando possui caminhos
# alternantes = só tem uma aresta incidindo sobre um vértice.)
# st. SOMATÒRIO de (arestas no vertíce) Xa <= 1 - ou seja, apenas uma aresta
# está sendo selecionada para o emparelhamento.
#                                  Modelo binário, portanto X deve ser = 1 ou 0

# GERANDO O MODELO.
model <- list()

# função objetivo, contendo o peso de cada aresta que deve ser maximixado.
model$obj <- peso_arestas$p

# criando uma matriz esparsa a partir da matriz de restrição criada anteriormen.
model$A   <- Matrix(matriz_rest, sparse = TRUE)

model$rhs         <- rep(1, n_vertices)
model$sense       <- rep('<=')
model$modelname   <- 'maximum_weighted_matching'
model$modelsense  <- 'max'
model$vtype       <- "B"

# Optimize
res <- gurobi(model)
imprime_weighted_matching(res)
