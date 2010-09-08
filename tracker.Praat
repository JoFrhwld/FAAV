select TextGrid PH06-2-1-AB-Jean

nint= Get number of intervals... 1

id = 1

for i from 1 to nint
	lab$ = Get label of interval... 1 i
 	if lab$ = "UW1"
		beg = Get start point... 1 i
		end = Get end point... 1 i
		mid = ((end-beg)/2) + beg

		wordint = Get interval at time... 2 mid
		wordbeg = Get start point... 2 wordint
		wordend = Get end point... 2 wordint

		firstint = Get interval at time... 1 wordbeg+0.001
		lastint = Get interval at time... 1 wordend-0.001
	
		trans$ = ""
		for j from firstint to lastint
			seg$ = Get label of interval... 1 j
			trans$ = trans$ + seg$ + " "
		endfor
		
		if beg = wordbeg
			prelab$ = Get label of interval... 1 i-1
			if prelab$ = "HH"
				beg = wordbeg
			endif
		endif
		
    		word$ = Get label of interval... 2 wordint
		
		
		index = (i - firstint) + 1
		idstr$ = "'id'"
		indexstr$ = "'index'"
		wordinfo$ = tab$ + word$+tab$+idstr$+tab$+trans$ +tab$+indexstr$ + newline$
		
		id = id + 1

		select LongSound PH06-2-1-AB-Jean
		Extract part... beg end 1
		Rename... jawn

		To Formant (burg)... 0 5 5000 0.025 50
		x$ = List... 0 1 6 0 3 1 2 1
		l = length (x$)
		endline = index (x$, newline$)
		
		info = l-endline
		toprint$ = right$ (x$, info)
		toprint2$ = replace$ (toprint$, newline$, wordinfo$, 0)

		
		
		fileappend "~/uw.txt" 'toprint2$'
		select Sound jawn
		Remove
		select Formant jawn
		Remove
		select TextGrid PH06-2-1-AB-Jean
	endif
endfor
