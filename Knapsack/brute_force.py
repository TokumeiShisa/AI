import heapq
from itertools import product
import random
import time
class Item:
    def __init__(self, weight, value, label):
        self.weight = weight
        self.value = value
        self.label = label
        self.ans = 0
    def Output(self):
        print(self.weight, "\t", self.value,"\t", self.label, '\t', self.ans, "\n")

def GetDataFromFile(filename):
    items = []
    str = ""
    fo = open(filename, "r")
    capacity = int(fo.readline())
    _class = int(fo.readline())
    weight_list = fo.readline().split(", ")
    value_list = fo.readline().split(", ")
    label_list = fo.readline().split(", ")
    for i in range(len(weight_list)):
        items.append(Item(float(weight_list[i]), int(value_list[i]), int(label_list[i])))
    return capacity, _class, items

def CreateFileOutput(folder_name, max_val, items, i):
    filename = str(folder_name) + "/OUTPUT_" + str(i) + ".txt"
    fo = open(filename, "w")
    fo.write(str(max_val) + "\n")
    fo.write(", ".join([str(i.ans) for i in items]))
    fo.close()
    return filename

def checkClass(ifClass):
    for i in range(len(ifClass)):
        if ifClass[i] <= 0:
            return False
    return True

def bruteForce(maxW, numClass, items):
    n = len(items)
    max = 0
    permutation = [[0, 1] for i in range(n)]
    ifClass = [0 for i in range(numClass)]
    for permu in product(*permutation):
        weight = 0
        value = 0
        for i in range(len(permu)):
            weight += permu[i] * items[i].weight
            value += permu[i] * items[i].value
            if weight > maxW:
                break
        ifClass = [0 for i in range(numClass)]
        for i in range(n):
            if permu[i] == 1:
                ifClass[items[i].label - 1] += 1
        if checkClass(ifClass):
            if value > max and weight <= maxW:
                max = value
                for i in range(n):
                    items[i].ans = permu[i]
    return max

def run():
    time_list = []
    for i in range(0, 10):
        start_time = time()
        maxW, numClass, items = GetDataFromFile(f"Input/INPUT_{i}.txt")
        items_size = len(items)
        print("Test case", i + 1)
        print("Items:",items_size)

        max_val = bruteForce(maxW, numClass, items)
        
        print("Ans:", max_val)
        end = round((time() - start_time) * 1000, 4)
        print("Running time:", end, "ms")
        time_list.append(end)
        CreateFileOutput("Output/BruteForce",max_val, items, i)
        
    with open("data.txt", "a") as f:
        f.write("Brute Force:")
        f.write("\n".join([str(i) for i in items]))
        f.close()