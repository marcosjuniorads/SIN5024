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

# GERANDO O MODELO ------ 
# inicialmente criei as matrizes na mão...
model <- list()

# função objetivo: Somatorio para cada vértice e cor (- cores iniciais dos
# vértices).
model$obj <- c(1, 0, 0, 1, 0, 1, 1, 0)
 
# PRIMEIRA RESTRIÇÃO. Escolher uma cor para cada vértice.
# primeiro exemplo, supondo 4 vertices
model$A <- matrix(data = c(1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,
                           1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1),
                 nrow = 4,
                 ncol = 8)

# SEGUNDA RESTRIÇÃO. Garantir a convexidade entre eles.
# Segunda tentativa - matriz para a restrição de convexidade cor 1
# matriz esparsa onde -> j = col e i = lin
# acho que deu certo....
cor_1 <- spMatrix(nrow = 32,
                  ncol = 8,
                  x = c(1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, 1,
                        -1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, 1, -1, 1, 1, 1,
                        1, -1, -1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1),

                  j = c(2, 4, 6, 2, 4, 6, 2, 6, 2, 4, 4, 6,
                        2, 4, 8, 2, 4, 8, 2, 8, 2, 4, 4, 8,
                        2, 6, 8, 2, 6, 8, 2, 8, 2, 6, 6, 8,
                        4, 6, 8, 4, 6, 8, 4, 8, 4, 6, 6, 8),

                  i = c(1, 1, 1, 2, 3, 4, 6, 6, 7, 7, 8, 8,
                        9, 9, 9, 10, 11, 12, 14, 14, 15, 15, 16, 16,
                        17, 17, 17, 18, 19, 20, 22, 22, 23, 23, 24, 24,
                        25, 25, 25, 26, 27, 28, 30, 30, 31, 31, 32, 32)
                  )

cor_2 <- spMatrix(nrow = 32,
                  ncol = 8,
                  x = c(1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, 1,
                        -1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, 1, -1, 1, 1, 1,
                        1, -1, -1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1),

                  j = c(1, 3, 5, 1, 3, 5, 1, 5, 1, 3, 3, 5,
                        1, 3, 7, 1, 3, 7, 1, 7, 1, 3, 3, 7,
                        1, 5, 7, 1, 5, 7, 1, 7, 1, 5, 5, 7,
                        3, 5, 7, 3, 5, 7, 3, 7, 3, 5, 5, 7),

                  i = c(1, 1, 1, 2, 3, 4, 6, 6, 7, 7, 8, 8,
                        9, 9, 9, 10, 11, 12, 14, 14, 15, 15, 16, 16,
                        17, 17, 17, 18, 19, 20, 22, 22, 23, 23, 24, 24,
                        25, 25, 25, 26, 27, 28, 30, 30, 31, 31, 32, 32)
                  )


model$A     <- rbind(model$A, rbind(cor_1, cor_2))
model$rhs   <- rep(1, nrow(model$A))
model$sense <- c(rep('=', 4), rep('<=', 64))

model$modelname   <- "convex_recoloration"
model$modelsense  <- "min"
model$vtype       <- "B"

# Optimize
res <- gurobi(model)
res$x
res$status
