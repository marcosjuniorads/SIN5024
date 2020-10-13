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
