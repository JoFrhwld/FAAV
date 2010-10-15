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
        F1 = float(line[3])
        F2 = float(line[4])
#        if line[5] != "":
#            F3 = float(line[5])
#        else
        B1 = math.log(float(line[6]))
        B2 = math.log(float(line[7]))
#        B3 = math.log(float(line[8]))
        Dur = math.log(float(line[12]))
        

    
        if vowel in vowels:
#            vowels[vowel].append([F1, F2,F3,  B1, B2, B3, Dur])
            vowels[vowel].append([F1, F2,  B1, B2, Dur])
        else:
#            vowels[vowel] = [[F1, F2, F3, B1, B2, B3, Dur]]
            vowels[vowel] = [[F1, F2, B1, B2, Dur]]

    sys.stderr.write("Vowel dictionary created\n")
    return vowels

def excludeOutliers(vowels, vowelMeans, vowelCovs):
    """
    Finds outliers and excludes them.
    """
    sys.stderr.write("Excluding outlying vowels...")
    outvowels = {}
    for vowel in vowels:
        ntokens = len(vowels[vowel])
        if ntokens >= 7:
            outlie = 4.75
            outvowels[vowel] = pruneVowels(vowels, vowel, vowelMeans, vowelCovs, outlie)
        else:
            outvowels[vowel] = vowels[vowel]
    sys.stderr.write("excluded.\n")
    return(outvowels)


def pruneVowels(vowels, vowel, vowelMeans, vowelCovs, outlie):
    """
    Tries to prune outlier vowels, making sure enough tokens are left to calculate mahalanobis distance.
    """
    enough = False
       
    while not enough:
        outtokens = [ ]
        for token in vowels[vowel]:
            x = robjects.FloatVector(token)
            dist = robjects.r['mahalanobis'](x, vowelMeans[vowel], vowelCovs[vowel])[0]
            if dist <= outlie:
                outtokens.append(token)
        if len(outtokens) >= 7:
            enough = True
        else:
            outlie = outlie + 0.5
    
    return(outtokens)
            
    
    



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
    #sys.stdout.write("\n\nCMUVowel\tVowel\tStress\tWord\tbeg\tend\tdur\tOriginalF1\tOriginalF2\tOriginalF3\tOriginalB1\tOriginalB2\tOriginalB3\tfm\tfp\tfv\tps\tfs\tF1\tF2\tlogB1\tlogB2\tlogDur\n")
    colnames = ["CMUVowel",
                "Vowel",
                "Stress",
                "Word",
                "t",
                "beg",
                "end",
                "dur",
                "OriginalF1",
                "OriginalF2",
                "OriginalF3",
                "OriginalB1",
                "OriginalB2",
                "OriginalB3",
                "dist",
                "cd",
                "fm",
                "fp",
                "fv",
                "ps",
                "fs",
                "style",
                "glide",
                "F1",
                "F2",
                "F3",
                "logB1",
                "logB2",
                "logB3",
                "logDur"
                ]
    colnamesstring = string.join(colnames, "\t")
    sys.stdout.write("\n\n"+colnamesstring+"\n")
    
    for line in lines:
        CMUvowel = line[0]
        vowel= line[vowelindex]
        stress = line[1]
        word = line[2]
        t = line[9]
        beg = line[10]
        end = line[11]
        Dur = line[12]
        F1orig = line[3]
        F2orig = line[4]
        F3orig = line[5]
        B1orig = line[6]
        B2orig = line[7]
        B3orig = line[8]
        lDur = math.log(float(Dur))
        
        poles = ast.literal_eval(line[21])
        bandwidths = ast.literal_eval(line[22])

        valuesList = []
        distanceList = []

        for i in range(len(poles)):
            if len(poles[i]) >= 2:
                F1 = poles[i][0]
                F2 = poles[i][1]
                if len(poles[i]) >= 3:
                    F3 = poles[i][2]
                else:
                    F3 = "NA"
                B1 = math.log(bandwidths[i][0])
                B2 = math.log(bandwidths[i][1])
                if len(bandwidths[i]) >= 3:
                    B3 = math.log(bandwidths[i][2])
                else:
                    B3 = "NA"

    
#                values = [F1, F2, F3, B1, B2, B3, lDur]
                values = [F1, F2, B1, B2, lDur]
                outvalues = [F1, F2, F3, B1, B2, B3, lDur]
    
                x = robjects.FloatVector(values)

                ##If there is only one member of a vowel category,
                ##the covariance matrix will be filled with NAs
                #sys.stderr.write(vowel+"\n")
                if vowel in vowelCovs:
                    if vowelCovs[vowel][0] is rinterface.NA_Real:
                        valuesList.append([float(F1orig), float(F2orig), float(F2orig), float(B1orig), float(B2orig), float(B3orig),lDur])
                        distanceList.append(0)
                    else:
                        dist = robjects.r['mahalanobis' ](x, vowelMeans[vowel], vowelCovs[vowel])[0]
    
                        valuesList.append(outvalues)
                        distanceList.append(dist)
                else:
                    valuesList.append([float(F1orig), float(F2orig), float(F2orig), float(B1orig), float(B2orig), float(B3orig),lDur])
                    distanceList.append(0)

        winnerIndex = distanceList.index(min(distanceList))
        dist = repr(min(distanceList))
        bestValues = valuesList[winnerIndex]
        bestValuesString = [repr(x) for x in bestValues]

        info = [CMUvowel, vowel, stress, word, t, beg, end, Dur, F1orig, F2orig, F3orig,B1orig, B2orig, B3orig, dist, string.join(line[13:21], "\t")]
        infoLine = string.join(info, "\t")
        valuesLine = string.join(bestValuesString, "\t")
        

        sys.stdout.write(infoLine+"\t")
        sys.stdout.write(valuesLine+"\n")
    sys.stderr.write("Done!\n")


## Main Program Starts Here
#Define some constants
#file = "/Users/joseffruehwald/Documents/Classes/Fall_10/misc/FAAV/extractFormants_modified/PH06-2-1-AB-Jean.formants"
file = sys.argv[1]
vowelindex = 13

lines = loadfile(file)
vowels = createVowelDictionary(lines, vowelindex)
vowelMeans, vowelCovs = calculateVowelMeans(vowels)


invowels = excludeOutliers(vowels, vowelMeans, vowelCovs)
vowelMeans, vowelCovs = calculateVowelMeans(invowels)

repredictF1F2(lines, vowelindex, vowelMeans, vowelCovs)
