#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import operator
import numpy as np 

Item = namedtuple("Item", ['index', 'value', 'weight','density'])

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
        #if int(parts[1])<=capacity:
        items.append(Item(i-1, int(parts[0]), int(parts[1]),int(parts[0])/int(parts[1])))

    #items.sort(key = operator.itemgetter(3),reverse = True)

    table=np.zeros((capacity+1,len(items)+1))
    value = 0
    weight = 0
    taken = [0]*len(items)

    for j in range(len(items)+1):
        for capacities in range(table.shape[0]):
            if j==0 or capacities==0:
                table[capacities,j]=0
            #if item fits, take max of item's value + previous value without the item (v_i=i.value+table[k-weight,i-1])
            #or don't pick the item and keep the value without the item               (v_i=table[k,i-1])
            elif items[j-1].weight<=capacities:
                table[capacities,j]=max(items[j-1].value +table[capacities-items[j-1].weight,j-1],table[capacities,j-1])
            else:
                table[capacities,j]=table[capacities,j-1]

    value=int(table[capacity,len(items)])

    #Backtracking
    for i in range(len(items),0,-1):
        if table[capacity,i]==table[capacity,i-1]:
            #print('Item',i,'was not picked up')
            taken[i-1]=0
        else:
            capacity=capacity-items[i-1].weight
            #print('Item', i, 'was picked up')
            taken[i-1]=1
    #print(table)


    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

