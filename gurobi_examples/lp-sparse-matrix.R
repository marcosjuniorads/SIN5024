# Copyright 2020, Gurobi Optimization, LLC
#
# This example formulates and solves the following simple LP model:
#  maximize
#        x + 2 y + 3 z
#  subject to
#        x +   y       <= 1
#              y +   z <= 1

library(Matrix)
library(gurobi)

model <- list()

model$A          <- matrix(c(1, 1, 0, 0, 1, 1), nrow = 2, byrow = T)
model$obj        <- c(1, 2, 3)
model$modelsense <- 'max'
model$rhs        <- c(1, 1)
model$sense      <- c('<', '<')

result <- gurobi(model)

print(result$objval)
print(result$x)

# Second option for A - as a sparseMatrix (using the Matrix package)...

model$A <- spMatrix(nrow = 2,
                    ncol = 3,
                    i = c(1, 1, 2, 2), # linhas onde estão os valores != 0
                    j = c(1, 2, 2, 3), # colunas onde estão os valores != 0
                    x = c(1, 1, 1, 1)  # armazena somente os valores != 0
                    )
result <- gurobi(model)

print(result$objval)
print(result$x)

# Clear space
rm(result, params, model)
