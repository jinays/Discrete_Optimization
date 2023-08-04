#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def cal_relaxation(itemlist,weight,value):
    estimate = value
    if len(itemlist) > 1:
        for item in itemlist:
            if item.weight < weight:
                estimate += item.value
            else:
                estimate += (weight)/item.weight*item.value
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
    itemtcho = itemlist[0]

    room_a_a = room - itemtcho.weight
    #take
    #feasible
    if room_a_a >= 0:
        estimate = cal_relaxation(itemlist,room,value)
        newtaken = taken[:]
        newtaken[itemtcho.index] = 1
        tuplelist[0] = (itemlist[1:],value+itemtcho.value,room-itemtcho.weight,estimate,newtaken)
    else: #not feasible (no enough room)
        tuplelist.remove(tuplelist[0])
    #not take
    estimate0 = cal_relaxation(itemlist[1:],room,value)
    tuplelist.append((itemlist[1:],value,room,estimate0,taken))
    tuplelist.sort(reverse=True,key = lambda choice: choice[3])
    return 0

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

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

    taken = [0]*len(items) #items ->priority queue
    items.sort(reverse=True,key = lambda item: item.value/item.weight)
    n = 0
    tuplelist = [(items,0,capacity,cal_relaxation(items,capacity,0),taken)]
    while n == 0:
        cal_branch(tuplelist)
        current_max = tuplelist[0]
        if (len(current_max[0])==0):
            result = current_max
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
