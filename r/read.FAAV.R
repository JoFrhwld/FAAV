read.FAAV <- function(file){
	header = scan(file, what = "character", sep = ",", strip.white = T, nlines = 1, quiet = T)
	
	fileName <- tail(unlist(strsplit(file,.Platform$file.sep)),1)
	data <- read.delim(file, skip = 2)[,1:22]
	data$Name <- header[1]
	data$Age <- header[2]
	data$Sex <- header[3]
	data$City <- header[4]
	data$State <- header[5]
	data$Date <- header[6]
	data$File <- fileName
	return(data)
}