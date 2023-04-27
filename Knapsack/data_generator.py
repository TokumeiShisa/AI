import random

class Item:
    def __init__(self, weight, value, label):
        self.weight = weight
        self.value = value
        self.label = label
    def Output(self):
        print(self.weight, "\t", self.value,"\t", self.label, "\n")
    
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
    filename = "Input/INPUT_" + str(i) + ".txt"
    fi = open(filename, "w")
    fi.write(str(capacity) + "\n")
    fi.write(str(_class) + "\n")
    fi.write(", ".join([str(i.weight) for i in sets]) + "\n")
    fi.write(", ".join([str(i.value) for i in sets]) + "\n")
    fi.write(", ".join([str(i.label) for i in sets]))
    fi.close()
    return filename
def run():
    size = [10, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    n_class = [1, 2, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(len(size)):	
        print(CreateFileInput(size[i], n_class[i], i))
        
if __name__ == "__main__":
    run()