import praat
import bisect
import string
import os
import optparse
import sys


def readPlt(path):
    """Reads in a plotnik file"""
    fi = open(path, "r")
    spinfo = fi.readline().rstrip().split(",")
    fi.readline()
    
    lines = []
    while fi:
        line = fi.readline().rstrip()
        if line == "":
            break
        else:
            line = line.split(",")
            line[-1] = line[-1].split(" ")
            lines.append(line)
    return(lines, spinfo)
        
        


def getIntervalAtTime(xmins, time, lo = 0, hi = 0):
    """Returns index of interval at given time"""

    if hi == 0:
        hi = len(xmins)
    
    index = (bisect.bisect_right(xmins[lo:hi], time)-1) + lo
    return(index)


def getVowelInterval(tg, tier, xmins, time, lo = 0, hi = 0):
    """Gets vowel interval"""

    v_Interval_index = getIntervalAtTime(xmins, time, lo, hi)

    while not isVowelInterval(tg[tier][v_Interval_index]):
       v_Interval_index = v_Interval_index + 1


    return(v_Interval_index)
        


def isVowelInterval(interval):
    """Tests to see if an interval is a CMU vowel"""
    
    return(interval.mark()[0] in ["A","E","I","O","U"])

def subDivideTime(tg, tier, n):
    """Returns subintervals in the time domain"""

    subtimes = []
    subintervals = []
    increment = (tg.xmax() - tg.xmin()) / n

    xmins = [x.xmin() for x in tg[tier]]
    last_Interval = 0
    for i in range(n+1):
        subtimes.append(tg.xmin() + (increment * i))

        this_Interval = getIntervalAtTime(xmins, tg.xmin() + (increment * i), lo = last_Interval)
        subintervals.append(this_Interval)

        subtimes[i] = tg[tier][this_Interval].xmin()

        last_Interval = this_Interval


    return(subtimes,subintervals)

def getPhoneAndWordTier(tg, spinfo):
    tier_Names = [x.name() for x in tg]

    phone_Tier = ''
    word_Tier = ''

    for i in range(len(tg)):
        if spinfo[0] in  tier_Names[i]:
            if "phone" in tier_Names[i]:
                phone_Tier = i
            elif "word" in tier_Names[i]:
                word_Tier = i

    if phone_Tier != '' and word_Tier != '':
        return(phone_Tier, word_Tier)
    else:
        return(0, 1)


def getWordContext(word, phone):
    context = "Internal"
    if word.xmin() == phone.xmin():
        if word.xmax() == phone.xmax():
            context = "Coextensive"
        else:
            context = "Initial"
    elif word.xmax() == phone.xmax():
        context = "Final"

    return(context)


def getWordTranscription(tg, word_Tier, phone_Tier, word_Index):
    word_Start = tg[word_Tier][word_Index].xmin()
    word_End = tg[word_Tier][word_Index].xmax()
    phone_xmins = [x.xmin() for x in tg[phone_Tier]]
    word_xmins = [x.xmin() for x in tg[word_Tier]]

    first_Phone = getIntervalAtTime(phone_xmins, word_Start + 0.001)
    last_Phone = getIntervalAtTime(phone_xmins, word_End - 0.001)

    word = []
    for i in range(first_Phone, last_Phone + 1):
        word.append(tg[phone_Tier][i].mark())

    word_str = string.join(word, sep = " ")
    return(word_str)


def writeContextInfo(path, spinfo, line, context, pre_Seg, post_Seg, post2_Seg, word_Trans, post_word_Trans):
    """Writes data to file"""

    line[3] = line[3].split(".")
    line[3][-1] = string.join([x for x in line[3][-1]], sep = "\t")
    line[3] = string.join(line[3], "\t")
    word = line[-1][0]
    time = line[-1][-1]
    line[-1] = string.join(line[-1], sep = " ")
    line.append(word)
    line.append(time)
    line = string.join(line, "\t")

    spinfo = string.join(spinfo, "\t")

    outline = [spinfo, line, context, pre_Seg, post_Seg, post2_Seg, word_Trans, post_word_Trans]

    outline = string.join(outline, "\t")

    savef = open(path, "a")
    savef.write(outline+"\n")
    savef.close()


def getContext(tgfile, pltfile, savepath):
    """Primary function"""
    tg = praat.TextGrid()
    tg.read(tgfile)
    maxtime = tg.xmax()
    
    lines, spinfo = readPlt(pltfile)

    path_elements = tgfile.split("/")
    print "Processing %s\n" %path_elements[-1]

    savefile = path_elements[-1].replace("TextGrid", "txt")
        
    if savepath is None:
        if len(path_elements[:-1]) < 1:
            savepath = ""
        else:
            savepath = "/"
        for element in path_elements[:-1]:
            savepath = os.path.join(savepath, element)

    path = os.path.join(savepath, savefile)


    phone_Tier, word_Tier = getPhoneAndWordTier(tg, spinfo)
    print "Phone tier "+repr(phone_Tier)+" and Word Tier "+repr(word_Tier)

    phone_xmins = [x.xmin() for x in tg[phone_Tier]]
    word_xmins = [x.xmin() for x in tg[word_Tier]]

    print "NPhones = "+repr(len(phone_xmins))
    print "NWords = "+repr(len(word_xmins))

    last_v_Interval = 0

##    v_Sub_Time, v_Sub_Interval = subDivideTime(tg, phone_Tier, 10)
##    w_Sub_Time, w_Sub_Interval = subDivideTime(tg, word_Tier, 10)

    for line in lines:
        time = float(line[-1][-1])
        if time > maxtime:
            print "Error! TextGrid ended early"
            break
        
        word = line[-1][0]

##        v_Index = bisect.bisect(v_Sub_Time, time)
##        w_Index = bisect.bisect(w_Sub_Time, time)

##        v_Lo = v_Sub_Interval[v_Index-1]
##        v_Hi = v_Sub_Interval[v_Index]

##        w_Lo = w_Sub_Interval[w_Index-1]
##        w_Hi = w_Sub_Interval[w_Index]



        v_Interval_index = getVowelInterval(tg, phone_Tier, phone_xmins, time, lo = last_v_Interval)
        last_Interval = v_Interval_index
        
        pre_Interval_index = v_Interval_index - 1
        post_Interval_index = v_Interval_index + 1
        post2_Interval_index = v_Interval_index + 2

        pre_Seg = tg[phone_Tier][pre_Interval_index].mark()
        post_Seg = tg[phone_Tier][post_Interval_index].mark()
        post2_Seg = tg[phone_Tier][post2_Interval_index].mark()



        phone_Interval = tg[phone_Tier][v_Interval_index]

        w_Interval_Index = getIntervalAtTime(word_xmins, phone_Interval.xmin()+0.001)

        
        word_Interval = tg[word_Tier][w_Interval_Index]

        context = getWordContext(word_Interval, phone_Interval)

        word_Trans = getWordTranscription(tg, word_Tier, phone_Tier, w_Interval_Index)
        post_word_Trans = getWordTranscription(tg, word_Tier, phone_Tier, w_Interval_Index+1)

        writeContextInfo(path, spinfo, line, context, pre_Seg, post_Seg, post2_Seg, word_Trans, post_word_Trans)   


######################
##  Main Program
######################

parser = optparse.OptionParser()
parser.add_option("-m", "--multiple", action = "store_true", default = False, dest = "multiple")
parser.add_option("-s", "--savepath", action = "store", dest = "savepath")

(options, args) = parser.parse_args()

if options.multiple:
    tgfile_mult = open(args[0])
    pltfile_mult = open(args[1])

    while tgfile_mult:
        tgfile = tgfile_mult.readline().rstrip()
        if tgfile == "":
            break
        pltfile = pltfile_mult.readline().rstrip()

        getContext(tgfile, pltfile, options.savepath)

        
else:
    tgfile = args[0]
    pltfile = args[1]

    getContext(tgfile, pltfile, options.savepath)
    




#tgfile = "/Users/joseffruehwald/Documents/Classes/FAAV/python/PH73-0-7-EDonnelly.TextGrid"
#pltfile = "/Users/joseffruehwald/Documents/Classes/FAAV/python/PH73-0-7-EDonnelly-rx.plt"
#getContext(tgfile, pltfile, None)
