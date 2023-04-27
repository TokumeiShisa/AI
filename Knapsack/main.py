import random
from time import *

import brute_force as bf
import brand_and_bound as bb
import local_beam as lb
import genetic_algo as ga

if __name__ == "__main__":
    while True:
        print("1.Brute Force")
        print("2.Branch and Bound")
        print("3.Local Beam")
        print("4.Genetic Algorithm")
        x = int(input())
        if x == 1:
            bf.run()
        if x == 2:
            bb.run()
        if x == 3:
            lb.run()
        if x == 4:
            ga.run()
        else: break
