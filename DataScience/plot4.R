windows()
png(file="plot4.png")
par(mfrow = c(2, 2))
with(mydata,plot(Time, Global_active_power,
                 ylab="Global Active Power (kilowatts)",
                 xlab = "",
                 type="l"
))
with(mydata,plot(Time, Voltage,
                 ylab="Voltage",
                 xlab = "datetime",
                 type="l"
))
with(mydata,plot(Time, Sub_metering_1,
                 ylab="Energy sub mettering", 
                 type="l"
))
with(mydata,points(Time, Sub_metering_2, type="l",col="red"))
with(mydata,points(Time, Sub_metering_3, type="l",col="blue"))
legend("topright", lty=1, 
       col = c("black","blue", "red"), 
       legend = c("Sub_metering_1", "Sub_metering_2", "Sub_metering_3"))
with(mydata,plot(Time, Global_reactive_power,
                 ylab="Global_reactive_power",
                 xlab = "datetime",
                 type="l"
))
dev.off()