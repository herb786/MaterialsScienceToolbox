pollutantmean<-function(directory,pollutant,id=1:332) {
  print(id)
  file_list <- list.files(path.expand(file.path("~","specdata")))
  setwd(path.expand(file.path("~","specdata")))
  dataset0<-read.csv(file_list[id[1]])
  if (length(id)>1){
    for ( i in 2:length(id)) {
      dataset1<-read.csv(file_list[id[i]])
      dataset2<-rbind(dataset0,dataset1)
      dataset0<-dataset2
    }
  }
  setwd(path.expand("~"))
  if (pollutant == "sulfate"){
    value<-mean(dataset0$sulfate, na.rm=TRUE)
  }
  if (pollutant == "nitrate"){
    value<-mean(dataset0$nitrate, na.rm=TRUE)
  }
  return(value)
}