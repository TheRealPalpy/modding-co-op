# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 13:17:49 2020

@author: TheThBa
"""

import os.path
import re
import sys

user_path = "../history/states"  # enter the history/states path of your mod here

###############################################################################
provdef_file = os.path.join(user_path, "ProvinceDefinitions.txt")
if os.path.exists(provdef_file):
    os.remove(provdef_file)
def CreateProvList(statepath, check):
    global provid
    with open(statepath, "r") as f:
        stateid = 0 #get rid of the content of province ids - list may vary in length and carryover on tail end would be bad
        idfound = 0 #state id
        providfound = 0  # province id
        line = f.readline()
        while idfound == 0:
            if re.search('id=.+', line) or re.search('id = .+', line) or re.search('id =.+', line) or re.search('id= .+', line):
                stateid = int(re.findall(r'\d+', line)[0]) #we only expect 1 state id, so we just reduce the 1D-Array to an int
                idfound = 1
            line = f.readline()
            print("Stuck on line:", line)
            if line[-1:] != '\n':
                break
        while line and providfound == 0:
            if re.search('provinces=.+',line) or re.search('provinces = .+',line):
                line = f.readline()
                ids = re.findall(r'\d+', line)
                for n in range(0, len(ids)):
                    provid.append((stateid, int(ids[n])))
                    providfound = 1
            line = f.readline()
    firstcall = 1
    f.close

def SortProvList(provlist):
    provlist.sort(key = lambda province: province[1])
    return (provlist) #<--- this guy is now in the correct order to use provIDs as a HOI4 index (!) or it would be so if there weren't sea provinces

statefiles = [f for f in os.listdir(user_path) if os.path.isfile(os.path.join(user_path,f))]
x = 0
firstcall = 0
provid = []
while x < len(statefiles):
    CreateProvList(os.path.join(user_path, statefiles[x]), firstcall)
    if firstcall <= 1:
        total_list = provid
    else:
        total_list.extend(provid)
    x = x+1
    print("X:", x)
    print("Length:", len(statefiles))

provid = SortProvList(provid)
i = 0
s = len(provid)
l = 0
o = 1
while l<s:
    k = 1
    o = o+1
    if (100*o)%s == 0:
        print("Progress: "+str(100*o/s) + "%")
    with open(provdef_file, "a") as file_object:
        if int(str(provid[l][0])) != 0:
            provdef = str(provid[l][0])+""" = { add_to_array = { provinces = """+str(provid[l][1])+""" } } #Province Nr. is """+str(provid[l][1])+""" \n"""
            file_object.write(provdef)
        while True:
            if l+k >= len(provid):
                break
            if provid[l][1] == provid[l+1][1]:
                print("THERE ARE MULTIPLE STATES SHARING A PROVINCE!! PROGRAM TERMINATED!! STATES:"+str(provid[l][0])+" and "+str(provid[l+1][0])+". Province:"+str(provid[l][1])) #direct end of program
                sys.exit()
                if os.path.exists(provdef_file):
                    os.remove(provdef_file)
            if provid[l][1]+k == provid[l+k][1]:
                break
            provid.insert(l+k, (0, provid[l][1]+k))
            k = k+1
            s = s+1
    l = l+1
print("Done. If there are any issues ping me on Discord: @TheThBa#0244")
