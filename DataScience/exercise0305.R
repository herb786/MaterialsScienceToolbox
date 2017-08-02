fileUrl<-"https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2Fss06hid.csv"
download.file(fileUrl,destfile="microdata.csv")
data<-read.csv("microdata.csv",sep=",",header=TRUE)
head(data)
agricultureLogical<-(data$ACR==3&data$AGS==6)
which(agricultureLogical) 

install.packages("jpeg")
library("jpeg")
data<-readJPEG("getdata_jeff.jpg",native=TRUE)
quantile(data,probs=c(0.3,0.8))


library(dplyr)
fileUrl<-"https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2FGDP.csv"
fileUrl2<-"https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2FEDSTATS_Country.csv"
download.file(fileUrl,destfile="microdata.csv")
download.file(fileUrl2,destfile="microdata2.csv")
country<-read.csv("microdata2.csv",sep=",",header=TRUE)
#microdata3.csv is the microdata.csv without garbage metadata
gdp<-read.csv("microdata3.csv",sep=";",stringsAsFactors = TRUE)
head(gdp)
head(country)
str(country)
sel1<-select(country,CountryCode,Income.Group)
superd<-merge(sel1,gdp,by.x="CountryCode",by.y="COUNTRY")

byIncome<-group_by(superd,Income.Group)
summarize(byIncome,mean(RANK))

quest<-quantile(superd$RANK,probs=c(0.0,0.2,0.4,0.6,0.8,1.0))
ranks<-cut(superd$RANK,quest)
table(superd$Income.Group,ranks)

