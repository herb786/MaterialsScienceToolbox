## Put comments here that give an overall description of what your
## functions do


## This function saves a matrix into cache.
## To save a matrix A into cache call makeCacheMatrix(A)
## To retrieve the matrix A call myCacheMatrix$get() where
##    myCacheMatrix is the result of makeCacheMatrix(A)
## To set the inverse of a matrix A call myCacheMatrix$setInverse(solve(A))
## To get the inverse matrix call yourCacheMatrix$getInverse()


makeCacheMatrix <- function(x = matrix()) {
  m <- NULL
  set <- function(y) {
    x <<- y
    m <<- NULL
  }
  get <- function() x
  setInverse <- function(solve) m <<- solve
  getInverse <- function() m
  list(set = set, get = get,
       setInverse = setInverse,
       getInverse = getInverse)
}


## This function computes the inverse of matrix A and save it into cache
## In case the inverse has already been calculated and stored into cache, the function 
## shows a message and the result of the calculation.
## To retrieve the inverse call myCacheMatrix$getInverse()

cacheSolve <- function(x, ...) {
        ## Return a matrix that is the inverse of 'x'
  m <- x$getInverse()
  if(!is.null(m)) {
    message("getting cached data")
    return(m)
  }
  data <- x$get()
  m <- solve(data, ...)
  x$setInverse(m)
  m
}
