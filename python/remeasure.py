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

    
    if line[0] in vowels:
        vowels[line[0]].append([F1, F2, B1, B2, Dur])
    else:
        vowels[line[0]] = [[F1, F2, B1, B2, Dur]]
        

    

#poles = ast.literal_eval(line2[20])
#bandwidths = ast.literal_eval(line2[21])


