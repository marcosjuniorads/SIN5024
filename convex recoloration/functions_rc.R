# Formato dos arquivos de entrada:
# num_vertices
# num_cores
# sequencia de cores

obter_numero_vertices <- function(nome_arquivo) {
  path <- paste0(getwd(), "/convex recoloration/instancias/", nome_arquivo)
  data <- read.delim(path, header = FALSE, comment.char = "#")

  # lendo a primeira linha
  vertices <- as.character(data[1, ])
  # separando a string pelo espaço e obtendo só o número de vértices
  vertices <- strsplit(vertices, " ")[[1]][1]

  return(vertices)
}

obter_numero_cores <- function(nome_arquivo) {
  path <- paste0(getwd(), "/convex recoloration/instancias/", nome_arquivo)
  data <- read.delim(path, header = FALSE, comment.char = "#")

  # lendo a primeira linha
  cores <- as.character(data[1, ])
  # separando a string pelo espaço e obtendo só o número de cores.
  cores <- strsplit(cores, " ")[[1]][2]

  return(cores)
}

obter_lista_cores <- function(nome_arquivo) {
  path <- paste0(getwd(), "/convex recoloration/instancias/", nome_arquivo)
  data <- read.delim(path, header = FALSE, comment.char = "#")

  # lendo a primeira linha
  vetor_cores <- as.character(data[2:nrow(data), ])
  return(vetor_cores)
}

obter_combinacao_vertices <- function(nome_arquivo) {
  n_vertices <- obter_numero_vertices(nome_arquivo)
  return(combn(c(1:n_vertices), 3))
}

obter_funcao_objetivo <- function(numero_vertices, numero_cores, lista_cor) {

  # fazendo eventuais conversões para o formato correto, caso necessário
  numero_vertices <- as.numeric(numero_vertices)
  numero_cores <- as.numeric(numero_cores)

  # obtendo o total de combinações.
  vetor_fo <- rep(1, numero_vertices * numero_cores)

  # apenas gerando nomes para cada casela do vetor.
  names_vetor <- expand.grid(paste0("V", rep(1:numero_vertices)),
                             unique(cor_vertices)) %>% arrange(Var1)
  names_vetor <- paste(names_vetor$Var1, names_vetor$Var2, sep = "_")

  # nomeando o vetor
  names(vetor_fo) <- names_vetor

  # preenchendo o vetor com 0 para as caselas que contém a mesma cor do vertice
  for (vertice in 1:numero_vertices) {
    name <- paste0("V", vertice, "_", lista_cor[vertice])
    vetor_fo[[name]] <- 0
  }

  return(vetor_fo)
}


gerar_restricao1 <- function(n_vertices, n_cores, fun_objetivo) {
  # garantindo que todos os parâmetros estejam no formato correto
  n_vertices <- as.integer(n_vertices)
  n_cores <- as.integer(n_cores)

  # criando a matriz e preenchendo com 0
  r1 <- matrix(data = 0,
               ncol = n_cores * n_vertices,
               nrow = n_vertices,
               dimnames = list(NULL, names(fun_objetivo)))

  inicio <- 1
  # preenchenco a matriz com 1.
  for (vertice in 1:n_vertices) {
    for (cor in 1:n_cores) {
      vertice_i = paste0("V", vertice, "_", cor)
      r1[inicio, vertice_i] <- 1
    }
    inicio <- inicio + 1
  }

  return(r1)
}

gerar_restricao2 <- function(n_vertices, n_cores, matriz_combin, fun_objetivo) {
  # garantindo que todos os parâmetros estejam no formato correto
  n_vertices <- as.integer(n_vertices)
  n_cores <- as.integer(n_cores)

  # criando a matriz e preenchendo com 0
  r2 <- matrix(data = 0,
               ncol = n_cores * n_vertices,
               nrow = ncol(matriz_combin) * n_cores,
               dimnames = list(NULL, names(fun_objetivo)))

  inicio <- 1
  # preenchenco a matriz com 1.
  for (cor in 1:n_cores) {
    for (n_combinacao in 1:ncol(matriz_combin)) {
      comb <- matriz_combin[, n_combinacao]

      # primeiro item
      vertice_i = paste0("V", comb[1], "_", cor)
      r2[inicio, vertice_i] <- 1

      # segundo item
      vertice_i = paste0("V", comb[2], "_", cor)
      r2[inicio, vertice_i] <- -1

      # terceiro item
      vertice_i = paste0("V", comb[3], "_", cor)
      r2[inicio, vertice_i] <- 1
      
      inicio <- inicio + 1
    }
  }

  return(r2)
}
