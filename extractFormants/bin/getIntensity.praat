## Praat script for getting the intensity contour for a given sound file
## written by Ingrid Rosenfelder
## last modified July 23, 2010

## Usage:  praat getIntensity.praat filename.wav

form Please specify the sound file:
  sentence audioFile
endform

filename$ = audioFile$ - ".wav" + ".Intensity"

Read from file... 'audioFile$'
To Intensity... 100 0.001 yes
Write to short text file... 'filename$'