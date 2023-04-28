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
