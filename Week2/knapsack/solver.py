#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from dataclasses import dataclass
from queue import PriorityQueue as PQueue
Item = namedtuple("Item", ['index', 'value', 'weight'])

@dataclass
class SearchWork:
    itemlist: list
    value: int
    room: int
    taken: list

    def __lt__(self, other):
        return self.estimate > other.estimate
    
    def do_estimate(self):
        estimate = float(self.value)
        remaining_room = self.room
        for item in self.itemlist:
            if item.weight < remaining_room:
                estimate += item.value
                remaining_room -= item.weight
            else:
                estimate += remaining_room/item.weight * item.value
                remaining_room = 0
                break
        self.estimate = estimate
    
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

def children_work(work):
    item = work.itemlist[0]
    remaining_room = work.room - item.weight
    children = []
    if remaining_room > 0:
        taken = work.taken[:]
        taken[item.index] = 1
        take_work = SearchWork(work.itemlist[1:], work.value + item.value, remaining_room, taken)
        children.append(take_work)
    notake_work = SearchWork(work.itemlist[1:], work.value, work.room, work.taken[:])
    children.append(notake_work)
    for work in children:
        work.do_estimate()
    return children


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
    search_queue = PQueue()
    initial_work = SearchWork(items[:], 0, capacity, taken[:])
    initial_work.do_estimate()
    search_queue.put(initial_work)
    while True:
        work = search_queue.get()
        if len(work.itemlist) == 0:
            break
        children = children_work(work)
        for child in children:
            search_queue.put(child)
    print(work)
    for i, take in enumerate(work.taken):
        if take:
            print(i)
    #initial_work.do_estimate()
    return 0

if __name__ == '__main__':
    import time
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        start = time.time()
        print(solve_it(input_data))
        ending = time.time()
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
    print("The time of execution is:",(ending-start)*10**3,"ms")
