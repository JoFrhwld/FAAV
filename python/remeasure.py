file = "/Users/joseffruehwald/Documents/Classes/Fall_10/misc/FAAV/extractFormants_modified/PH06-2-1-AB-Jean.formants"
f = open(file)
line = f.readline()
line = f.readline()
line = f.readline()
line = f.readline().rstrip()

import ast

line2 = line.split("\t")

poles = ast.literal_eval(line2[20])
bandwidths = ast.literal_eval(line2[21])
