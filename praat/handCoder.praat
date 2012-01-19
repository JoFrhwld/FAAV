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
##    Minor Additions by Jordan Kodner, 2012
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
	comment File Settings
	word file speaker
	word outfile outfile.txt
	comment Segments to Search For
	sentence Search_Segments T, D, ER0 AW1 N, B AH1 N, D OW1 N, K UH1 D AH0 N, D IH1 D AH0 N, D AH1 Z AH0 N, D OW1 N, HH AE1 D AH0 N, HH AE1 V AH0 N, IH1 Z AH0 N, L AE1 S, M OW1 S, N EH1 K S, P L EY1 G R AW2 N, R AH1 N AH0 R AW2 N, S EH1 K AH0 N, TH AW1 Z AH0 N             
	comment Word context
	optionmenu Context: 1
		option End of word
		option Start of word
		option Word internal
		option Internal and End of word
		option Internal and Start of word
		option Start and End of word
		option All contexts
	#boolean End_Of_Word 1
	#boolean Start_Of_Word 0
	#boolean Word_Internal 0 
	comment Search Context
	sentence Search_Pre_Context consonant
	sentence Search_Post_Context
	sentence Word_String_Search
	comment Exclusion Contexts
	sentence Stop_Pre_Context R ER
	sentence Stop_Post_Context T D TH DH CH JH
	sentence Stop_Words AND
	comment Extra Settings
	positive Window_Size 3
	sentence Default_Code1
	sentence Default_Code2
	real Start_Time 0 
	boolean Play_on_Continue 0
endform

end_Of_Word = 0
start_Of_Word = 0
word_Internal = 0

if context == 1
	end_Of_Word = 1
elsif context == 2
	start_Of_Word = 1
elsif context == 3
	word_Internal = 1
elsif context == 4
	word_Internal = 1
	end_Of_Word = 1
elsif context == 5
	word_Internal = 1
	start_Of_Word = 1
elsif context == 6
	start_Of_Word = 1
	end_Of_Word = 1
elseif context == 7
	end_Of_Word = 1
	start_Of_Word = 1
	word_Internal = 1
endif

#
#creates array of search strings named search_array$
#length of array is num_search_segs
#creates array of lengths of search strings search_lens
#arrays indexed from 0
search_Segments$ = " " + replace_regex$ (search_Segments$, ",", " , ", 1000) + " , "
search_Segments$ = replace_regex$ (search_Segments$, " +", " ", 1000)
#search_Segments$ = replace_regex$ (search_Segments$, "\d", "", 1000)

x = index(search_Segments$, ",")
i = 0
while x > 0 && i < 15
	search_array'i'$ = left$ (search_Segments$, index(search_Segments$, ",")-1)
	len = length(search_array'i'$)
	if len == 3
		search_lens'i' = 1
	else
		pr$ = replace$ (search_array'i'$, " ", "", 0)
		search_lens'i' = length(search_array'i'$) - length(pr$) - 1
	endif
	search_Segments$ = right$ (search_Segments$, length(search_Segments$) - index(search_Segments$, ","))
	i = i + 1
	x = index(search_Segments$, ",")
endwhile
num_search_segs = i-1


#log_file = file$ + ".log"

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

if start_Time == 0
	fileappend 'outfile$'	File	Segment	Position	Code1	Code2	Seg_Start	Seg_End	Word	Word_Start	Word_End	Pre_Seg	Pre_Seg_Start	Pre_Seg_End	Post_Seg	Post_Seg_Start	Post_Seg_End	Window	Vowels_per_Second	Comments	Warnings'newline$'
endif

		word_Intervals = Get number of intervals... 2
		start_Interval = Get interval at time... 2 start_Time
		for int from start_Interval to word_Intervals
			word$ = Get label of interval... 2 int
			word_Start = Get start point... 2 int
			word_End = Get end point... 2 int
		
			if index(stop_Words$, " "+word$+" ") == 0
				ph_First_Int = Get interval at time... 1 word_Start + 0.005
				ph_Last_Int = Get interval at time... 1 word_End - 0.005

				#
				# gets Arpabet transcription of word arpa$
				arpa$ = ""
				for ph_Int from ph_First_Int to ph_Last_Int
					seg$ = Get label of interval... 1 ph_Int
					arpa$ = arpa$ + seg$ + " "
				endfor
				#arpa$ = replace_regex$ (arpa$, "\d", "", 0)

				for ph_Int from ph_First_Int to ph_Last_Int

					seg$ = Get label of interval... 1 ph_Int

					#
					#checks whether this word contains search terms
					#condition_met: ~(whether a search segment was found)
					#found_len: length of search segment matched
					#found_index: index of search segment matched in search_array$
					condition_met = 1
					found_len = 0
					found_index = 0
					arpa$ = " " + arpa$

					for i from 0 to num_search_segs
						if index_regex (arpa$, search_array'i'$) == 1
							condition_met = 0
							found_len = search_lens'i'
							found_index = i
						endif
					endfor
					arpa$ = right$ (arpa$, length(arpa$) -1)
					arpa$ = right$ (arpa$, length(arpa$) - index(arpa$, " "))

					if condition_met = 0
				
						seg_Start = Get start point... 1 ph_Int
						seg_End = Get end point... 1 ph_Int
						seg_Dur = seg_End-seg_Start
						seg_Mid = seg_Start + (seg_Dur/2)

						if ph_Int > 1
							pre_Seg$ = Get label of interval... 1 ph_Int-1
						else
							pre_Seg$ = "none"
						endif
						pre_Seg$ = replace$(pre_Seg$, "0", "", 0)
						pre_Seg$ = replace$(pre_Seg$, "1", "", 0)
						pre_Seg$ = replace$(pre_Seg$, "2", "", 0)

						post_Seg$ = Get label of interval... 1 ph_Int+1
						post_Seg$ = replace$(post_Seg$, "0", "", 0)
						post_Seg$ = replace$(post_Seg$, "1", "", 0)
						post_Seg$ = replace$(post_Seg$, "2", "", 0)

						location$ = ""

						if end_Of_Word == 1 and ph_Int + found_len -1 == ph_Last_Int
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

						if length(replace$ (search_Pre_Context$, " ", "", 0)) > 0 and found_len == 1
							if index(search_Pre_Context$, " "+pre_Seg$+" ") == 0
				 				condition_met = 0
							endif
						endif

						if length(replace$ (search_Post_Context$, " ", "", 0)) > 0 and found_len == 1
							if index(search_Post_Context$, " "+post_Seg$+" ") == 0
								condition_met = 0
							endif
						endif

						if length(replace$ (stop_Pre_Context$, " ", "", 0)) > 0 and found_len == 1
							if index(stop_Pre_Context$, " "+pre_Seg$+" ") > 0
								condition_met = 0
							endif
						endif

						if length(replace$ (stop_Post_Context$, " ", "", 0)) > 0 and found_len == 1
							if index(stop_Post_Context$, " "+post_Seg$+" ") > 0
								condition_met = 0
							endif
						endif

						if condition_met == 1
							window_Start = Get start point... 2 max(1,int - window_Size)
							window_End = Get end point... 2 min(int + window_Size, word_Intervals)
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
							Zoom... max(1,window_Start) min(window_End, word_Intervals)
							if play_on_Continue = 1
								Play window
							endif
							coded = 0
							
							while coded == 0
							beginPause ("Code it")
								comment("'word$' 'location$'")
								comment("Code 1")
								text ("code1", default_Code1$)
								comment("Code 2")
								text ("code2", default_Code1$)
								comment("Comments")
								text ("comment", "")
								comment("Preceding Segment")
								text("Preceding_Segment", pre_Seg$)
								comment("Following Segment")
								text("Following_Segment", post_Seg$)
								comment("Reject this token?")
								boolean("Reject", 0)
							#	Play window
							click = endPause ("Play", "Continue", 1)
							if click == 1
								Play window
							else
								coded = 1
							endif
							endwhile
							endeditor
							warning$ = ""
							if preceding_Segment$ <> pre_Seg$
								warning$ = "PreSeg Changed"
								pre_Seg$ = preceding_Segment$
							endif
							if following_Segment$ <> post_Seg$
								warning$ = "PostSeg Changed"
								post_Seg$ = following_Segment$
							endif
							if reject ==0
								fileappend 'outfile$' 'file$'	'seg$'	'location$'	'code1$'	'code2$'	'seg_Start:3'	'seg_End:3'	'word$'	'word_Start:3'	'word_End:3'	'pre_Seg$'	'pre_Seg_Start:3'	'pre_Seg_End:3'	'post_Seg$'	'post_Seg_Start:3'	'post_Seg_End:3'	'real_Dur:3'	'vowels_Per_Second:3'	'comment$'	'warning$''newline$'
							endif
						endif		
					endif
				endfor
			endif
		endfor