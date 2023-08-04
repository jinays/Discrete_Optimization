#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def cal_relaxation(itemlist,weight,value):
    current_weight = 0
    estimate = value
    if len(itemlist) > 1:
        for item in itemlist:
            if current_weight + item.weight < weight:
                estimate += item.value
            else:
                estimate += (weight-current_weight)/item.weight*item.value
    elif len(itemlist)==1:
        estimate += itemlist[0].value
    return estimate

def cal_branch(tuplelist):
    target = tuplelist[0]
    itemlist = target[0]
    value = target[1]
    room = target[2]
    estimate = target[3]
    taken = target[4]
    tuplelist.remove(tuplelist[0])
    room_a_a = room - itemlist[0].weight
    #not take
    estimate0 = cal_relaxation(itemlist[1:],room,value)
    #take
    #feasible
    if room_a_a >= 0:
        estimate = cal_relaxation(itemlist,room,value)
        newtaken = taken[:]
        newtaken[itemlist[0].index] = 1
        #tuplelist.append((itemlist[1:],value+itemlist[0].value,room-itemlist[0].weight,estimate,newtaken))
        pos = -1
        n=0
        for tuples in tuplelist:
            print(tuplelist)
            pos += 1
            if tuples[3]<=estimate0 and n!=1:
                tuplelist.insert(pos, (itemlist[1:],value,room,estimate0,taken))
                if n==2:
                    break
                else:
                    n=1
            elif pos == len(tuplelist) - 1:
                tuplelist.append((itemlist[1:],value,room,estimate0,taken))
            if tuples[3]<=estimate and n!=2:
                tuplelist.insert(pos, (itemlist[1:],value+itemlist[0].value,room-itemlist[0].weight,estimate,newtaken))
                if n==1:
                    break
                else:
                    n=2
            elif pos == len(tuplelist) - 1:
                tuplelist.append((itemlist[1:],value+itemlist[0].value,room-itemlist[0].weight,estimate,newtaken))
#        while n!=3:
#            if (i> len(tuplelist)-1 or tuplelist[i][3]<=estimate0) and n!=1:
#                tuplelist.insert(i, (itemlist[1:],value,room,estimate0,taken))
#                if n==2:
#                    n = 3
#                else:
#                    n = 1
#            elif (i> len(tuplelist)-1 or tuplelist[i][3]<=estimate) and n!=2:
                #print(tuplelist)
#                tuplelist.insert(i, (itemlist[1:],value+itemlist[0].value,room-itemlist[0].weight,estimate,newtaken))
#                if n==1:
#                    n = 3
#                else:
#                    n = 2
#            i += 1
    #tuplelist.append((itemlist[1:],value,room,estimate0,taken))
    #tuplelist.sort(reverse=True,key = lambda choice: choice[3])
    else:
        i=0
        n=0
        while n==0:
            if (i> len(tuplelist)-1 or tuplelist[i][3]<=estimate0):
                tuplelist.insert(i, (itemlist[1:],value,room,estimate0,taken))
                n=1
            i += 1
    return tuplelist

def solve_it(input_data):
    # parse the input
    lines = input_data.split('\n')
    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    items = []
    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))
    taken = [0]*len(items)
    items.sort(reverse=True,key = lambda item: item.value/item.weight)
    n = 0
    tuplelist = [(items,0,capacity,cal_relaxation(items,capacity,0),taken)]
    while n == 0:
        result = cal_branch(tuplelist)
        if (tuplelist[0][1]==tuplelist[0][3]) & (len(tuplelist[0][0])==0):
            result = tuplelist[0]
            n = 1
    # prepare the solution in the specified output format
    output_data = str(result[1]) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, result[4]))
    return output_data

if __name__ == '__main__':
    import time
    start = time.time()
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
    ending = time.time()
    print("The time of execution is:",(ending-start)*10**3,"ms")
