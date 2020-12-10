import gurobipy as gp
from gurobipy import GRB

# Criando o modelo
m = gp.Model("recoloration_convex")

#exemplo de entradas: model=gp.Model("recoloration_convex"),
#                     lista_vertices=[1,2,3] e lista_cores=[1,2]
def adicionar_variaveis_modelo(model, lista_vertices, lista_cores):
    for v in lista_vertices:
        for c in lista_cores:
            variable_name = 'ver' + str(v) + '_cor' + str(c)
            globals()[variable_name] = model.addVar(vtype=GRB.BINARY,
                                                    name=variable_name)
    return model

model = adicionar_variaveis_modelo(m, [1,2,3], [1,2])




# obter_funcao_objetivo <- function(numero_vertices, numero_cores, lista_cor) {
#
#   # fazendo eventuais conversões para o formato correto, caso necessário
#   numero_vertices <- as.numeric(numero_vertices)
#   numero_cores <- as.numeric(numero_cores)
#
#   # obtendo o total de combinações.
#   vetor_fo <- rep(1, numero_vertices * numero_cores)
#
#   # apenas gerando nomes para cada casela do vetor.
#   names_vetor <- expand.grid(paste0("V", rep(1:numero_vertices)),
#                              unique(cor_vertices)) %>% arrange(Var1)
#   names_vetor <- paste(names_vetor$Var1, names_vetor$Var2, sep = "_")
#
#   # nomeando o vetor
#   names(vetor_fo) <- names_vetor
#
#   # preenchendo o vetor com 0 para as caselas que contém a mesma cor do vertice
#   for (vertice in 1:numero_vertices) {
#     name <- paste0("V", vertice, "_", lista_cor[vertice])
#     vetor_fo[[name]] <- 0
#   }
#
#   return(vetor_fo)
# }