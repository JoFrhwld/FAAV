import ast
import math
import rpy2.robjects as robjects
import sys
import string

file = "/Users/joseffruehwald/Documents/Classes/Fall_10/misc/FAAV/extractFormants_modified/PH06-2-1-AB-Jean.formants"
f = open(file)
sys.stdout.write(f.readline())
f.readline()
f.readline()
sys.stderr.write("Reading file...")
lines = f.readlines()
f.close()
sys.stderr.write("File read\n")





vowels = {}

lines = [line.rstrip().split("\t") for line in lines]

sys.stderr.write("Creating vowel dictionary...")

for line in lines:
    vowel = line[0]
    F1 = float(line[4])
    F2 = float(line[5])
    B1 = math.log1p(float(line[7]))
    B2 = math.log1p(float(line[8]))
    Dur = math.log1p(float(line[13]))

    
    if vowel in vowels:
        vowels[vowel].append([F1, F2, B1, B2, Dur])
    else:
        vowels[vowel] = [[F1, F2, B1, B2, Dur]]

sys.stderr.write("Vowel dictionary created\n")

sys.stderr.write("Calculating vowel means...")
vowelMeans = {}
vowelCovs = {}
for vowel in vowels:
    vF1 = robjects.FloatVector([F1 for [F1,F2,B1,B2,Dur] in vowels[vowel]])
    vF2 = robjects.FloatVector([F2 for [F1,F2,B1,B2,Dur] in vowels[vowel]])
    vB1 = robjects.FloatVector([B1 for [F1,F2,B1,B2,Dur] in vowels[vowel]])
    vB2 = robjects.FloatVector([B2 for [F1,F2,B1,B2,Dur] in vowels[vowel]])
    vDur = robjects.FloatVector([Dur for [F1,F2,B1,B2,Dur] in vowels[vowel]])

    rcolMeans = robjects.r["colMeans"]
    rcov = robjects.r["cov"]

    measureMatrix = robjects.r["matrix"](vF1 + vF2 + vB1 + vB2 + vDur, ncol = 5)
    
    vowelMeans[vowel] = rcolMeans(measureMatrix)
    vowelCovs[vowel] = rcov(measureMatrix)
sys.stderr.write("Vowel means calculated\n")


sys.stderr.write("Finding best measurements...")
sys.stdout.write("\n\nVowel\tStress\tWord\tbeg\tend\tdur\tOriginalF1\tOriginalF2\tF1\tF2\tlogB1\tlogB2\tlogDur\n")
for line in lines:
    vowel = line[0]
    stress = line[1]
    word = line[3]
    beg = line[11]
    end = line[12]
    Dur = line[13]
    F1orig = line[4]
    F2orig = line[5]
    lDur = math.log(float(Dur))
    poles = ast.literal_eval(line[20])
    bandwidths = ast.literal_eval(line[21])

    valuesList = []
    distanceList = []

    for i in range(len(poles)):
        for j in range(len(poles[i])):
            if len(poles[i][j]) >= 2:
                F1 = poles[i][j][0]
                F2 = poles[i][j][1]
                B1 = math.log1p(bandwidths[i][j][0])
                B2 = math.log1p(bandwidths[i][j][0])
    
                values = [F1, F2, B1, B2, lDur]
    
                x = robjects.FloatVector(values)

                dist = robjects.r['mahalanobis' ](x, vowelMeans[vowel], vowelCovs[vowel])[0]

                valuesList.append(values)
                distanceList.append(dist)

    winnerIndex = distanceList.index(min(distanceList))
    bestValues = valuesList[winnerIndex]
    bestValuesString = [repr(x) for x in bestValues]

    info = [vowel, stress, word, beg, end, Dur, F1orig, F2orig]
    infoLine = string.join(info, "\t")
    valuesLine = string.join(bestValuesString, "\t")

    sys.stdout.write(infoLine+"\t")
    sys.stdout.write(valuesLine+"\n")
    
    

            
    


