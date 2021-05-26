#!/bin/env python3

import sys
import os
import csv

length = len(sys.argv)
infile = None
if length >= 2:
    infile = sys.argv[1]
else:    
    # print("Usage readcmdcsv.py <csv>")
    # exit()
    infile = "cmd.csv"



if not os.path.exists(infile):
    print("%s: File not found!" % infile)
    exit()

cf = open(infile, "r", encoding="utf8", errors="", newline="" )

f = csv.reader(cf, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
header = next(f)
# print(header)

cmdlist = []
argenum = []
cmdenum = []

for row in f:
    if len(row[0]) > 0:
        cmdlist.append({'name': row[0], 'cmd': row[3], 'arg' : row[2], 'comment' : row[4]})
    argenum.append(row[2])
    cmdenum.append(row[3])

cf.close()

argenum = list(set(argenum))
cmdenum = list(set(cmdenum))

indent = ' ' * 4

print("#!/bin/env python3")
print("")
print("from enum import Enum, auto")
print("")

print("class ArgTypeEnum(Enum):")


for t in sorted(argenum):
    print(indent + "%s = auto()" % t)

print("")
print("class CommandTypeEnum(Enum):")
for t in sorted(cmdenum):
    print(indent + "%s = auto()" % t)

print("")
print("class CommandList:")
print(indent + "List = [")

cmdlist = sorted(cmdlist, key=lambda x: (x['name'][0], 0-len(x['name']), x['name']))

for t in cmdlist:
    print(indent*2 + "[\"%s\", CommandTypeEnum.%s, ArgTypeEnum.%s]," % (t['name'],t['cmd'],t['arg']))
print(indent + "]")

