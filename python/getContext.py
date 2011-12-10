import praat
import bisect


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
        
        


def getIntervalAtTime(tg, tier, time, lo = 0, hi = 0):
    """Returns index of interval at given time"""
    
    if hi == 0:
        hi = len(tg[tier])
    
    index = (bisect.bisect_right([x.xmin() for x in tg[tier][lo:hi]], time)-1) + lo
    return(index)


def getVowelInterval(tg, tier, time, lo = 0, hi = 0):
    """Gets vowel interval"""

    v_Interval_index = getIntervalAtTime(tg, tier, time, lo, hi)

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

    last_Interval = 0
    for i in range(n+1):
        subtimes.append(tg.xmin() + (increment * i))

        this_Interval = getIntervalAtTime(tg, tier, tg.xmin() + (increment * i), lo = last_Interval)
        subintervals.append(this_Interval)


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



tg = praat.TextGrid()
tg.read("/Users/joseffruehwald/Documents/Classes/FAAV/python/PH73-0-7-EDonnelly.TextGrid")
lines, spinfo = readPlt("/Users/joseffruehwald/Documents/Classes/FAAV/python/PH73-0-7-EDonnelly-rx.plt")

phone_Tier, word_Tier = getPhoneAndWordTier(tg, spinfo)

sub_v_Time, sub_v_Index = subDivideTime(tg, 0, 10)
sub_w_Time, sub_w_Index = subDivideTime(tg, 1, 10)



for line in lines:
    time = float(line[-1][-1])
    word = line[-1][0]

    jawn = bisect.bisect(sub_v_Time, time)
    lo = sub_v_Index[jawn-1]
    hi = sub_v_Index[jawn]
    
    v_Interval_index = getVowelInterval(tg, phone_Tier, time, lo = lo, hi = hi)
    pre_Interval_index = v_Interval_index - 1
    post_Interval_index = v_Interval_index + 1
    post2_Interval_index = v_Interval_index + 2

    pre_Seg = tg[phone_Tier][pre_Interval_index].mark()
    post_Seg = tg[phone_Tier][post_Interval_index].mark()
    post2_Seg = tg[phone_Tier][post2_Interval_index].mark()

    phone_Interval = tg[phone_Tier][v_Interval_index]
    word_Interval = tg[word_Tier][getIntervalAtTime(tg, word_Tier, phone_Interval.xmin())]

    context = getWordContext(word_Interval, phone_Interval)

    
