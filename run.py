import argparse
import numpy as np
import pandas as pd
import math

from simulator import Simulation, read_int, read_hex

parser = argparse.ArgumentParser(description='Caches simulation')
parser.add_argument('--block_size', type=int, default=1, help="size offset or word id in words")
parser.add_argument('--blocks', type=int, default=16, help="number of lines in words")
parser.add_argument('--associativity', type=int, default=1,
                    help="1 for direct map, 2 for two-way set associative, 4 for four-way, 8 for eight-way, blocks for fully set")
parser.add_argument('--hit_time', type=float, default=0, help='hit time for caches in ns')
parser.add_argument('--miss_time', type=float, default=0, help="miss time for caches in ns")
parser.add_argument('--LRU', action="store_true", default=False, help="true to use LRU replacement else set Random replacement")
parser.add_argument('--fileName', type=str, default="sample1.txt", help="file name contain series of word addresses in text file")
arguments = parser.parse_args()
print(arguments)

def main():
    block_size = arguments.block_size
    blocks = arguments.blocks
    associativity = arguments.associativity
    hit_time = arguments.hit_time
    miss_time = arguments.miss_time
    LRU = arguments.LRU
    fileName = arguments.fileName

    #size = 6
    #addr1 = read_int(fileName,size)
    #print(addr1)
    #sample1_simulation = Simulation(block_size,blocks,associativity,LRU,addr1,size)
    #sample1_simulation.DMTable()
    #sample1_simulation.DMResult()

    #sample1_simulation.NSATable(step=True)
    #sample1_simulation.NASResult()

    size = 20
    addr2 = read_hex()
    simulation = Simulation(block_size,blocks,associativity,LRU,addr2,size)
    #simulation.DMTable()
    #simulation.DMResult()

    #simulation.NSATable(step=True)
    simulation.NASResult()

if __name__ == "__main__":
    main()