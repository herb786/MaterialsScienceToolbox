names(mydata)
windows()
png(file="plot3.png")
with(mydata,plot(Time, Sub_metering_1,
                 ylab="Energy sub mettering", 
                 type="l"
))
with(mydata,points(Time, Sub_metering_2, type="l",col="red"))
with(mydata,points(Time, Sub_metering_3, type="l",col="blue"))
legend("topright", lty=1, 
       col = c("black","blue", "red"), 
       legend = c("Sub_metering_1", "Sub_metering_2", "Sub_metering_3"))
dev.off()

