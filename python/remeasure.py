file = "/Users/joseffruehwald/Documents/Classes/Fall_10/misc/FAAV/extractFormants_modified/PH06-2-1-AB-Jean.formants"
f = open(file)
l = f.readline()
l = f.readline()
l = f.readline()
print("Reading file...")
lines = f.readlines()
f.close()
print("File read")



import ast
import math
import rpy2

vowels = {}

for line in lines:
    line = line.rstrip()
    line = line.split("\t")
    F1 = float(line[4])
    F2 = float(line[5])
    B1 = float(line[7])
    B2 = float(line[8])
    Dur = math.log1p(float(line[13]))

    print(line[0])
    print([F1, F2, B1, B2, Dur])
    print(line[0] in vowels)
    if line[0] in vowels:
        vowels[line[0]] = vowels[line[0]].append([F1, F2, B1, B2, Dur])
    else:
        vowels[line[0]] = [[F1, F2, B1, B2, Dur]]
        

    ## right now returns error
    ## Traceback (most recent call last):
      #File "/Users/joseffruehwald/Documents/Classes/Fall_10/FAAV/python/remeasure.py", line 32, in <module>
    #vowels[line[0]] = vowels[line[0]].append([F1, F2, B1, B2, Dur])
    #AttributeError: 'NoneType' object has no attribute 'append'
    #
    #For some reason, the first IY and AY have None for values.

#poles = ast.literal_eval(line2[20])
#bandwidths = ast.literal_eval(line2[21])


