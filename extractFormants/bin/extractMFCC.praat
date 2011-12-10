# Usage:  praat extractMFCC.praat filename.wav nCoefs windowLength timeStep

form Get_arguments
  word audioFile
  real windowLength
endform

# get the number of characters in the file name
flen = length(audioFile$)
# cut off the final '.wav' (or other three-character file extension) to get the full path of the .Formant file that we will create
path$ = left$ (audioFile$, flen-4)

Read from file... 'audioFile$'

To MFCC... 12 'windowLength' 0.005 100 100 0

Write to short text file... 'path$'.MFCC