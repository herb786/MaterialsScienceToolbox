best <- function(state, outcome) {
  ## Read outcome data
  ## Check that state and outcome are valid
  ## Return hospital name in that state with lowest 30-day death
  ## rate
  nom <- c("Hospital.Name","State","Hospital.30.Day.Death..Mortality..Rates.from.Heart.Attack","Hospital.30.Day.Death..Mortality..Rates.from.Heart.Failure","Hospital.30.Day.Death..Mortality..Rates.from.Pneumonia")
  set0 <- read.csv("outcome-of-care-measures.csv",colClasses = "character")
  frame0 <-set0[nom]
  frame1 <- frame0[frame0$State == state,]
  if (outcome == "heart failure"){
    frame2 <- frame1[c(nom[1],nom[4])]
    frame2[,2] <- as.numeric(frame2[,2])
    frame2 <- frame2[!rowSums(is.na(frame2[2])), ]
    vmax <- min(frame2[2], na.rm=TRUE)
    partial <- frame2[frame2$Hospital.30.Day.Death..Mortality..Rates.from.Heart.Failure == vmax, ]
    return (partial)
    
  }
  if (outcome == "heart attack"){
    frame2 <- frame1[c(nom[1],nom[3])]
    frame2[,2] <- as.numeric(frame2[,2])
    frame2 <- frame2[!rowSums(is.na(frame2[2])), ]
    vmax <- min(frame2[2], na.rm=TRUE)
    partial <- frame2[frame2$Hospital.30.Day.Death..Mortality..Rates.from.Heart.Attack == vmax, ]
    return (partial)
    
  }
  if (outcome == "pneumonia"){
    frame2 <- frame1[c(nom[1],nom[5])]
    frame2[,2] <- as.numeric(frame2[,2])
    frame2 <- frame2[!rowSums(is.na(frame2[2])), ]
    vmax <- min(frame2[2], na.rm=TRUE)
    partial <- frame2[frame2$Hospital.30.Day.Death..Mortality..Rates.from.Pneumonia == vmax, ]
    return (partial)
    
    
  }
 
  
}