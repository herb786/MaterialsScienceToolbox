install.packages("readr")
library(readr)
gc()
memory.size()

features<-read.csv(file.path("UCI HAR Dataset","features.txt"),sep=" ",header=FALSE)
act_labels<-read.csv(file.path("UCI HAR Dataset","activity_labels.txt"),sep=" ",header=FALSE)

### The variables have the same name as the files
path<-file.path("UCI HAR Dataset","test")
xtest<-read_fwf(file=file.path(path,"X_test.txt"),fwf_widths(rep(16,561)))
ytest<-read.csv(file.path(path,"y_test.txt"),sep=" ",header=FALSE)
subjecttest<-read.csv(file.path(path,"subject_test.txt"),sep=" ",header=FALSE)

### The variables have the same name as the files
path<-file.path("UCI HAR Dataset","train")
xtrain<-read_fwf(file=file.path(path,"X_train.txt"),fwf_widths(rep(16,561)))
ytrain<-read.csv(file.path(path,"y_train.txt"),sep=" ",header=FALSE)
subjecttrain<-read.csv(file.path(path,"subject_train.txt"),sep=" ",header=FALSE)

### Descriptive variable names
### I will use the same names provided by the documentation
colnames(xtest)<-features$V2
colnames(xtrain)<-features$V2

### I appended two columns to both datasets test and train
### with the names subject and activity
install.packages("plyr")
library(plyr)
xtest<-cbind(xtest,subjecttest)
xtest<-cbind(xtest,ytest)
colnames(xtest)[562]<-"subject"
colnames(xtest)[563]<-"activity"
xtrain<-cbind(xtrain,subjecttrain)
xtrain<-cbind(xtrain,ytrain)
colnames(xtrain)[562]<-"subject"
colnames(xtrain)[563]<-"activity"

### Merging both dataframes test and train by rows
total <- rbind(xtest, xtrain) 

### Mean and Std deviation
### I kept variables with mean, std, subject and activity in the column headers.
names(total)
mset<-grep("mean|std()|subject|activity",names(total))
data<-subset(total,select=mset)
rm(xtest,xtrain,total)


### Descriptive activity names
### I will use the activity names giben by the documentation
data$activity <- as.factor(data$activity)
labf<-factor(data$activity,levels=act_labels$V1)
library(plyr)
vvv<-as.character(act_labels$V2)
data$activity<-mapvalues(data$activity, from = act_labels$V1, to = vvv )


### Average by activty and subject
library(dplyr)
groups <- group_by(data, activity, subject)
result<-summarise_each(groups,funs(mean))
write.table(result,"tidy_data.txt",row.name=FALSE)












