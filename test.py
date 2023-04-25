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

def DataGenerate(size, _class):
    sets = []
    max_weight = 0
    min_weight = 0    
    for x in range(_class):
        weight = random.uniform(1,100)
        value = random.randint(1,100)
        sets.append(Item(weight, value, x + 1))
        min_weight += weight
        max_weight += weight
    for x in range(size - _class):
        weight = random.uniform(1,100)
        value = random.randint(1,100)
        label = random.randint(1, _class)
        sets.append(Item(weight, value, label))
        max_weight += weight
    capacity = int(random.uniform(min_weight, max_weight))   
    random.shuffle(sets) 
    return (capacity, sets)
        
def CreateFileInput(size, _class, i):
    capacity, sets = DataGenerate(size, _class)
    filename = "INPUT_" + str(i) + ".txt"
    fi = open(filename, "w")
    fi.write(str(capacity) + "\n")
    fi.write(str(_class) + "\n")
    fi.write(", ".join([str(i.weight) for i in sets]) + "\n")
    fi.write(", ".join([str(i.value) for i in sets]) + "\n")
    fi.write(", ".join([str(i.label) for i in sets]))
    fi.close()
    return filename

def GetDataFromFile(filename):
    sets = []
    str = ""
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
    fo.write(", ".join([str(i.ans) for i in sets]))
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
    
def branchAndBound(maxW, numClass, items):
    n = len(items)
    root = [0, set(), 0, 0, []]
    heap = [(0, root)]
    max = 0
    while(heap):
        ign, node = heapq.heappop(heap)
        level, selectedClasses, value, weight, selectedItems = node
        if level == n:
            if value > max:
                max = value
                for i in range(n):
                    items[i].ans = selectedItems[i]
            continue
        curWeight, curValue, curClass = items[level].weight, items[level].value, items[level].label
        if curClass not in selectedClasses:
            selectedClasses.add(curClass)
        bound = value + (maxW - weight) * (curValue / curWeight)
        if (weight + curWeight <= maxW):
            heapq.heappush(heap, (-bound, (level + 1, selectedClasses, value + curValue, weight + curWeight, selectedItems + [1], )))
            heapq.heappush(heap, (-bound, (level + 1, selectedClasses, value, weight, selectedItems + [0])))
        else:
            heapq.heappush(heap, (0, (level + 1, selectedClasses, value, weight, selectedItems + [0])))
    return max
    
if __name__ == "__main__":
    '''
    for i in range(1,6):			#tao random 5 file size 10 - 40
        size = random.randint(10, 40)
        _class = random.randint(2, 3)
        print(CreateFileInput(size, _class, i))
    
    for i in range(6,11):			#tao random 5 file size 50 - 1000
        size = random.randint(50, 1000)
        _class = random.randint(5, 10)
        print(CreateFileInput(size, _class, i))
    '''
    for i in range(1, 11):
        filename = 'INPUT_' + str(i) + '.txt'
        maxW, numClass, items = GetDataFromFile(filename)
        start = time.time()
        max = bruteForce(maxW, numClass, items)
        #max = branchAndBound(maxW, numClass, items)
        end = time.time()
        print('test case', i,  ':', end - start)
        CreateFileOutput(max, items, i)
