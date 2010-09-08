## This script extracts formant measurements at 6 milisecond intervals (the Praat default)
## It does this rapidly using:
##		
##	To formant (burg)...
##	List...

form Test
	word objectName PH06-2-1-AB-Jean
	word vowelToMeasure AY1
	word outputfile ~/ay.txt
	real maxformant 5500
	real nformants 5
endform

select TextGrid 'objectName$'
nint= Get number of intervals... 1

#This is a counter to keep tokens of the same lexical item distinct
id = 1

for i from 1 to nint
	lab$ = Get label of interval... 1 i
 	if lab$ = vowelToMeasure$
		
		#These are time points of the vowel
		beg = Get start point... 1 i
		end = Get end point... 1 i
		mid = ((end-beg)/2) + beg

		#These are intervals and time points of the word
		wordint = Get interval at time... 2 mid
		wordbeg = Get start point... 2 wordint
		wordend = Get end point... 2 wordint

		#These are the first and last intervals of the word's phonemes
		firstint = Get interval at time... 1 wordbeg+0.001
		lastint = Get interval at time... 1 wordend-0.001
	
		#trans$ will hold a space delimited transcription of the word
		trans$ = ""
		for j from firstint to lastint
			seg$ = Get label of interval... 1 j
			trans$ = trans$ + seg$ + " "
		endfor
		
		#Word holds the word itself
		word$ = Get label of interval... 2 wordint
		
		#This is meant to be a correction for bad forced alignment involving preceding HH
		#Commented out 9/7/2010
		#if beg = wordbeg
		#	prelab$ = Get label of interval... 1 i-1
		#	if prelab$ = "HH"
		#		beg = wordbeg
		#	endif
		#endif
		
    		#index holds the index (starting at 1) of the vowel being measured within 
		#space delimited transcription
		index = (i - firstint) + 1

		# Numerals must be converted to strings to be appended
		idstr$ = "'id'"
		indexstr$ = "'index'"

		#wordinfo$ holds the 
		wordinfo$ = tab$ + word$+tab$+idstr$+tab$+trans$ +tab$+indexstr$ + newline$
		
		
		# This is the acoustic analysis bit
		select LongSound 'objectName$'
		Extract part... beg end 1
		Rename... jawn

		# These two commands work much faster than looping over a sound file
		To Formant (burg)... 0 'nformants' 'maxformant' 0.025 50
		x$ = List... 0 1 6 0 3 1 2 1
		
		#This whole block of code simply strips out the column headers of the formant list
		l = length (x$)
		endline = index (x$, newline$)
		info = l-endline
		toprint$ = right$ (x$, info)
		
		#This enriches the formant list with the word info,
		# replacing all newlines with word info
		toprint2$ = replace$ (toprint$, newline$, wordinfo$, 0)

		# Write to output
		fileappend 'outputfile$' 'toprint2$'
		
		#Housekeeping
		select Sound jawn
		Remove
		select Formant jawn
		Remove
		id = id + 1
		select TextGrid 'objectName$'
	endif
endfor
