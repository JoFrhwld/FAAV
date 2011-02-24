form jawn
	word file PH06-2-6-Amy
	word outfile outfile	
	sentence Search_Segments T D
	comment Word context
	boolean End_Of_Word 1
	boolean Start_Of_Word 0
	boolean All_Contexts 0
	sentence Search_Pre_Context consonant
	sentence Search_Post_Context
	sentence Stop_Pre_Context R
	sentence Stop_Post_Context T D DH TH JH SH
	sentence Stop_Words AND
endform

search_Segments$ = " "+search_Segments$+" "

if index(search_Pre_Context$,"vowel") > 0
	search_Pre_Context$ = " AA AE AH AO AW AX AY EH EY IH IY OW OY UH UW "
elsif index(search_Pre_Context$, "consonant") > 0
	search_Pre_Context$ = " B CH DH DX AXR EL EM EN ER F G HH HV JH K L M N NX NG P R S SH T TH V W Y Z ZH "
else
	search_Pre_Context$ = " "+search_Pre_Context$+" "
endif

if index(search_Post_Context$,"vowel") > 0
	search_Post_Context$ = " AA AE AH AO AW AX AY EH EY IH IY OW OY UH UW "
elsif index(search_Post_Context$ ,"consonant") > 0
	search_Post_Context$ = " B CH DH DX AXR EL EM EN ER F G HH HV JH K L M N NX NG P R S SH T TH V W Y Z ZH "
else
	search_Post_Context$ = " "+search_Post_Context$+" "
endif

if index(stop_Pre_Context$, "vowel") >0
	stop_Pre_Context$ = " AA AE AH AO AW AX AY EH EY IH IY OW OY UH UW "
elsif index(stop_Pre_Context$ ,"consonant") >0
	stop_Pre_Context$ = " B CH DH DX AXR EL EM EN ER F G HH HV JH K L M N NX NG P R S SH T TH V W Y Z ZH "
else
	stop_Pre_Context$ = " "+stop_Pre_Context$+" "
endif

if index(stop_Post_Context$, "vowel") > 0
	stop_Post_Context$ = " AA AE AH AO AW AX AY EH EY IH IY OW OY UH UW "
elsif index(stop_Post_Context$, "consonant") > 0
	stop_Post_Context$ = " B CH DH DX AXR EL EM EN ER F G HH HV JH K L M N NX NG P R S SH T TH V W Y Z ZH "
else
	stop_Post_Context$ = " "+stop_Post_Context$+" "
endif

stop_Words$ = " "+stop_Words$+" "

select TextGrid 'file$'
plus LongSound 'file$'
Edit
editor TextGrid 'file$'
endeditor

select TextGrid 'file$'


#fileappend 'outfile$' 'Word''tab$''code''tab$''finalSeg''tab$''preSeg''tab$''folSeg''tab$''vPerSecond''tab$''begin''tab$''end''tab$''folSegDur''newline$'



if all_Contexts == 1
	ph_Intervals = Get number of intervals... 1
	for int from 1 to ph_Intervals
		seg$ = Get label of interval... 1 int
		if index(search_Segments$, " "+seg$+" ") > 0
			condition_met = 1
			
			seg_Start = Get start point... 1 int
			seg_End = Get end point... 1 int
			seg_Dur = seg_End-seg_Start
			seg_Mid = seg_Start + (seg_Dur/2)

			word_Int = Get interval at time... 2 seg_Mid
			word$ = Get label of interval... 2 word_Int

			pre_Seg$ = Get label of interval... 1 int-1
			pre_Seg$ = replace$(pre_Seg$, "0", "", 0)
			pre_Seg$ = replace$(pre_Seg$, "1", "", 0)
			pre_Seg$ = replace$(pre_Seg$, "2", "", 0)

			post_Seg$ = Get label of interval... 1 int+1
			post_Seg$ = replace$(post_Seg$, "0", "", 0)
			post_Seg$ = replace$(post_Seg$, "1", "", 0)
			post_Seg$ = replace$(post_Seg$, "2", "", 0)
			
			
			if length(replace$ (search_Pre_Context$, " ", "", 0)) > 0
				if index(search_Pre_Context$, " "+pre_Seg$+" ") == 0
					condition_met = 0
				endif
			endif

			if length(replace$ (search_Post_Context$, " ", "", 0)) > 0
				if index(search_Post_Context$, " "+post_Seg$+" ") == 0
					condition_met = 0
				endif
			endif

			if length(replace$ (stop_Pre_Context$, " ", "", 0)) > 0
				if index(stop_Pre_Context$, " "+pre_Seg$+" ") > 0
					condition_met = 0
				endif
			endif

			if length(replace$ (stop_Post_Context$, " ", "", 0)) > 0
				if index(stop_Post_Context$, " "+post_Seg$+" ") > 0
					condition_met = 0
				endif
			endif

			if length(replace$ (stop_Words$, " ", "", 0)) > 0
				if index(stop_Words$, " "+word$+" ") > 0
					condition_met = 0
				endif
			endif

			if condition_met == 1
				window_start = Get start point... 2 word_Int - 3
				window_end = Get end point... 2 word_Int + 3
				window_dur = window_end - window_start
				
				editor TextGrid 'file$'
				Zoom... window_start window_end
				Play window
		
				beginPause ("Is it accurate")
					word ("the word", word$)
					text ("td", "1")
					Play window
				endPause ("Continue", 1)
				endeditor
			endif
		endif
	endfor
endif

if end_Of_Word == 1 or start_Of_Word == 1
	word_Intervals = Get number of intervals... 2
	for int from 1 to word_Intervals
		word$ = Get label of interval... 2 int
		word_Start = Get start point... 2 int
		word_End = Get end point... 2 int
		
		if index(stop_Words$, " "+word$+" ") == 0
			if start_Of_Word == 1 
				ph_Int = Get interval at time... 1 word_Start + 0.005
				seg$ = Get label of interval... 1 ph_Int

				if index(search_Segments$, " "+seg$+" ") > 0
					condition_met = 1
			
					seg_Start = Get start point... 1 int
					seg_End = Get end point... 1 int
					seg_Dur = seg_End-seg_Start
					seg_Mid = seg_Start + (seg_Dur/2)

					pre_Seg$ = Get label of interval... 1 ph_Int-1
					pre_Seg$ = replace$(pre_Seg$, "0", "", 0)
					pre_Seg$ = replace$(pre_Seg$, "1", "", 0)
					pre_Seg$ = replace$(pre_Seg$, "2", "", 0)

					post_Seg$ = Get label of interval... 1 ph_Int+1
					post_Seg$ = replace$(post_Seg$, "0", "", 0)
					post_Seg$ = replace$(post_Seg$, "1", "", 0)
					post_Seg$ = replace$(post_Seg$, "2", "", 0)

					if length(replace$ (search_Pre_Context$, " ", "", 0)) > 0
						if index(search_Pre_Context$, " "+pre_Seg$+" ") == 0
			 				condition_met = 0
						endif
					endif

					if length(replace$ (search_Post_Context$, " ", "", 0)) > 0
						if index(search_Post_Context$, " "+post_Seg$+" ") == 0
							condition_met = 0
						endif
					endif

					if length(replace$ (stop_Pre_Context$, " ", "", 0)) > 0
						if index(stop_Pre_Context$, " "+pre_Seg$+" ") > 0
							condition_met = 0
						endif
					endif

					if length(replace$ (stop_Post_Context$, " ", "", 0)) > 0
						if index(stop_Post_Context$, " "+post_Seg$+" ") > 0
							condition_met = 0
						endif
					endif

					if condition_met == 1
						window_start = Get start point... 2 word_Int - 3
						window_end = Get end point... 2 word_Int + 3
						window_dur = window_end - window_start
				
						editor TextGrid 'file$'
						Zoom... window_start window_end
						Play window
		
						beginPause ("Is it accurate")
							word ("the word", word$)
							text ("td", "1")
							Play window
						endPause ("Continue", 1)
						endeditor
					endif		
				endif
			endif

			if end_Of_Word == 1
				ph_Int = Get interval at time... 1 word_End - 0.005
				seg$ = Get label of interval... 1 ph_Int

				if index(search_Segments$, " "+seg$+" ") > 0
					condition_met = 1
			
					seg_Start = Get start point... 1 int
					seg_End = Get end point... 1 int
					seg_Dur = seg_End-seg_Start
					seg_Mid = seg_Start + (seg_Dur/2)

					pre_Seg$ = Get label of interval... 1 ph_Int-1
					pre_Seg$ = replace$(pre_Seg$, "0", "", 0)
					pre_Seg$ = replace$(pre_Seg$, "1", "", 0)
					pre_Seg$ = replace$(pre_Seg$, "2", "", 0)

					post_Seg$ = Get label of interval... 1 ph_Int+1
					post_Seg$ = replace$(post_Seg$, "0", "", 0)
					post_Seg$ = replace$(post_Seg$, "1", "", 0)
					post_Seg$ = replace$(post_Seg$, "2", "", 0)

					if length(replace$ (search_Pre_Context$, " ", "", 0)) > 0
						if index(search_Pre_Context$, " "+pre_Seg$+" ") == 0
			 				condition_met = 0
						endif
					endif

					if length(replace$ (search_Post_Context$, " ", "", 0)) > 0
						if index(search_Post_Context$, " "+post_Seg$+" ") == 0
							condition_met = 0
						endif
					endif

					if length(replace$ (stop_Pre_Context$, " ", "", 0)) > 0
						if index(stop_Pre_Context$, " "+pre_Seg$+" ") > 0
							condition_met = 0
						endif
					endif

					if length(replace$ (stop_Post_Context$, " ", "", 0)) > 0
						if index(stop_Post_Context$, " "+post_Seg$+" ") > 0
							condition_met = 0
						endif
					endif

					if condition_met == 1
						window_start = Get start point... 2 int - 3
						window_end = Get end point... 2 int + 3
						window_dur = window_end - window_start
				
						editor TextGrid 'file$'
						Zoom... window_start window_end
						Play window
		
						beginPause ("Is it accurate")
							word ("the word", word$)
							text ("td", "1")
							Play window
						endPause ("Continue", 1)
						endeditor
					endif		
				endif
			endif
		endif
	endfor
endif




