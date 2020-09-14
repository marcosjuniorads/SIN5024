# Formato dos arquivos de entrada:
# capacidade da mochila
# n_itens
# v_1 v_2 ... v_n (valores dos itens)
# p_1 p_2 ... p_n (pesos dos itens)


obter_capacidade <- function(nome_arquivo) {
  path <- paste0(getwd(), "/instancias/mochila/", nome_arquivo)
  data <- read.delim(path, header = FALSE, comment.char = "#")

  return(as.numeric(as.character(data[1, ])))
}


obter_num_itens <- function(nome_arquivo) {
  path <- paste0(getwd(), "/instancias/mochila/", nome_arquivo)
  data <- read.delim(path, header = FALSE, comment.char = "#")

  return(as.numeric(as.character(data[2, ])))
}


obter_valor_peso <- function(nome_arquivo) {
  path <- paste0(getwd(), "/instancias/mochila/", nome_arquivo)
  data <- read.delim(path, header = FALSE, comment.char = "#")

  valor_item <- as.numeric(strsplit(as.character(data[3, ]), " ")[[1]])
  peso_item  <- as.numeric(strsplit(as.character(data[4, ]), " ")[[1]])

  valor_peso <- data.frame(peso = peso_item, valor = valor_item)

  return(valor_peso)
}


imprime_resultados_mochila <- function(resultado) {
  itens_escolhidos <- resultado$x
  peso_itens       <- peso_valor_itens$peso
  valor_itens      <- peso_valor_itens$valor

  print("             CONTEXTO            ")
  print("---------------------------------")
  print("PESO DE CADA ITEM DISPONÍVEL:")
  print(peso_itens)
  print("VALOR DE CADA ITEM DISPONÍVEL")
  print(valor_itens)

  print("     RESULTADO DA OTIMIZAÇÃO     ")
  print("---------------------------------")
  print("QUANTOS ITENS DEVO PEGAR DE CADA?")
  print(itens_escolhidos)
  print("PESO TOTAL DA MOCHILA:")
  print(sum(itens_escolhidos * peso_itens))
  print("VALOR DOS ITENS NA MOCHILA:")
  print(sum(itens_escolhidos * valor_itens))
}
