# carregando as funções necessárias
source(paste0(getwd(), "/librarys.R"))
source(paste0(getwd(), "/functions.R"))

# PROBLEMA: Dada uma mochila com capacidade C e N itens e respectivos pesos P e
# valores V escolher um subconjunto de itens para colocar na mochila cuja soma
# dos pesos não ultrapasse a capacidade da mochila e a soma dos valores seja max

# Formalizando o problema, temos que:
# FUN Vi * Xi, onde v = valores dos itens e X = indicador se está na mochila
# st. Pi * Xi <= C, onde P = Peso dos itens e X = indicadador se está na mochila
#     X deve ser = 1 ou 0

# chamando funções para resolução do problema de otimização
nome_arq <- "instancia4.txt"

capacidade_mochila <- obter_capacidade(nome_arq)
numero_itens       <- obter_num_itens(nome_arq)
peso_valor_itens   <- obter_valor_peso(nome_arq)

# gerando o modelo
model <- list()

model$obj <- c(peso_valor_itens$valor)        # função objetivo
model$A   <- matrix(c(peso_valor_itens$peso), # restrições
                    ncol = numero_itens,
                    byrow = TRUE)
model$modelsense <- "max"
model$rhs   <- capacidade_mochila
model$sense <- c("<=")
model$vtype <- "B"

# resolvendo o modelo
params <- list(OutputFlag = 0)
result <- gurobi(model, params)

imprime_resultados_mochila(result)

