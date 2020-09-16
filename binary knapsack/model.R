# carregando as funções necessárias
source(paste0(getwd(), "/librarys.R"))
source(paste0(getwd(), "/binary knapsack/functions.R"))

# PROBLEMA: Dada uma mochila com capacidade C e N itens e respectivos pesos P e
# valores V escolher um subconjunto de itens para colocar na mochila cuja soma
# dos pesos não ultrapasse a capacidade da mochila e a soma dos valores seja max

# Formalizando o problema, temos que:
# FUN SOMATÓRIO de (Vi * Xi), onde: V = valores dos itens e
                                  # X = indicador se está na mochila
# st. SOMATÒRIO de (Pi * Xi) <= C, onde: P = Peso dos itens e
                                       # X = indicadador se está na mochila
#                                        X deve ser = 1 ou 0

# chamando funções para resolução do problema de otimização
nome_arq <- "instancia4.txt"

capacidade_mochila <- obter_capacidade(nome_arq)
numero_itens       <- obter_num_itens(nome_arq)
peso_valor_itens   <- obter_valor_peso(nome_arq)

# GERANDO O MODELO.
model <- list()

model$obj <- c(peso_valor_itens$valor)        # função objetivo
model$A   <- matrix(c(peso_valor_itens$peso), # restrições
                    ncol = numero_itens,      # diferentes colunas, pq referem-se
                    byrow = TRUE)             # a diferentes itens. Ex. abaixo
model$modelsense <- "max"
model$rhs   <- capacidade_mochila             # lado direito da restrição
model$sense <- c("<=")
model$vtype <- "B"                            # modelo binário. Só escolhe 1 / 0

# RESTRIÇÕES
#        portanto 5 colunas                                               RHS
# SUM [(ITEM 1*X) + (ITEM 2*X) + (ITEM 3*X) + (ITEM 4*X) + (ITEM 5*X)] <= Cap. Mochila


# RESOLVENDO O MODELO
params <- list(OutputFlag = 0)
result <- gurobi(model, params)


# IMPRIMINDO O RESULTADO
imprime_resultados_mochila(result)

