def syllabify(w):
    import re

    #w = ["S", "T", "R", "EH1", "NG", "TH", "AH0", "N"] #strengthen
    #w = ["M", "AE2", "S", "T", "ER0"] #master
    #w = ["B","AE","N","ER"] #banner
    #w = ["B","AE","N","T","ER"] #banter
    #w = ["P","R","AE","NG","K","S","T","ER","Z"] #pranksters
    #w = ["S","IH","K","S","TH","S"] #sixths
    nuc = re.compile("A|E|I|O|U|@")
    n = 0
    nucs = []
    for i in range(len(w)):
        p = nuc.search(w[i])
        if p:
            n = n+1
            nucs.append(i)
            if "R" in w[i]:
                if i+1 == len(w):
                    w.append("R")
                elif w[i+1] is not "R":
                    w.insert(i+1,"R")
    syls = []
    nsyls = []
    
    for i in range(n):
        if w[nucs[i]]=="@":
            stress = 0
        else:
            stress = re.compile("\d").search(w[nucs[i]]).group()
        if w[nucs[i]] == "AH0":
            w[nucs[i]] = "@"
        syls.append([[],[re.sub("\d","",w[nucs[i]])   ],[],[stress]])
        #syls.append([[],[w[nucs[i]]],[]])
        #print "Nucleus is "+w[nucs[i]]
        nsyls.append([[],[nucs[i]],[]])
        #if "R" in w[nucs[i]]:
        #    syls[i][2].append("R")

        while nsyls:
            if len(syls[i][0])<1:
                ons = nsyls[i][1][0]-1
            else:
                ons = nsyls[i][0][0]-1
            if ons==-1:
                #print "Onset ended: Word Begining"
                break
            if ons == nsyls[i-1][1][0]:
                #print "Onset ended : Syl Boundary"
                break
           
        
            okl = re.compile("B|F|G|K|P|S|S")
            okr = re.compile("B|D|F|G|K|P|T|V")
            oks = re.compile("K|L|M|N|P|T|V|W")
            okw = re.compile("T|D|K|P|S")
            oky = re.compile("B|F|V|K|G")

       
        
            if len(syls[i][0])==0:
                #print "Adding "+w[ons]+" to onset"
                syls[i][0].insert(0,w[ons])
                nsyls[i][0].insert(0,ons)
            elif syls[i][0][0] == "L":
                if okl.match(w[ons]):
                    #print "Adding "+w[ons]+" onset: Acceptable XL onset"
                    syls[i][0].insert(0,w[ons])
                    nsyls[i][0].insert(0,ons)
                else:
                    break
            elif syls[i][0][0] == "R":
                if okr.match(w[ons]):
                    #print "Adding "+w[ons]+" onset: Acceptable XR onset"
                    syls[i][0].insert(0,w[ons])
                    nsyls[i][0].insert(0,ons)
                else:
                    break
            elif syls[i][0][0] == "W":
                if okw.match(w[ons]):
                    #print "Adding "+w[ons]+" onset: Acceptable XR onset"
                    syls[i][0].insert(0,w[ons])
                    nsyls[i][0].insert(0,ons)
                else:
                    break
            elif syls[i][0][0] == "Y":
                if oky.match(w[ons]):
                    #print "Adding "+w[ons]+" onset: Acceptable XR onset"
                    syls[i][0].insert(0,w[ons])
                    nsyls[i][0].insert(0,ons)
                else:
                    break
            elif oks.match(syls[i][0][0]):
                if w[ons] == "S":
                    #print "Adding "+w[ons]+" onset: Acceptable SX onset"
                    syls[i][0].insert(0,w[ons])
                    nsyls[i][0].insert(0,ons)
                else:
                    break
            else:
                break
    for i in range(n):
        if len(syls[i][0])>=1 and syls[i][0][0] == "NG":
            syls[i][0].pop(0)
            syls[i-1][2].append("NG")
        while nsyls:
            if len(nsyls[i][2]) == 0:
                cod = nsyls[i][1][0] + 1
            else:
                cod = nsyls[i][2][-1]+1
        
            if cod == len(w):
                #print "End Sylable "+str(i+1)+":End of Word"
                break
            elif i+1 == len(syls):
                #print "Adding "+w[cod]+" to Syl "+str(i+1)+" Coda"
                syls[i][2].append(w[cod])
                nsyls[i][2].append(cod)
            elif len(nsyls[i+1][0]) == 0:
                if cod == nsyls[i+1][1][0]:
                    #print "End Sylable "+str(i+1)
                    break
            elif cod == nsyls[i+1][0][0]:
                #print "End Sylable "+str(i+1)
                break
            else:
                #print "Adding "+w[cod]+" to Syl "+str(i+1)+" Coda"
                syls[i][2].append(w[cod])
                nsyls[i][2].append(cod)
    return syls

def defSyl(syl,n):
    sylinfo = []
    wlen = len(syl)
    nfollowing  = wlen - (n+1)
    coda = None
    final = None
    folseg = None
    onset = None
    preseg = None
    vowel = syl[n][1][0]
    
    if len(syl[n][2]) == 0:
        coda = "open"
    elif len(syl[n][2]) == 1:
        coda = "checked"
    elif len(syl[n][2]) > 1:
        coda = "complex"

    if nfollowing == 0:
        if coda == "open":
            final = "final"
        else:
            final = "non"
    else:
        final = "non"

    if final == "final":
        folseg = "final"
    elif len(syl[n][2]) != 0:
        folseg = syl[n][2][0]
    elif len(syl[n+1][0]) != 0:
        folseg = syl[n+1][0][0]
    else:
        folseg = "hiatus"

    if len(syl[n][0])==0:
        if n ==0:
            onset = "initial"
        else:
            onset = "none"
    elif len(syl[n][0])==1:
        onset = "simple"
    elif len(syl[n][0])>1:
        onset = "complex"

    if onset == "initial":
        preseg = "initial"
    elif onset == "none":
        preseg = "hiatus"
    else:
        preseg = syl[n][0][-1]

    segfeatures = {
        "B" : ["labial","voiced","stop"],
        "CH": ["palatal","voiceless","affricate"],
        "D" : ["apical","voiced","stop"],
        "DH": ["apical","voiced","fricative"],
        "F" : ["labial","voiceless","fricative"],
        "G" : ["velar","voiced","stop"],
        "HH": ["h","voiceless","fricative"],
        "JH": ["palatal","voiced","affricate"],
        "K" : ["velar","voiceless","stop"],
        "L" : ["apical","voiced","l"],
        "M" : ["labial","voiced","nasal"],
        "N" : ["apical","voiced","nasal"],
        "NG": ["velar","voiced","nasal"],
        "P" : ["labial","voiceless","stop"],
        "R" : ["r","voiced","r"],
        "S" : ["apical","voiceless","fricative"],
        "SH": ["palatal","voiceless","fricative"],
        "T" : ["apical","voiceless","stop"],
        "TH": ["apical","voiceless","fricative"],
        "V" : ["labial","voiced","fricative"],
        "W" : ["labial","voiced","glide"],
        "Y" : ["palatal","voiced","glide"],
        "Z" : ["apical","voiced","fricative"],
        "ZH": ["palatal","voiced","fricative"],
        "hiatus" : ["hiatus","voiced","hiatus"],
        "final" : ["final","final","final"]
        }
    thisseg = segfeatures[folseg]

    sylinfo = [vowel,str(nfollowing),coda,final,folseg,onset,preseg,thisseg[0],thisseg[1],thisseg[2]]
    return sylinfo

def cmutrans(word, cmu):
    if word in cmu:
        trans = cmu[word]
    else:
        sys.stderr.write("Please transcribe "+word+" "+vowel+"\n")
        trans = sys.stdin.readline().rstrip().upper()
        while "  " in trans:
            trans = trans.replace("  "," ")
        trans = trans.split(" ")
        valid = True
        transerror = []

        for j in trans:
            if dig.sub("",j) not in folsegcoding:
                valid = False
                transerror.append(j+" Not Part of CMU Character Set")
            if vowels.match(j) and not dig.search(j):
                valid = False
                transerror.append("Stress Missing on "+j)
            if not valid:
                for err in transerror:
                    sys.stderr.write("Error: "+err+"\n")
                break
        if valid:
            print "valid!"
            cmu[word] = trans

            cmuf2 = open(cmufilename,'a')
            #cmuf = open('cmudict.0.7a.JTFedit2009','a')
            writetrans = string.join(trans," ")
            cmuf2.write(word+"  "+writetrans+"\n")
            cmuf2.close()
    return(trans)

def readcmu(file):
    cmuf = open(file)
    #cmuf = open("cmudict.0.7a.JTFedit2009")
    cmu = {}
    for line in cmuf:
        line = line.rstrip()
        if ";;;" not in line:
            line = line.split("  ")
            line[1] = line[1].split(" ")
            abc = re.compile("[A-Z]*")
            cmu[line[0]] = line[1]
    cmuf.close()
    return(cmu)

def guesssyl(vowel, syls):
    thesyl = 0
    matchedsyl = "Monosyl"
    if len(syls) > 1:
        found = False
        for i in range(len(syls)):
            
            if syls[i][1][0] == vowel and int(syls[i][3][0]) == 1:
                matchedsyl =  "Exact"
                thesyl = i
                found = True
                
                break
    if not found:
        for i in range(len(syls)):
            if syls[i][1][0] == vowel:
                matchedsyl = "Vowel"
                thesyl = i
                found = True
                break
    if not found:
        for i in range(len(syls)):
            if int(syls[i][3][0]) == 1:
                matchedsyl =  "Stress"
                thesyl = i
                break
    return thesyl, matchedsyl

def findsyl(index, syls):
    thesyl = 0
    total = 0
    for i in range(len(syls)):
        if total + len(syls[i][0]) + len(syls[i][1]) >= index:
            thesyl = i
            break
        else:
            total = len(syls[i][0]) + len(syls[i][1]) + len(syls[i][2])
    return thesyl        

import re
import string
import sys

args = sys.argv
#sys.stderr.write(string.join(args, sep = "\n"))
tocode = sys.argv[1]
wordindex = int(sys.argv[2])-1
vowelindex = int(sys.argv[3])-1
transindex = sys.argv[4]
sylindex = sys.argv[5]

if len(transindex) > 2:
    cmu = readcmu(transindex)
else:
    transindex = int(transindex) - 1
    
form = open(tocode)
#form = open("../anaeformants-clean.txt")
dig  = re.compile("\d")
header = form.readline().rstrip()

#sylinfo = [vowel,str(nfollowing),coda,final,folseg,onset,preseg,thisseg[0],thisseg[1],thisseg[2]]
features = "\tVowel2\tFolSyl\tCoda\tFinal\tFolSeg\tOnset\tPreSeg\tPlace\tVoice\tManner"

sys.stdout.write(header+features+"\n")
for line in form:
    line = line.rstrip()
    if len(line) < 1:
       
        break
    line = line.split("\t")
    #vowel = "AY"
    

    word = line[wordindex]
    vowel = line[vowelindex]
    notinword= re.compile("[\d()]")
    word = notinword.sub("",word).upper()
    
    syls = []
    if transindex == "cmu":
        trans = cmutrans(word, cmu)
        syls = syllabify(trans)
    else:
        trans = line[transindex].split(" ")
        syls = syllabify(trans)        


    if sylindex == "guess":
        syl,matched = guesssyl(vowel, syls)
    else:
        index = int(line[int(sylindex)-1])
        syl = findsyl(index, syls)
       
        

    sylinfo = defSyl(syls,syl)
    line = string.join(line, "\t")
    sylinfo = string.join(sylinfo,"\t")
    sys.stdout.write(line+"\t"+sylinfo+"\n")

 
    

#                sylinfo = defSyl(syls,thesyl)
#                sylinfo.append(matchedsyl)
#                line = string.join(line, "\t")
#                sylinfo = string.join(sylinfo,"\t")
#                sys.stdout.write(line+"\t"+sylinfo+"\n")

