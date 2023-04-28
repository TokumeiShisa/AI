from itertools import product
import random
import time
class Item:
    def __init__(self, weight, value, label, index):
        self.weight = weight
        self.value = value
        self.label = label
        self.ans = 0
        self.ratio = value / weight
        self.index = index
    def Output(self):
        print(self.weight, "\t", self.value,"\t", self.label, '\t', self.ans, "\n")

def DataGenerate(size, _class):
    sets = []
    max_weight = 0
    min_weight = 0    
    for x in range(_class):
        weight = random.uniform(1,100)
        value = random.randint(1,100)
        sets.append(Item(weight, value, x + 1, x))
        min_weight += weight
        max_weight += weight
    for x in range(size - _class):
        weight = random.uniform(1,100)
        value = random.randint(1,100)
        label = random.randint(1, _class)
        sets.append(Item(weight, value, label, x + _class))
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
        sets.append(Item(float(weight_list[i]), int(value_list[i]), int(label_list[i]), int(i)))
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

def calBound(maxW, value, weight, items, i):
    return value + (maxW - weight) * items[i + 1].ratio

def branchAndBound(maxW, numClass, items):
    n = len(items)
    w = 0
    v = 0
    items.sort(key=lambda x: x.ratio, reverse=True)
    for i in range(n - 1):
        ub1 = calBound(maxW, v + items[i].value, w + items[i].weight, items, i)  #with items[i]
        ub2 = calBound(maxW, v, w, items, i)    #without items[i]
        if ub1 > ub2 and w + items[i].weight <= maxW:
            w += items[i].weight
            v += items[i].value
            items[items[i].index].ans = 1
    if w + items[n - 1].weight <= maxW:
        w += items[n - 1].weight
        v += items[n - 1].value
        items[items[n - 1].index].ans = 1 
    return v

if __name__ == "__main__":
    time_list = []
    for i in range(10):
        start_time = time.time()
        maxW, numClass, items = GetDataFromFile(f"INPUT_{i}.txt")
        items_size = len(items)
        print("Test case", i + 1)
        print("Items:",items_size)

        max_val = branchAndBound(maxW, numClass, items)

        print("Ans:", max_val)
        end = round((time.time() - start_time) * 1000, 4)
        print("Running time:", end, "ms")
        time_list.append(end)
        CreateFileOutput(max_val, items, i)
        
    with open("data.txt", "a") as f:
        f.write("Branch and Bound: ")
        f.write("\n".join([str(i) for i in items]))
        f.close()
