read.FAAV <- function(file){
	header = scan(file, what = "character", sep = ",", strip.white = T, nlines = 1, quiet = T)
	
	fileName <- tail(unlist(strsplit(file,.Platform$file.sep)),1)
	data <- read.delim(file, skip = 2)[,1:22]
	data$Name <- factor(header[1])
	data$Age <- factor(header[2])
	data$Sex <- factor(header[3])
	data$City <- factor(header[4])
	data$State <- factor(header[5])
	data$Date <- factor(header[6])
	data$File <- factor(fileName)
	return(data)
}