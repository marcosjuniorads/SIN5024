# Formato dos arquivos de entrada:
# num_vertices
# num_arestas
# vertice_origem (u) vertice_destino (v) peso (p)
# u_1 v_1 peso_1
# u_2 v_2 peso_2
# ...
# u_n v_n peso_n  ### ONDE n = num_arestas


obter_numero_vertices <- function(nome_arquivo) {
  path <- paste0(getwd(), "/maximum weighted matching/instancias/", nome_arquivo)
  data <- read.delim(path, header = FALSE, comment.char = "#")

  return(as.numeric(as.character(data[1, ])))
}


obter_numero_arestas <- function(nome_arquivo) {
  path <- paste0(getwd(), "/maximum weighted matching/instancias/", nome_arquivo)
  data <- read.delim(path, header = FALSE, comment.char = "#")

  return(as.numeric(as.character(data[2, ])))
}


obter_dados_grafo <- function(nome_arquivo) {
  path <- paste0(getwd(), "/maximum weighted matching/instancias/", nome_arquivo)
  data <- read.delim(path, header = FALSE, comment.char = "#")

  # obtendo os valores para os vertices de origem
  vertice_origem <- c()
  for (i in 3:nrow(data)) {
    vertice_origem <- c(vertice_origem,
                        as.numeric(
                          strsplit(as.character(data[i, ]), " ")[[1]])[1])
  }

  vertice_destino <- c()
  for (i in 3:nrow(data)) {
    vertice_destino <- c(vertice_destino,
                        as.numeric(
                          strsplit(as.character(data[i, ]), " ")[[1]])[2])
  }

  peso_vertice <- c()
  for (i in 3:nrow(data)) {
    peso_vertice <- c(peso_vertice,
                         as.numeric(
                           strsplit(as.character(data[i, ]), " ")[[1]])[3])
  }

  grafo_data <- data.frame(vertice_u = vertice_origem,
                           vertice_v = vertice_destino,
                           peso = peso_vertice)

  rm(peso_vertice, vertice_destino, vertice_origem)

  return(grafo_data)
}

obter_lista_adjacencia <- function(dados_grafo) {
  # obtendo a lista de vertices do grafo
  lista_vertices <- unique(c(peso_arestas$vertice_u, peso_arestas$vertice_v))
  df_adjacencia  <- setNames(data.frame(matrix(ncol = length(lista_vertices),
                                               nrow = 0)),
                             c(lista_vertices))

  for (vertice in lista_vertices) {
    vizinhos1    <- peso_arestas %>%
                    dplyr::filter(vertice_u == vertice)
    vizinhos1    <- vizinhos1$vertice_v

    vizinhos2    <- peso_arestas %>%
                    dplyr::filter(vertice_v == vertice)
    vizinhos2    <- vizinhos2$vertice_u

    v_adjacentes <- unique(c(vizinhos1, vizinhos2))

    df_adjacencia <- rbind(df_adjacencia,
                           paste(v_adjacentes, collapse = ' '),
                           stringsAsFactors = FALSE)
    rm(vizinhos1, vizinhos2, v_adjacentes)
  }

  names(df_adjacencia) <- c("vizinhos")
  df_adjacencia <- separate(data = df_adjacencia,
                            col = "vizinhos", sep = " ",
                            into = paste0("vizinho_",
                                   as.character(rep(1:length(lista_vertices))))
                            )
  df_adjacencia <- df_adjacencia[, !apply(is.na(df_adjacencia), 2, all)]
  return(df_adjacencia)
}

visualizar_grafo <- function(dados_grafo) {
  g <- graph_from_data_frame(dados_grafo, directed = F)
  plot(g, edge.label = E(g)$weight)
  rm(g)
}
