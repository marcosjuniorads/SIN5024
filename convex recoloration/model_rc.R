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
restricao2    <- gerar_restricao2(n_vertices, n_cores, comb_vertices)

# GERANDO O MODELO ------
# inicialmente criei as matrizes na mão...
model <- list()

# função objetivo: Somatorio para cada vértice e cor (- cores iniciais dos
# vértices).
model$obj <- fun_objetivo

# PRIMEIRA RESTRIÇÃO. Escolher uma cor para cada vértice.
# primeiro exemplo, supondo 4 vertices
rs1 <- matrix(data = c(1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,
                           1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1),
                 nrow = 4,
                 ncol = 8)

# SEGUNDA RESTRIÇÃO. Garantir a convexidade entre eles.
# Segunda tentativa - matriz para a restrição de convexidade cor 1
# matriz esparsa onde -> j = col e i = lin
# acho que deu certo....
rs2_cor1 <- spMatrix(nrow = 16,
                  ncol = 8,
                  x = c(1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, 1, 1, -1,
                        1, 1, 1, -1, 1, 1, -1),

                  j = c(1, 3, 5, 1, 3, 5, 1, 5, 3, 5, 1, 3, 3, 5, 7, 3, 5, 7, 3,
                        7, 5, 7, 3, 5),

                  i = c(1, 1, 1, 2, 3, 4, 5, 5, 6, 6, 8, 8, 9, 9, 9, 10, 11,
                        12, 13, 13, 14, 14, 16, 16))

rs2_cor2 <- spMatrix(nrow = 16,
                  ncol = 8,
                  x = c(1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, 1, 1, -1,
                        1, 1, 1, -1, 1, 1, -1),
                  
                  j = c(2, 4, 6, 2, 4, 6, 2, 6, 4, 6, 2, 4, 4, 6, 8, 4, 6, 8, 4,
                        8, 6, 8, 4, 6),
                  
                  i = c(1, 1, 1, 2, 3, 4, 5, 5, 6, 6, 8, 8, 9, 9, 9, 10, 11,
                        12, 13, 13, 14, 14, 16, 16))

model$A     <- rbind(rs1, r2)
model$rhs   <- rep(1, nrow(model$A))
model$sense <- c(rep('=', 4), rep('<=', 64))

model$modelname   <- "convex_recoloration"
model$modelsense  <- "min"
model$vtype       <- "B"

# Optimize
res <- gurobi(model)
res$x
res$status
