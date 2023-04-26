import random
from time import *
"""https://arpitbhayani.me/blogs/genetic-knapsack
https://www.micsymposium.org/mics_2004/Hristake.pdf"""

"""GLOBAL VARIABLES"""
sets = []
class_num = 2
capacity = 0
population_size = 200
mutation_rate = 0.2
generation = 1000
sets_size = 0
""""""

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
    filename = "TEST/OUTPUT_" + str(i) + ".txt"
    fo = open(filename, "w")
    fo.write(str(max_val) + "\n")
    fo.write(", ".join([str(i) for i in sets]))
    fo.close()
    return filename


def CheckDupe(population, individual):
    for i in population:
        if individual == i: return False 
    return True

def CheckClass(individual):
    class_count = [0] * (class_num + 1)
    class_count[0] = 1
    c = [1] * (class_num + 1)
    for i in range(sets_size):
        if individual[i] == 1 and class_count[sets[i].label] == 0:
            class_count[sets[i].label] = 1
    return class_count == c

def GeneratePopulation(sets):
    population = []
    while len(population) <= population_size:
        individual = []
        for i in range(sets_size):
            individual.append(random.choice([0, 1]))
        if CheckDupe(population, individual) and CheckClass(individual):
            population.append(individual)
    return population
    
def Fitness(individual):
    total_value = 0
    total_weight = 0
    for i in range(sets_size):
        if individual[i] == 1:
            total_value += sets[i].value
            total_weight += sets[i].weight
    if total_weight <= capacity and CheckClass(individual):
        return total_value
    return 0

#Elitist selection 
def Selection(population):
    population.sort(reverse = True, key = Fitness)
    return population[: population_size//2]
    
def Crossover(parents):
    crossover_pt = random.randint(0, sets_size - 1)
    child1 = parents[0][:crossover_pt] + parents[1][crossover_pt:]
    child2 = parents[0][crossover_pt:] + parents[1][:crossover_pt]
    return child1, child2

def Mutate(individual):
    while Fitness(individual) == 0:
        mutate_pt = random.randint(0, sets_size - 1)
        individual[mutate_pt] = 1 - individual[mutate_pt]
    return individual
                
def GeneticAlgo(sets):
    population = GeneratePopulation(sets)
    new_population = []
    for i in range(generation):
        while len(new_population) < len(population):
            parents = random.choices(Selection(population),k = 2)
            child1, child2 = Crossover(parents)
            if random.random() < mutation_rate:
                child1 = Mutate(child1)
            if random.random() < mutation_rate:
                child2 = Mutate(child2)
            new_population.append(child1)
            new_population.append(child2)
        population.extend(new_population)
        population = Selection(population)
    population.sort(reverse = True, key = Fitness)
    return Fitness(population[0]), population[0]
    

if __name__ == "__main__":
    for i in range(1, 10):
        start_time = time()
        capacity, class_num, sets = GetDataFromFile(f"TEST/INPUT_{i}.txt")
        sets_size = len(sets)
        population_size = sets_size * 5
        generation = sets_size * 10
        max_val, ans = GeneticAlgo(sets)
        CreateFileOutput(max_val, ans, i)
        print(i, "Running time", round((time() - start_time) * 1000, 3), "ms")
    
