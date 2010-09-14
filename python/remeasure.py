import ast
import math
import rpy2.robjects as robjects
import rpy2.rinterface as rinterface
import sys
import string


def loadfile(file):
    """
    Loads an extractFormants file. Returns formatted list of lists.
    """
    f = open(file)
    sys.stdout.write(f.readline())
    f.readline()
    f.readline()
    sys.stderr.write("Reading file...")
    lines = f.readlines()
    f.close()
    lines = [line.rstrip().split("\t") for line in lines]
    sys.stderr.write("File read\n")
    return lines


def createVowelDictionary(lines, vowelindex):
    """
    Creates a dictionary of F1, F2, B1, B3 and Duration observations by vowel type.
    vowel index indicates the index in lines[x] which should be taken as identifying vowel categories.
    """
    vowels = {}
    sys.stderr.write("Creating vowel dictionary...")

    for line in lines:
        vowel = line[vowelindex]
        F1 = float(line[4])
        F2 = float(line[5])
        B1 = math.log(float(line[7]))
        B2 = math.log(float(line[8]))
        Dur = math.log(float(line[13]))

    
        if vowel in vowels:
            vowels[vowel].append([F1, F2, B1, B2, Dur])
        else:
            vowels[vowel] = [[F1, F2, B1, B2, Dur]]

    sys.stderr.write("Vowel dictionary created\n")
    return vowels

def calculateVowelMeans(vowels):
    """
    calculates [means] and [covariance matrices] for each vowel class.
    It returns these as R objects in dictionaries indexed by the vowel class.
    """
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
    return vowelMeans, vowelCovs


def repredictF1F2(lines,vowelindex, vowelMeans, vowelCovs):
    """
    Predicts F1 and F2 from the speaker's own vowel distributions based on the mahalanobis distance.
    """
    sys.stderr.write("Finding best measurements...")
    sys.stdout.write("\n\nCMUVowel\tVowel\tStress\tWord\tbeg\tend\tdur\tOriginalF1\tOriginalF2\tfm\tfp\tfv\tps\tfs\tF1\tF2\tlogB1\tlogB2\tlogDur\n")
    for line in lines:
        CMUvowel = line[0]
        vowel= line[vowelindex]
        stress = line[1]
        word = line[3]
        beg = line[11]
        end = line[12]
        Dur = line[13]
        F1orig = line[4]
        F2orig = line[5]
        B1orig = line[7]
        B2orig = line[8]
        lDur = math.log(float(Dur))
        
        poles = ast.literal_eval(line[20])
        bandwidths = ast.literal_eval(line[21])

        valuesList = []
        distanceList = []

        for i in range(len(poles)):
            ## only consider measurement at 1/3 through
            j = len(poles[i])/3
            if len(poles[i][j]) >= 2:
                F1 = poles[i][j][0]
                F2 = poles[i][j][1]
                B1 = math.log(bandwidths[i][j][0])
                B2 = math.log(bandwidths[i][j][0])
    
                values = [F1, F2, B1, B2, lDur]
    
                x = robjects.FloatVector(values)

                #If there is only one member of a vowel category,
                #the covariance matrix will be filled with NAs
                if vowelCovs[vowel][0] is rinterface.NA_Real:
                    valuesList.append([float(F1orig), float(F2orig), float(B1orig), float(B2orig), lDur])
                    distanceList.append(0)
                else:
                    dist = robjects.r['mahalanobis' ](x, vowelMeans[vowel], vowelCovs[vowel])[0]
    
                    valuesList.append(values)
                    distanceList.append(dist)

        winnerIndex = distanceList.index(min(distanceList))
        bestValues = valuesList[winnerIndex]
        bestValuesString = [repr(x) for x in bestValues]

        info = [CMUvowel, vowel, stress, word, beg, end, Dur, F1orig, F2orig, string.join(line[15:20], "\t")]
        infoLine = string.join(info, "\t")
        valuesLine = string.join(bestValuesString, "\t")
        

        sys.stdout.write(infoLine+"\t")
        sys.stdout.write(valuesLine+"\n")
    sys.stderr.write("Done!\n   ")


## Main Program Starts Here
#Define some constants
file = "/Users/joseffruehwald/Documents/Classes/Fall_10/misc/FAAV/extractFormants_modified/PH06-2-1-AB-Jean.formants"
vowelindex = 14

lines = loadfile(file)
vowels = createVowelDictionary(lines, vowelindex)
vowelMeans, vowelCovs = calculateVowelMeans(vowels)

repredictF1F2(lines, vowelindex, vowelMeans, vowelCovs)

    


