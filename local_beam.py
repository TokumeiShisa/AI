import itertools
import random
import numpy as np
from time import *


class Item:
    def __init__(self, weight, value, label):
        self.weight = weight
        self.value = value
        self.label = label
        self.ans = 0
    def Output(self):
        print(self.weight, "\t", self.value,"\t", self.label, '\t', self.ans)

def GetDataFromFile(filename):
    sets = []
    fo = open(filename, "r")
    capacity = int(fo.readline())
    _class = int(fo.readline())
    weight_list = fo.readline().split(", ")
    value_list = fo.readline().split(", ")
    label_list = fo.readline().split(", ")
    for i in range(len(weight_list)):
        sets.append(Item(float(weight_list[i]), int(value_list[i]), int(label_list[i])))
    return capacity, _class, sets

def CreateFileOutput(max_val, sets, i):
    filename = "OUTPUT_" + str(i) + ".txt"
    fo = open(filename, "w")
    fo.write(str(max_val) + "\n")
    fo.write(", ".join([str(i) for i in sets]))
    fo.close()
    return filename

"""GLOBAL VARIABLES"""
sets = []
class_num = 2
capacity = 0
sets_size = 0
k = 10
loop_num = 100
""""""

def CheckDupe(sets_size, state):
    for i in sets_size:
        if state == i: return False 
    return True

def CheckClass(state):
    class_count = [0] * (class_num + 1)
    class_count[0] = 1
    c = [1] * (class_num + 1)
    for i in range(sets_size):
        if state[i] == 1 and class_count[sets[i].label] == 0:
            class_count[sets[i].label] = 1
    return class_count == c

def CheckWeight(state):
    total_value = 0
    total_weight = 0
    for i in range(sets_size):
        total_value += sets[i].value * state[i]
        total_weight += sets[i].weight *  state[i]
    if total_weight <= capacity and CheckClass(state):
        return total_value
    return 0

def GenerateInitialState():
    state_list = []
    while len(state_list) < k:
        state = []
        for i in range(sets_size):
            state.append(random.choice([0, 1]))
        if CheckDupe(state_list, state) and CheckClass(state):
            state_list.append(state)
    return state_list

def CreateDescendants(state_list):
    descendant_list = []
    for j in range(k):
        for i in range(sets_size):
            descendant = state_list[j].copy()
            descendant[i] = 1 - descendant[i]
            if CheckWeight(descendant) == 0:
                descendant[i] = 1 - descendant[i]
            descendant_list.append(descendant)
    return descendant_list

def BestKStates(state_list):
    state_list.sort(key = CheckWeight, reverse = True)
    return state_list[:k]

def LocalBeam(sets):
    state_list = GenerateInitialState()
    best_state = [0] * sets_size
    max_val = 0
    for _ in range(loop_num):
        descendant_list = CreateDescendants(state_list)
        best_k_state = BestKStates(descendant_list)
        for i in best_k_state:
            if max_val < CheckWeight(i):
                best_state = i
                max_val = CheckWeight(i)
    return max_val, best_state
        
if __name__ == "__main__":
    for i in range(1, 10):
        start_time = time()
        capacity, class_num, sets = GetDataFromFile(f"TEST/INPUT_{i}.txt")
        sets_size = len(sets)
        print(i,sets_size)
        k = sets_size
        loop_num = sets_size * 10
        max_val, ans = LocalBeam(sets)
        CreateFileOutput(max_val, ans, i)
        print(max_val, "Running time", round((time() - start_time) * 1000, 3), "ms")