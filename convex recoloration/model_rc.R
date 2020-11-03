# carregando as funções necessárias
source(paste0(getwd(), "/librarys.R"), encoding = "UTF-8")
source(paste0(getwd(), "/convex recoloration/functions_rc.R"),
       encoding = "UTF-8")

# lendo os dados dos arquivos de entrada - lista com cores para os vértices.
nome_arq <- "exemplo_simples.txt"

# lendo os arquivos e obtendo os dados necessários para input no solver.
n_vertices    <- obter_numero_vertices(nome_arq)
n_cores       <- obter_numero_cores(nome_arq)
cor_vertices  <- obter_lista_cores(nome_arq)
comb_vertices <- obter_combinacao_vertices(nome_arq)
fun_objetivo  <- obter_funcao_objetivo(n_vertices, n_cores, cor_vertices)
restricao1    <- gerar_restricao1(n_vertices, n_cores, fun_objetivo)
restricao2    <- gerar_restricao2(n_vertices, n_cores, comb_vertices, fun_objetivo)

# GERANDO O MODELO ------
# inicialmente criei as matrizes na mão...
model <- list()

# função objetivo
model$obj <- fun_objetivo

# combinando as restrições
model$A     <- rbind(restricao1, restricao2)
model$rhs   <- rep(1, nrow(model$A))
model$sense <- c(rep('=', nrow(restricao1)), rep('<=', nrow(restricao2)))

model$modelname   <- "convex_recoloration"
model$modelsense  <- "min"
model$vtype       <- "B"

# Optimize
res <- gurobi(model)
res$x
res$status
