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
