rankhospital <- function(state, outcome, num = "best") {
  if (num == "best"){
    num <- 1
  }
  nom <- c("Hospital.Name","State","Hospital.30.Day.Death..Mortality..Rates.from.Heart.Attack","Hospital.30.Day.Death..Mortality..Rates.from.Heart.Failure","Hospital.30.Day.Death..Mortality..Rates.from.Pneumonia")
  set0 <- read.csv("outcome-of-care-measures.csv",colClasses = "character")
  frame0 <-set0[nom]
  frame1 <- frame0[frame0$State == state,]
  #outcome <- "heart failure"
  #num <- 4
  if (outcome == "heart failure"){
    frame2 <- frame1[c(nom[1],nom[4],nom[2])]
    frame2[,2] <- as.numeric(frame2[,2])
    frame2 <- frame2[!rowSums(is.na(frame2[2])), ]
    rank <- unique(frame2[2])
    rank2 <- rank[sort.list(rank[,1],na.last = TRUE, decreasing = FALSE),]
    set0 <- frame2[frame2$Hospital.30.Day.Death..Mortality..Rates.from.Heart.Failure == rank2[1], ]
    set0 <- set0[order(set0[,1]),]
    for ( i in 2:length(rank2)) {
      set1 <- frame2[frame2$Hospital.30.Day.Death..Mortality..Rates.from.Heart.Failure == rank2[i], ]
      set1 <- set1[order(set1[,1]),]
      set2 <- rbind(set0,set1)
      set0 <- set2
    }
    if (num == "worst"){
      num <- length(frame2[,2])
    }
    partial <- set0[num,]
    return (partial)
  }
  if (outcome == "heart attack"){
    frame2 <- frame1[c(nom[1],nom[3],nom[2])]
    frame2[,2] <- as.numeric(frame2[,2])
    frame2 <- frame2[!rowSums(is.na(frame2[2])), ]
    rank <- unique(frame2[2])
    rank2 <- rank[sort.list(rank[,1],na.last = TRUE, decreasing = FALSE),]
    set0 <- frame2[frame2$Hospital.30.Day.Death..Mortality..Rates.from.Heart.Attack == rank2[1], ]
    set0 <- set0[order(set0[,1]),]
    for ( i in 2:length(rank2)) {
      set1 <- frame2[frame2$Hospital.30.Day.Death..Mortality..Rates.from.Heart.Attack == rank2[i], ]
      set1 <- set1[order(set1[,1]),]
      set2 <- rbind(set0,set1)
      set0 <- set2
    }
    if (num == "worst"){
      num <- length(frame2[,2])
    }
    partial <- set0[num,]
    return (partial)
  }
  if (outcome == "pneumonia"){
    frame2 <- frame1[c(nom[1],nom[5],nom[2])]
    frame2[,2] <- as.numeric(frame2[,2])
    frame2 <- frame2[!rowSums(is.na(frame2[2])), ]
    rank <- unique(frame2[2])
    rank2 <- rank[sort.list(rank[,1],na.last = TRUE, decreasing = FALSE),]
    set0 <- frame2[frame2$Hospital.30.Day.Death..Mortality..Rates.from.Pneumonia == rank2[1], ]
    set0 <- set0[order(set0[,1]),]
    for ( i in 2:length(rank2)) {
      set1 <- frame2[frame2$Hospital.30.Day.Death..Mortality..Rates.from.Pneumonia == rank2[i], ]
      set1 <- set1[order(set1[,1]),]
      set2 <- rbind(set0,set1)
      set0 <- set2
    }
    if (num == "worst"){
      num <- length(frame2[,2])
    }
    partial <- set0[num,]
    return (partial)
  }
}