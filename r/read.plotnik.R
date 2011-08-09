read.plotnik <- function(file){
  require(plyr)
  require(reshape)
  data <- scan(file, blank.lines.skip = F, what = "list", sep = "\n", quiet = T)
  filename <- rev(unlist(strsplit(file, split = "/")))[1]
  
  header.info <- data[1]
  for(i in 3:length(data)){
    if(nchar(data[[i]]) <= 1){
      break
    }
    data[[i]] <- paste(data[[i]], header.info, sep = ",")
  }
  
  len <- (i-1)-2
  
  to.compile <- data[3:(i-1)]
  out <- ldply(to.compile, function(x) unlist(strsplit(x, split = ",")))
  colnames(out) <- c(c("F1","F2","F3","VCoding","Dur_Stress","Info"), paste("V",7:ncol(out), sep = ""))
  out$Word <- colsplit(out$Info, split = " ", names = "Word")$Word
  if(length(grep("\\.", out$Dur_Stress)) > 0){
	  out <- cbind(out, colsplit(out$Dur_Stress, split = "\\.", names = c("Stress","Dur_msec")))
	  out$Dur_msec <- as.numeric(out$Dur_msec)
  }else{
      out$Stress <- as.numeric(out$Dur_Stress)	
  }
 
  out$VCoding <- as.character(out$VCoding)
  
  if(length(grep("\\.", out$VCoding)) > 0){
  	vcodings <- data.frame(VClass = gsub("\\..*","",out$VCoding), envs = gsub(".*\\.","",out$VCoding),stringsAsFactors=F)
  	for(i in 1:nrow(vcodings)){
  		env <- vcodings$envs[i]
  		while(nchar(env) < 5){
  			env <- paste(env, "0", sep = "")	
  		}
  		vcodings$envs[i] <- env
  	}
  vcodings <- cbind(vcodings, 
                    ldply(vcodings$envs, function(x) unlist(strsplit(x, split = ""))))
  }else{
	vcodings <- data.frame(VClass = out$VCoding, envs = "00000",stringsAsFactors=F)
	vcodings <- cbind(vcodings, 
                    ldply(vcodings$envs, function(x) unlist(strsplit(x, split = ""))))
  }
  
  colnames(vcodings) <- c("VClass","envs", "Manner","Place","Voice","PreSeg","FolSeq")
  
  vclass.codes = c(
     `1` = "i",
     `2` = "e",
     `3` = "ae",
     `5` = "o",
     `6` = "uh",
     `7` = "u",
     `*` = "*",
     `11` = "iy",
     `12` = "iyF",
     `21` = "ey",
     `22` = "eyF",
     `41` = "ay",
     `47` = "ay0",
     `61` = "oy",
     `42` = "aw",
     `62` = "ow",
     `63` = "owF",
     `72` = "uw",
     `73` = "Tuw",
     `82` = "iw",
     `33` = "aeh",
     `39` = "aeBR",
     `43` = "ah",
     `53` = "oh",
     `14` = "iyr",
     `24` = "eyr",
     `44` = "ahr",
     `54` = "ohr",
     `64` = "owr",
     `74` = "uwr",
     `94` = "*hr"
  )
  
  manner.codes = c(
    `1` = "stop",
    `2` = "affricate",
    `3` = "fricative",
    `4` = "nasal",
    `5` = "lateral",
    `6` = "central"
  )
  
  place.codes = c(
    `1` = "labial",
    `2` = "labiodental",
    `3` = "interdental",
    `4` = "apical",
    `5` = "palatal",
    `6` = "velar"
  )
  
  voice.codes = c(
    `1` = "voiceless",
    `2` = "voiced"
  )
  
  preseg.codes = c(
    `1` = "oral labial",
    `2` = "nasal labial",
    `3` = "oral apical",
    `4` = "nasal apical",
    `5` = "palatal",
    `6` = "velar",
    `7` = "liquid",
    `8` = "obstruent liquid",
    `9` = "w/y"
  )
  
  folseq.codes = c(
    `1` = "one_fol_syll",
    `2` = "two_fol_syl",
    `3` = "complex_coda",
    `4` = "complex_one_syl",
    `5` = "complex_two_syl"
  )
  
  vcodings$VClass <- as.factor(vclass.codes[vcodings$VClass])
  vcodings$Manner <- as.factor(manner.codes[vcodings$Manner])
  vcodings$Place <- as.factor(place.codes[vcodings$Place])
  vcodings$Voice <- as.factor(voice.codes[vcodings$Voice])
  vcodings$PreSeg <- as.factor(preseg.codes[vcodings$PreSeg])
  vcodings$FolSeq <- as.factor(folseq.codes[vcodings$FolSeq])
  
  out <- cbind(out, vcodings[,-2])
  
#   out$Time <- 0
#   for(i in 1:nrow(out)){
#   	timestr <- rev(unlist(strsplit(out$Info[i], " ")))[1]
#   	out$Time[i] <- as.numeric(timestr)
#   }
  
  out$F1 <- as.numeric(out$F1)
  out$F2 <- as.numeric(out$F2)
  out$F3 <- as.numeric(out$F3)
  out$Stress <- as.factor(out$Stress)
  out$Word <- as.factor(out$Word)
  if(length(grep("\\[f\\]", out$Info)) > 0){
    out$Function <- FALSE
    out[grep("\\[f\\]", out$Info),]$Function <- TRUE
  }
  
  out$File <- filename
  
  return(out)
}

