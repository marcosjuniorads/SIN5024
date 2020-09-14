# PROBLEMA 1

# Uma pequena companhia vende dois produtos denominados PRODUTO 1 e PRODUTO 2.
# Cada tonelada do produto 1 consome 30 horas de trabalho humano e cada tonelada
# do produto 2 consome 20 horas de trabalho humano. 
# O negócio possui um máximo de 2700 horas de trabalho humano para o período.
 
# Cada tonelada do produto 1 e 2 consomem, respectivamente, 5 e 10 horas de
# trabalho de máquinas. Há 850 horas máquina disponíveis no período.

# Cada tonelada do produto 1 gera um lucro de 20 Milhões, enquanto o produto 2
# gera o equivalente a 60 milhões. Por razões técnicas, a firma necessita
# produzir um minimo de 95 toneladas entre os dois produtos.

# Quantas toneladas de produto devem ser produzidas para maximizar o lucro?

# EXEMPLO 1  - FORMALIZANDO O PROBLEMA, TEMOS QUE:
# FUN 20 * X1 + 60 * X2
# st. WH = 30 * X1 + 20 * X2 <= 2.700
#     MH = 05 * X1 + 10 * X2 <= 850
#     PM = X1 + X2 <= 95


# LIBRARY LP SOLVE ----------------

library(lpSolve)

obj.function <- c(20, 60)
constr       <- matrix(c(30 , 20, 5, 10, 1, 1), ncol = 2, byrow = TRUE) # tal como em WH, MH, PM
sense        <- c("<=", "<=", ">=") # sinais para cada restrição
rhs          <- c(2700, 850, 95)    # valores do lado direito
modelsense   <- "max"

# resolvendo o modelo
prod.sol <- lp(direction = modelsense, 
               objective.in = obj.function,
               const.mat = constr,
               const.dir = sense,
               const.rhs = rhs,
               compute.sens = T)
prod.sol$solution

# Arguments -----------------
# DIRECTION	= Sring giving direction of optimization: "min" (default) or "max."
# OBJECTIVE.IN = Numeric vector of coefficients of objective function
# CONST.MAT	= Matrix of numeric constraint coefficients, one row per constraint,
#            one column per variable (unless transpose.constraints = FALSE).
# CONST.DIR	= Vector of character strings giving the direction of the constraint
#             each value should be one of "<," "<=," "=," "==," ">," or ">=".
#             (In each pair the two values are identical.)
# CONST.RHS	= Vector of numeric values for the righthand side of the constraints
# COMPUTE.SENS = compute sensitivity? Default 0 (no); any non-zero value="yes"
# BINARY.VEC = Numeric vector like int.vec giving the indices of variables that
#              are required to be binary.
# ALL.INT	= Logical: should all variables be integer? Default: FALSE.
# ALL.BIN	= Logical: should all variables be binary? Default: FALSE.


# LIBRARY GUROBI ----------------

library(gurobi)

# EXEMPLO 1  - FORMALIZANDO O PROBLEMA, TEMOS QUE:
# FUN OB = 20 * X1 + 60 * X2
# st. WH = 30 * X1 + 20 * X2 <= 2.700
#     MH = 05 * X1 + 10 * X2 <= 850
#     PM =      X1 +      X2 <= 95

model <- list()

model$obj <- c(20, 60) # função objetivo
model$A   <- matrix(c(30 , 20, 5, 10, 1, 1), ncol = 2, byrow = TRUE) # restricao
model$modelsense <- "max"
model$rhs <- c(2700, 850, 95)
model$sense <- c("<=", "<=", ">=")

# resolvendo o modelo
params <- list(OutputFlag = 0)
result <- gurobi(model, params)

print('Solution:')
print(result$objval)
print(result$x)

# Arguments -----------------

# A = The linear constraint matrix.
# obj = The linear objective vector (the c vector in the problem statement).
#       When present, you must specify one value for each column of A.
#       When absent, each variable has a default objective coefficient of 0.
# sense (optional) = The senses of the linear constraints. Allowed values are
#                    '=', '<', or '>'. You must specify one value for each row
#                     of A, or a single value to specify that all constraints
#                     have the same sense. When absent, all senses default '<'.
# rhs (optional) = The right-hand side vector for the linear constraints in the
#                  problem statement). You must specify one value for each row
#                  of A. When absent, the right-hand side vector defaults to
#                  the zero vector.
# vtype (optional) = The variable types. This vector is used to capture variable
#                    integrality constraints. Allowed values are 'C'
#                    (continuous), 'B' (binary), 'I' (integer), 'S' (semi
#                    continuous), or 'N' (semi-integer). Binary variables must
#                    be either 0 or 1. Integer variables can take any integer
#                    value between the specified lower and upper bounds. Semi
#                    continuous variables can take any value between the
#                    specified lower and upper bounds, or a value of zero.
#                    Semi-integer variables can take any integer value between
#                    the specified lower and upper bounds, or a value of zero.
#                    When present, you must specify one value for each column
#                    of A, or a single value to specify that all variables
#                    have the same type. When absent, each variable is treated
#                    as being continuous.
# modelsense (optional) = The optimization sense. Allowed values are 'min'
#                         (minimize) or 'max' (maximize). When absent, the
#                         default optimization sense is minimization.model$obj
