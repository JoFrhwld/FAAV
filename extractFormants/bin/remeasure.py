#import ast
import math
import rpy2.robjects as robjects
import rpy2.rinterface as rinterface
import sys
import string

class VowelMeasurement:
    """represents a vowel measurement"""
    ## !!! not the same as class plotnik.VowelMeasurement !!!
    phone = ''          ## Arpabet coding
    stress = ''         ## stress level ("1", "2", "0")
    style = ''          ## style label (if present)
    word = ''           ## corresponding word
    f1 = None           ## first formant
    f2 = None           ## second formant
    f3 = None           ## third formant
    b1 = None           ## bandwidth of first formant
    b2 = None           ## bandwidth of second formant
    b3 = None           ## bandwidth of third formant
    t = ''              ## time of measurement
    code = ''           ## Plotnik vowel code ("xx.xxxxx")
    cd = ''             ## Plotnik code for vowel class
    fm = ''             ## Plotnik code for manner of following segment
    fp = ''             ## Plotnik code for place of following segment
    fv = ''             ## Plotnik code for voicing of following segment
    ps = ''             ## Plotnik code for preceding segment
    fs = ''             ## Plotnik code for following sequences
    text = ''           ## ???
    beg = None          ## beginning of vowel
    end = None          ## end of vowel
    dur = None          ## duration of vowel
    poles = []          ## original list of poles returned by LPC analysis
    bandwidths = []     ## original list of bandwidths returned by LPC analysis
    nFormants = None    ## actual formant settings used in the measurement (for Mahalanobis distance method)
    glide = ''          ## Plotnik glide coding


def loadfile(file):
    """
    Loads an extractFormants file. Returns formatted list of lists.
    """
    f = open(file)
    sys.stdout.write(f.readline())
    f.readline()
    f.readline()
    #sys.stderr.write("Reading file...")
    lines = f.readlines()
    f.close()
    lines = [line.rstrip().split("\t") for line in lines]
    measurements = []
    for line in lines:
        vm = VowelMeasurement()
        vm.cd = line[vowelindex]
        vm.f1 = float(line[3])
        vm.f2 = float(line[4])
        if line[5] != "":
            vm.f3 = float(line[5])
        vm.b1 = float(line[6])
        vm.b2 = float(line[7])
        if line[8] != "":
            vm.b3 = float(line[8])
        vm.dur = float(line[12])
        vm.phone = line[0]
        vm.stress = line[1]
        vm.word = line[2]
        vm.t = line[9]
        vm.beg = line[10]
        vm.end = line[11]       
        vm.poles = [[float(y) for y in x.rstrip(']').lstrip('[').split(',')] for x in line[22].split('],[')]
        vm.bandwidths = [[float(y) for y in x.rstrip(']').lstrip('[').split(',')] for x in line[23].split('],[')]
        measurements.append(vm) 
    #sys.stderr.write("File read\n")
    return measurements


def createVowelDictionary(measurements):
    """
    Creates a dictionary of F1, F2, B1, B3 and Duration observations by vowel type.
    vowel index indicates the index in lines[x] which should be taken as identifying vowel categories.
    """
    vowels = {}
    #sys.stderr.write("Creating vowel dictionary...")

    for vm in measurements:        
        if vm.cd in vowels:
#            vowels[vowel].append([F1, F2,F3,  B1, B2, B3, Dur])
            vowels[vm.cd].append([vm.f1, vm.f2,  math.log(vm.b1), math.log(vm.b2), math.log(vm.dur)])
        else:
#            vowels[vowel] = [[F1, F2, F3, B1, B2, B3, Dur]]
            vowels[vm.cd] = [[vm.f1, vm.f2,  math.log(vm.b1), math.log(vm.b2), math.log(vm.dur)]]

    #sys.stderr.write("Vowel dictionary created\n")
    return vowels

def excludeOutliers(vowels, vowelMeans, vowelCovs):
    """
    Finds outliers and excludes them.
    """
    #sys.stderr.write("Excluding outlying vowels...")
    outvowels = {}
    for vowel in vowels:
        ntokens = len(vowels[vowel])
        if ntokens >= 10:
            outlie = 4.75
            outvowels[vowel] = pruneVowels(vowels, vowel, vowelMeans, vowelCovs, outlie)
        else:
            outvowels[vowel] = vowels[vowel]
    #sys.stderr.write("excluded.\n")
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
        if len(outtokens) >= 10:
            enough = True
        else:
            outlie = outlie + 0.5
    
    return(outtokens)
            
    
    



def calculateVowelMeans(vowels):
    """
    calculates [means] and [covariance matrices] for each vowel class.
    It returns these as R objects in dictionaries indexed by the vowel class.
    """
    #sys.stderr.write("Calculating vowel means...")
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
    #sys.stderr.write("Vowel means calculated\n")
    return vowelMeans, vowelCovs





    

def repredictF1F2(measurements, vowelMeans, vowelCovs, vowels):
    """
    Predicts F1 and F2 from the speaker's own vowel distributions based on the mahalanobis distance.
    """
    remeasurements = []
    for vm in measurements:


        valuesList = []
        distanceList = []
        nFormantsList = []
        vowel = vm.cd

        
        for i in range(len(vm.poles)):

            if len(vm.poles[i]) >= 2:
                F1 = vm.poles[i][0]
                F2 = vm.poles[i][1]
                if len(vm.poles[i]) >= 3:
                    F3 = vm.poles[i][2]
                else:
                    F3 = "NA"
                B1 = math.log(vm.bandwidths[i][0])
                B2 = math.log(vm.bandwidths[i][1])
                if len(vm.bandwidths[i]) >= 3:
                    B3 = vm.bandwidths[i][2]
                else:
                    B3 = "NA"
                
                ##nFormants = len(vm.poles[i])
                lDur = math.log(vm.dur)
#                values = [F1, F2, F3, B1, B2, B3, lDur]
                values = [F1, F2, B1, B2, lDur]
                outvalues = [F1, F2, F3, B1, B2, B3, lDur]
    
                x = robjects.FloatVector(values)
               

                ##If there is only one member of a vowel category,
                ##the covariance matrix will be filled with NAs
                #sys.stderr.write(vowel+"\n")

                if vowel in vowelCovs:

                    if vowelCovs[vowel][0] is rinterface.NA_Real:
                        valuesList.append([float(vm.f1), float(vm.f2), vm.f3, math.log(float(vm.b1)), math.log(float(vm.b2)), vm.b3, lDur])
                        distanceList.append(0)
                        nFormantsList.append(i + 3)  ## these are the formant settings used, not the actual number of formants returned!
                    elif len(vowels[vowel]) < 7:
                        valuesList.append([float(vm.f1), float(vm.f2), vm.f3, math.log(float(vm.b1)), math.log(float(vm.b2)), vm.b3, lDur])
                        distanceList.append(0)
                        nFormantsList.append(i + 3)
                    else:  
                        dist = robjects.r['mahalanobis' ](x, vowelMeans[vowel], vowelCovs[vowel])[0]   
                        valuesList.append(outvalues)
                        distanceList.append(dist)
                        nFormantsList.append(i + 3)
                else:
                    valuesList.append([float(vm.f1), float(vm.f2), float(vm.f3), math.log(float(vm.b1)), math.log(float(vm.b2)), vm.b3,lDur])
                    distanceList.append(0)
                    nFormantsList.append(i + 3)

        winnerIndex = distanceList.index(min(distanceList))
        dist = repr(min(distanceList))
        bestValues = valuesList[winnerIndex]
        bestnFormants = nFormantsList[winnerIndex]
        ## change formants and bandwidths to new values
        vm.f1 = round(bestValues[0], 1)
        vm.f2 = round(bestValues[1], 1)
        if bestValues[2] != "NA":
            vm.f3 = round(bestValues[2], 1)
        else:
            vm.f3 = ''
        vm.b1 = round(math.exp(bestValues[3]), 1)
        vm.b2 = round(math.exp(bestValues[4]), 1)
        if bestValues[5] != "NA":
            try:
                vm.b3 = round(bestValues[5], 1)
            except OverflowError:
                vm.b3 = ''
        else:
            vm.b3 = ''
        vm.nFormants = bestnFormants
        remeasurements.append(vm)
        
    return remeasurements


def output(remeasurements):
    """writes measurements to file according to selected output format"""
    fw = open("remeasure.txt", 'w')
    # header
    fw.write('\t'.join(['vowel', 'stress', 'word', 'F1', 'F2', 'F3', 'B1', 'B2', 'B3', 't', 'beg', 'end', 'dur', 'cd', 'fm', 'fp', 'fv', 'ps', 'fs', 'style', 'glide', 'nFormants', 'poles', 'bandwidths']))
    fw.write('\n')
    for vm in measurements:
        fw.write('\t'.join([vm.phone, str(vm.stress), vm.word, str(vm.f1), str(vm.f2)]))    ## vowel (ARPABET coding), stress, word, F1, F2
        fw.write('\t')
        if vm.f3:
            fw.write(str(vm.f3))                                                            ## F3 (if present)
        fw.write('\t')
        fw.write('\t'.join([str(vm.b1), str(vm.b2)]))                                       ## B1, B2
        fw.write('\t')
        if vm.b3:            
            fw.write(str(vm.b3))                                                            ## B3 (if present)
        fw.write('\t')
        fw.write('\t'.join([str(vm.t), str(vm.beg), str(vm.end), str(vm.dur), vm.cd, vm.fm, vm.fp, vm.fv, vm.ps, vm.fs, vm.style, vm.glide]))
        fw.write('\t')      ## time of measurement, beginning and end of phone, duration, Plotnik environment codes, style coding, glide coding
        if vm.nFormants:
            fw.write(str(vm.nFormants))                                                     ## nFormants selected (if Mahalanobis method)
        fw.write('\t')
        fw.write('\t'.join([','.join([str(p) for p in vm.poles]), ','.join([str(b) for b in vm.bandwidths])]))  ## candidate poles and bandwidths (at point of measurement)
        fw.write('\n')
    fw.close()


def remeasure(measurements):
    vowels = createVowelDictionary(measurements)
    vowelMeans, vowelCovs = calculateVowelMeans(vowels)
    invowels = excludeOutliers(vowels, vowelMeans, vowelCovs)
    vowelMeans, vowelCovs = calculateVowelMeans(invowels)
    remeasurements = repredictF1F2(measurements, vowelMeans, vowelCovs, vowels)
    return remeasurements


def choosePoles(measurements, pole):
    index = pole-3
    remeasurements = []
    for vm in measurements:
        vm.f1 = vm.poles[index][0]
        vm.f2 = vm.poles[index][1]
        if len(vm.poles) < 3:
            vm.f3 = vm.poles[index][2]
        vm.b1 = vm.bandwidths[index][0]
        vm.b2 = vm.bandwidths[index][1]
        if len(vm.poles) < 3:
            vm.b3 = vm.bandwidths[index][2]
        remeasurements.append(vm)
    return remeasurements

## Main Program Starts Here
#Define some constants
#file = "/Users/joseffruehwald/Documents/Classes/Fall_10/misc/FAAV/extractFormants_modified/PH06-2-1-AB-Jean.formants"
if __name__ == '__main__':
    file = sys.argv[1]
    vowelindex = 13
    measurements = loadfile(file)
    measurements = choosePoles(measurements, 4)
    remeasurements = remeasure(measurements)

    output(remeasurements)

