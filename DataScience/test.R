a <- matrix (rnorm(16),  nrow = 4, ncol = 4)
b <- matrix (c(1,0,0,1), nrow = 2, ncol = 2)
c <- matrix (c(4,3,3,2), nrow = 2, ncol = 2)

source("cachematrix.R")
aa <- makeCacheMatrix(a)
ai <- cacheSolve(aa)

bb <- makeCacheMatrix(b)
bi <- cacheSolve(bb)

cc <- makeCacheMatrix(c)
ci <- cacheSolve(cc)
