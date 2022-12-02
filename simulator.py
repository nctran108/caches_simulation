import argparse
import numpy as np
import pandas as pd
import math

from caches_simulation.caches import DirectMap, NSetAssociate

parser = argparse.ArgumentParser(description='Caches simulation')
parser.add_argument('--block_size', type=int, default=1, help="size offset or word id in words")
parser.add_argument('--blocks', type=int, default=16, help="number of lines in words")
parser.add_argument('--associativity', type=int, default=1,
                    help="1 for direct map, 2 for two-way set associative, 4 for four-way, 8 for eight-way, blocks for fully set")
parser.add_argument('--hit_time', type=float, default=3, help='hit time for caches in ns')
parser.add_argument('--miss_time', type=float, default=3, help="miss time for caches in ns")
parser.add_argument('--LRU', type=bool, default=False, help="true to use LRU replacement else set Random replacement")
parser.add_argument('--fileName', type=str, default="sample1.txt", help="file name contain series of byte addresses in text file")
# parser.add_argument('--dtype', type=str, default='bytes', help="type of input data")
arguments = parser.parse_args()
print(arguments)

block_size = arguments.block_size
blocks = arguments.blocks
associativity = arguments.associativity
hit_time = arguments.hit_time
miss_time = arguments.miss_time
LRU = arguments.LRU
fileName = arguments.fileName
#dtype = arguments.dtype


#addr_size = 8
#addrs = np.loadtxt(fileName,dtype=int)
#addrs = [np.binary_repr(s,addr_size) for s in addrs]
# print(addrs)

addr_size = 8
addrs = np.loadtxt(fileName,dtype=str)
addrs = [np.binary_repr(int(s, base=16),addr_size) for s in addrs]
#print(addrs)

offset = int(math.log2(block_size))
setSize = int(blocks/associativity)
indexID = int(math.log2(setSize))
tag = addr_size - indexID - offset

cache_map = NSetAssociate(offset,indexID,tag,associativity,LRU,addrs)

print(cache_map.NSA())
print(cache_map.hit)
print(cache_map.miss)