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
  
  def branchAndBound(maxW, numClass, items):
    items.sort(key=lambda x: x.ratio, reverse=True)
    n = len(items)
    root = [0, set(), 0, 0, []]
    heap = [(0, root)]
    max = 0
    while(heap):
        ign, node = heapq.heappop(heap)
        level, selectedClasses, value, weight, selectedItems = node
        if ign > -max:
            continue
        if level == n:
            if value > max:
                max = value
                for i in range(n):
                    items[items[i].index].ans = selectedItems[i]
            continue
        curWeight, curValue, curClass = items[level].weight, items[level].value, items[level].label
        if curClass not in selectedClasses:
            selectedClasses.add(curClass)
        bound = value + (maxW - weight) * items[level].ratio
        if (weight + curWeight <= maxW):
            heapq.heappush(heap, (-bound, (level + 1, selectedClasses, value + curValue, weight + curWeight, selectedItems + [1], )))
            heapq.heappush(heap, (-bound, (level + 1, selectedClasses, value, weight, selectedItems + [0])))
        else:
            heapq.heappush(heap, (0, (level + 1, selectedClasses, value, weight, selectedItems + [0])))
    return max
