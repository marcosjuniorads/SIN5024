# carregando as funções e bibliotecas necessárias
source(paste0(getwd(), "/librarys.R"), encoding = "UTF-8")
source(paste0(getwd(), "/convex recoloration/functions_rc.R"),
       encoding = "UTF-8")

# obtendo lista de arquivos de instâncias que serão processadas
files <- list.files(path = "./convex recoloration/instancias", full.names = T)

# lendo os dados dos arquivos de entrada.
nome_arq <- "rand_50_10.txt"
start <- Sys.time () # começando a contabilizar, a partir daqui, o tempo

# Obtendo os dados necessários para input no solver.
n_vertices    <- obter_numero_vertices(nome_arq)
n_cores       <- obter_numero_cores(nome_arq)
cor_vertices  <- obter_lista_cores(nome_arq)
comb_vertices <- obter_combinacao_vertices(nome_arq)
fun_objetivo  <- obter_funcao_objetivo(n_vertices, n_cores, cor_vertices)
restricao1    <- gerar_restricao1(n_vertices, n_cores, fun_objetivo)
restricao2    <- gerar_restricao2(n_vertices, n_cores, comb_vertices, fun_objetivo)

# variável que armazenará o output do GUROBI que será impresso no relatório
stdout <- vector('character')
con    <- textConnection('stdout', 'wr', local = TRUE)
sink(con)

# GERANDO O MODELO ------
model <- list() # iniciando o modelo do GUROBI

# passando a função objetivo
model$obj <- fun_objetivo

# passando as restrições
model$A     <- rbind(restricao1, restricao2)
model$rhs   <- rep(1, nrow(model$A))
model$sense <- c(rep('=', nrow(restricao1)), rep('<=', nrow(restricao2)))

# passando o nome do modelo, tipo binário e minimização
model$modelname   <- "convex_recoloration"
model$modelsense  <- "min"
model$vtype       <- "B"

# Otimizando - encontrando as soluções
res <- gurobi(model)
res$x
res$status

# coletando o output gerado pelo gurobi e fechando conexão com o console output
sink()
close(con)

# salvando os resultados em relatório que será entregue.
gerando_relatorio(nome_arq, n_vertices, n_cores, cor_vertices, fun_objetivo,
                  res, start, stdout)
