complete<-function(directory,ids=1:332) {
  setwd(path.expand("~"))
  file_list <- list.files(path.expand(file.path("~","specdata")))
  setwd(path.expand(file.path("~","specdata")))
  nob<-0
  for ( i in 1:length(ids)) {
    dataset<-read.csv(file_list[ids[i]])
    na.sulfate<-is.na(dataset$sulfate)
    na.nitrate<-is.na(dataset$nitrate)
    nas<-na.sulfate | na.nitrate
    nob[i]<-nrow(dataset)-sum(nas)
  }
  setwd(path.expand("~"))
  
  value <-data.frame(id =ids, nobs=nob)
  return(value)
  
  
}