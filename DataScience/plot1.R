data<-read.table("household_power_consumption.txt",sep=";",header=TRUE,na.strings="?")
names(data)
data$Date<-as.Date(data$Date,"%d/%m/%Y")
data$Date
dt1<-as.Date("2007-02-01")
dt2<-as.Date("2007-02-02")
mydata<-subset(data, data$Date==dt1 | data$Date==dt2)
rm(data)
mydata$Time<-strptime(paste(format(mydata$Date,"%Y-%m-%d"),mydata$Time),"%Y-%m-%d%H:%M:%S")
format(mydata$Time,"%H:%M:%S")

library(base)
mydata$Global_active_power
hist(mydata$Global_active_power,main="Global Active Power",
     xlab="Global Active Power (kilowatts)",col="red")
png(file="plot1.png")
hist(mydata$Global_active_power,main="Global Active Power",
     xlab="Global Active Power (kilowatts)",col="red")
dev.off()
