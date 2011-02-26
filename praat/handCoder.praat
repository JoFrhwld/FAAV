############################################################
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
##    Copyright 2011, Josef Fruehwald
###########################################################

######################################################################################################	
##	Usage:
##		Setup
##			-- Load a long sound file and a P2FA text grid.
##			     These should be called the same thing in the objects list.
##			-- Open this script and select Run > Run
##			-- Define the segments and contexts you want to search for.
##			     Enter lists of segments separated by spaces in the context fields, or alternatively,
##			     enter "consonant" or "vowel"
##		Coding
##			-- An x-word window (default 3, defined buy Window_Size) on each side of the word of interest will play twice. 
##			     You can adjust the window context and replay it within the editor, but this will require juggling
##			     between the coding window and the editor window, and will slow down your workflow.
##			-- You can enter any text into the coding field. If you are going to code multiple things, I suggest
##			     using some kind of character delimiter between codes. Use the comment field for comments to yourself.
##		Output
##			-- The output will be a tab delimited file including the following pieces of data:
##				* Object name
##				* Segment of focus
##				* Word position of the segment
##				* Code from the coding field
##				* Time of segment start
##				* Time of segment end
##				* Time of segment end
##				* Word of focus
##				* Word start
##				* Word end
##				* Preceding segment
##				* Preceding segment start
##				* Preceding segment end
##				* Window duration
##				* Vowels per second in the window
##				* Comments
######################################################################################################		



form Search Settings
	word file carterDNC1976_5
	word outfile outfile.txt
	sentence Search_Segments R ER0 ER1 ER2
	comment Word context
	boolean End_Of_Word 1
	boolean Start_Of_Word 0
	boolean Word_Internal 0
	sentence Search_Pre_Context 
	sentence Search_Post_Context
	sentence Stop_Pre_Context 
	sentence Stop_Post_Context 
	sentence Stop_Words
	positive Window_Size 3
	sentence Default_Code  
endform

#log_file = file$ + ".log"

search_Segments$ = " "+search_Segments$+" "

vowel$ = " AA AE AH AO AW AX AY EH EY IH IY OW OY UH UW "
consonant$ = " B CH DH DX AXR EL EM EN ER F G HH HV JH K L M N NX NG P R S SH T TH V W Y Z ZH "

if index(search_Pre_Context$,"vowel") > 0
	search_Pre_Context$ = vowel$
elsif index(search_Pre_Context$, "consonant") > 0
	search_Pre_Context$ = consonant$
else
	search_Pre_Context$ = " "+search_Pre_Context$+" "
endif

if index(search_Post_Context$,"vowel") > 0
	search_Post_Context$ = vowel$
elsif index(search_Post_Context$ ,"consonant") > 0
	search_Post_Context$ = consonant$
else
	search_Post_Context$ = " "+search_Post_Context$+" "
endif

if index(stop_Pre_Context$, "vowel") >0
	stop_Pre_Context$ = vowel$
elsif index(stop_Pre_Context$ ,"consonant") >0
	stop_Pre_Context$ = consonant$
else
	stop_Pre_Context$ = " "+stop_Pre_Context$+" "
endif

if index(stop_Post_Context$, "vowel") > 0
	stop_Post_Context$ = vowel$
elsif index(stop_Post_Context$, "consonant") > 0
	stop_Post_Context$ = consonant$
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


fileappend 'outfile$'	File	Segment	Position	Code		Seg_Start	Seg_End	Word	Word_Start	Word_End	Pre_Seg	Pre_Seg_Start	Pre_Seg_End	Post_Seg	Post_Seg_Start	Post_Seg_End	Window	Vowels_per_Second	Comments'newline$'

		word_Intervals = Get number of intervals... 2
		for int from 1 to word_Intervals
			word$ = Get label of interval... 2 int
			word_Start = Get start point... 2 int
			word_End = Get end point... 2 int
		
			if index(stop_Words$, " "+word$+" ") == 0
				ph_First_Int = Get interval at time... 1 word_Start + 0.005
				ph_Last_Int = Get interval at time... 1 word_End - 0.005
				for ph_Int from ph_First_Int to ph_Last_Int

					seg$ = Get label of interval... 1 ph_Int

					if index(search_Segments$, " "+seg$+" ") > 0
						condition_met = 0
				
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

						location$ = ""

						if end_Of_Word == 1 and ph_Int  == ph_Last_Int
							condition_met = 1
							location$ = "End"
						endif

						if start_Of_Word == 1 and ph_Int == ph_First_Int
							condition_met = 1
							location$ = "Start"
						endif

						if word_Internal == 1 and ph_Int <> ph_First_Int and ph_Int <> ph_Last_Int
								condition_met = 1
								location$ = "Internal"
						endif

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
							window_Start = Get start point... 2 int - window_Size
							window_End = Get end point... 2 int + window_Size
							window_Dur = window_End - window_Start
				

							firstPhInt = Get interval at time... 1 window_Start+0.005
							lastPhInt = Get interval at time... 1 window_End-0.005

							nval = 0
							sp_Dur = 0
							for ph from firstPhInt to lastPhInt
								phLabel$ = Get label of interval... 1 ph
								if endsWith (phLabel$, "0") or endsWith (phLabel$, "1") or endsWith (phLabel$, "2")
									nval = nval + 1
								elsif phLabel$ = "sp"
									ph_Start = Get start point... 1 ph
									ph_End = Get end point... 1 ph
									spDur = sp_Dur + (ph_End - ph_Start)
								endif
							endfor
							real_Dur = window_Dur - sp_Dur
							vowels_Per_Second = nval / (window_Dur - sp_Dur)
				
							pre_Seg_Start = Get start point... 1 ph_Int-1
							pre_Seg_End = Get end point... 1 ph_Int-1
							pre_Seg_Dur = pre_Seg_End - pre_Seg_Start

							post_Seg_Start = Get start point... 1 ph_Int+1
							post_Seg_End = Get end point... 1 ph_Int+1
							post_Seg_Dur = post_Seg_End - post_Seg_Start

							editor TextGrid 'file$'
							Zoom... window_Start window_End
							Play window
			
							beginPause ("Code it")
								comment("'word$' 'location$'")
								comment("Code")
								text ("code", default_Code$)
								comment("Comments")
								text ("comment", "")
								Play window
							endPause ("Continue", 1)
							endeditor
							fileappend 'outfile$' 'file$'	'seg$'	'location$'	'code$'	'seg_Start:3'	'seg_End:3'	'word$'	'word_Start:3'	'word_End:3'	'pre_Seg$'	'pre_Seg_Start:3'	'pre_Seg_End:3'	'post_Seg$'	'post_Seg_Start:3'	'post_Seg_End:3'	'real_Dur:3'	'vowels_Per_Second:3'	'comment$''newline$'

						endif		
					endif
				endfor
			endif
		endfor