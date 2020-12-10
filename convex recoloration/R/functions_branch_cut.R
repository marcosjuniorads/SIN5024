options(scipen=999)

# retorna o índice do vetor com o maior valor.
get_index_max_value <- function(array) {
  index <- 1
  aux   <- array[1:1]

  for(i in 1:length(array)) {
    if(array[i:i] > aux) {
      aux   <- array[i:i]
      index <- i
    }
  }
  return(as.integer(index))
}

# Retorna a versao positiva de um número.
# Se -1, retorna 1. Se 1, retorna 1.
get_positive_number <- function(value) {
  return(ifelse(value < 0, value * -1, value))
}

# retorna o maior valor na comparação entre dois números.
get_maximum_number <- function(val1, val2) {
  
  # apenas garantindo que não haverá valores nulos na entrada
  val1 <- get_positive_number(val1)
  val2 <- get_positive_number(val2)

  return(ifelse(val1 > val2, val1, val2))
}

# retorna o maior valor em um array.
get_maximum_number_in_array <- function(array) {
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
    j <- get_index_max_value(mais[1:i])
    indexIneq[j:j] <- 1
    monta_inequacao(j - 1, "-", mais, menos, indexIneq)
  } else if(i >= 2) {
    j <- get_index_max_value(menos[2:i])

    if(menos[(j + 1):(j + 1)] > 0) {
      indexIneq[j:j] <- -1
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
  inequacao <- vetor_inequacao

  # ponteiro do vetor mais
  p <- NA

  # ponteiro de vetor menos
  q <- NA

  # inicia os vetores auxuliares mais e menos com o tamanho de V
  mais  <- rep(NA, length(v))
  menos <- rep(NA, length(v))
  inequacao <- rep(0, length(v))

  menos[1:1] <- -Inf
  mais[1:1]  <- v[1:1]
  mais[2:2]  <- v[2:2]
  menos[2:2] <- v[1:1] - v[2:2]

  # percorrendo o vetor criado.
  for (r in 2:length(v)) {
    p <- get_index_max_value(mais[1:r])
    q <- get_index_max_value(menos[1:r])

    mais[(r + 1):(r + 1)]  <- get_maximum_number(val1 = v[(r + 1):(r + 1)],
                                                 val2 = sum(menos[q:q],
                                                            v[(r + 1):(r + 1)]))
    menos[(r + 1):(r + 1)] <- mais[p:p] - v[(r + 1):(r + 1)]
  }

  menos <- menos[!is.na(menos)]
  mais  <- mais[!is.na(mais)]

  # inequação 'mais violada' está violada?
  if(get_maximum_number_in_array(mais) > 1 + ε){
    monta_inequacao(length(v), "+", mais, menos, inequacao)
  }
  return(inequacao)
}

# chamando a função
a <- sep_ineq_convex_gen(vetor_corte = c(0.1, 0.4, 0.3, 0.1, 0.7, 0.5, 0.5,
                                         0.2, 0.5, 0.5, 0.7))
