corr<-function(directory,threshold=0) {
  file_list <- list.files(path.expand(file.path("~","specdata")))
  value<-0
  for ( i in 1:332) {
    d0<-complete(directory,i)[2]
    if(d0>=threshold){
      setwd(path.expand(file.path("~","specdata")))
      dataset0<-read.csv(file_list[i])
      na.sulfate<-is.na(dataset0$sulfate)
      na.nitrate<-is.na(dataset0$nitrate)
      nas<-na.sulfate | na.nitrate
      index<-1:nrow(dataset0)
      index<-index[nas==TRUE]
      dataset0<-dataset0[-index,]
      mcor<-cor(dataset0$nitrate,dataset0$sulfate)
      value<- c(value,mcor)
    }
  }
  value<-value[2:length(value)]
  setwd(path.expand("~"))
  return(value)
  
}