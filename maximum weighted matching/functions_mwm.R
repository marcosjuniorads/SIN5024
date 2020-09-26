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

  grafo_data <- data.frame(u = vertice_origem,
                           v = vertice_destino,
                           p = peso_vertice)

  rm(peso_vertice, vertice_destino, vertice_origem)

  return(grafo_data)
}

criar_matriz_restricao <- function(dados_grafo, n_vertices, n_arestas) {
  # obtendo a lista de vertices do grafo
  lista_vertices <- unique(c(dados_grafo$u, dados_grafo$v))

  # criando matrix que armazenará as restrições para o problema.
  m_restricao <- matrix(data = 0, # 1 quando a aresta está conect. com o vértice
                        nrow = length(lista_vertices), # qnt de vértices
                        ncol = nrow(dados_grafo),
                        dimnames = list(paste0("VERTICE_", rep(1:n_vertices)),
                                        paste0("ARESTA_", rep(1:n_arestas))))

  for (vertice in lista_vertices) {
    arestas_relacionadas <- unique(c(which(dados_grafo$u == vertice),
                                     which(dados_grafo$v == vertice)))

    m_restricao[vertice, arestas_relacionadas] <- 1
  }
  return(m_restricao)
}

visualizar_grafo <- function(dados_grafo) {
  g <- graph_from_data_frame(dados_grafo, directed = F)
  plot(g, edge.label = E(g)$weight)
  rm(g)
}

imprime_weighted_matching <- function(resultado) {
  print("     RESULTADO DA OTIMIZAÇÃO     ")
  print("---------------------------------")
  print("QUAIS ARESTAS DEVO ESCOLHER?")
  print(paste("ARESTA", rep(1:length(resultado$x)))[resultado$x == 1])
  print("QUAL PESO TOTAL DO EMPARELHAMENTO?")
  print(resultado$objbound)
}
