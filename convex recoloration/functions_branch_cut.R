# retorna o índice do item com o maior valor
argmax <- function(array) {
  index <- 1
  aux   <- array[1:1]

  for(i in 1:length(array)) {
    if(array[i:i] > aux) {
      aux   <- array[i:i]
      index <- i
    }
  }
  return(index)
}

# retorna a versao positiva do numero
getPositivo <- function(value) {
  return(ifelse(value < 0, value * -1, value))
}

# maior valor na comparacao (os dois sao comparados como positivos)
maxCompare <- function(val1, val2) {
  val1 <- getPositivo(val1)
  val2 <- getPositivo(val2)

  return(ifelse(val1 > val2, val1, val2))
}

# maior valor em um array
maxArray <- function(array) {
  aux <- array[1:1]

  for (i in 1:length(array)) {
    if(array[i:i] > aux) {
      aux <- array[i:i]
    }
  }
  return(aux)
}

monta_inequacao <- function(i, sinal, mais, menos, indexIneq) {
  if(sinal == "+" & i >= 1) {
    j <- argmax(mais[1:(i+1)])

    # criar funcao que monta a inequacao, adicionar o resultado com o indice+1
    # no lhs da inequacao
    indexIneq <- rbind(indexIneq, j)
    monta_inequacao(j - 1, "-", mais, menos, indexIneq)
  } else if(i >= 2) {
    j <- argmax(menos[1:i+1])

    # adiciona 1 pq ja começou contando do 1 e nao do zero
    if(menos[(j + 1):(j + 1)] > 0) {
      # criar funcao que monta a inequacao, adiciona o resultado com o indice
      #  -1 no lhs da inequacao
      indexIneq <- rbind(indexIneq, (j + 1))
      monta_inequacao(j, "+", mais, menos, indexIneq)
    }
  }
  return(indexIneq)
}

# prenche mais ou menos 
sep_ineq_convex_gen <- function(vetor_corte,
                                vetor_mais      = NULL,
                                vetor_menos     = NULL,
                                vetor_inequacao = NULL,
                                ε = 0.01) {

  # copiando os valores dos parâmetros que serão alterados dentro da função
  v         <- vetor_corte
  mais      <- vetor_mais
  menos     <- vetor_menos
  indexIneq <- vetor_inequacao

  # inicia os vetores auxuliares mais e menos com o tamanho de V
  mais  <- rep(NA, length(v))
  menos <- rep(NA, length(v))

  menos[1:1] <- -0
  mais[1:1]  <- v[1:1]
  mais[2:2]  <- v[2:2]
  menos[2:2] <- v[1:1] - v[2:2]

  # percorrendo o vetor criado.
  for (r in 2:length(v)) {
    p <- argmax(mais[1:r])
    q <- argmax(menos[2:r]) + 1

    mais[(r+1):(r+1)]  <- maxCompare(val1 = v[(r+1):(r+1)],
                                     val2 = menos[q:q] + v[(r+1):(r+1)])
    menos[(r+1):(r+1)] <- mais[p:p] - v[(r+1):(r+1)]
  }

  menos <- menos[!is.na(menos)]
  mais  <- mais[!is.na(mais)]

  # o maior valor do vetor "mais" representa se inequacao está violada
  if(maxArray(mais) > 1 + ε){
    monta_inequacao(length(v) - 1,
                    "+",
                    mais,
                    menos,
                    indexIneq)
  }

  return(indexIneq) #o que essa função deveria retornar? esse vetor?
}

# chamando a função
a <- sep_ineq_convex_gen(vetor_corte = c(0.1, 0.4, 0.3, 0.1, 0.7, 0.5, 0.5,
                                         0.2, 0.5, 0.5, 0.7))
