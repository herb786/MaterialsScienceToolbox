fileUrl<-"https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2Fss06hid.csv"
download.file(fileUrl,destfile="idaho.csv")
data<-read.csv("idaho.csv",sep=",",header=TRUE)
namy<-names(data)
strsplit(namy,"wgtp")

fileUrl<-"https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2FGDP.csv"
download.file(fileUrl,destfile="grossdp.csv")
data<-read.csv("grossdp.csv",sep=",",header=TRUE,skip=4)
head(data)
data$X.4
million<-data$X.4[c(1:216)]
million<-gsub(",","",million)
million<-as.integer(million)
million
mean(million,na.rm=TRUE)
countryNames<-data$X.3[c(1:216)]
grep("^United",countryNames, value=TRUE)

fileUrl1<-"https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2FGDP.csv"
fileUrl2<-"https://d396qusza40orc.cloudfront.net/getdata%2Fdata%2FEDSTATS_Country.csv"
download.file(fileUrl1,destfile="grossdp.csv")
download.file(fileUrl2,destfile="edu.csv")
data1<-read.csv("grossdp.csv",sep=",",header=TRUE,skip=4)
data2<-read.csv("edu.csv",sep=",",header=TRUE)
head(data1)
head(data2)
fiscal<-data2$Special.Notes
sum(table(grep("^Fiscal year end: June",fiscal)))


install.packages("quantmod")
library(quantmod)
amzn = getSymbols("AMZN",auto.assign=FALSE)
sampleTimes = index(amzn)
library(lubridate)
amzn["2007-01-04"]
sampleTimes
sum(year(sampleTimes)==2012)
sum(year(sampleTimes)==2012 & wday(sampleTimes)==2)

