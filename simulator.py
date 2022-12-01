import argparse
import numpy as np
import pandas as pd

from caches_simulation.caches import Caches

parser = argparse.ArgumentParser(description='Caches simulation')
parser.add_argument('--block_size', type=int, default=1, help="size offset or word id in words")
parser.add_argument('--blocks', type=int, default=16, help="number of lines in words")
parser.add_argument('--associativity', type=int, default=1,
                    help="1 for direct map, 2 for two-way set associative, 4 for four-way, 8 for eight-way, blocks for fully set")
parser.add_argument('--hit_time', type=float, default=3, help='hit time for caches in ns')
parser.add_argument('--miss_time', type=float, default=3, help="miss time for caches in ns")
parser.add_argument('--LRU', type=bool, default=False, help="true to use LRU replacement else set Random replacement")
parser.add_argument('--fileName', type=str, default="sample1.txt", help="file name contain series of byte addresses in text file")
parser.add_argument('--dtype', type=str, default='bytes', help="type of input data")
arguments = parser.parse_args()
print(arguments)

block_size = arguments.block_size
blocks = arguments.blocks
associativity = arguments.associativity
hit_time = arguments.hit_time
miss_time = arguments.miss_time
LRU = arguments.LRU
fileName = arguments.fileName
dtype = arguments.dtype

#addrs = np.loadtxt(fileName,dtype=str)
#addrs = [np.binary_repr(int(s, base=16),20) for s in addrs]
addr_size = 8
addrs = np.loadtxt(fileName,dtype=int)
addrs = [np.binary_repr(s,addr_size) for s in addrs]
addrs = np.array(addrs)
print(addrs)

cache_map = Caches(block_size, blocks, associativity, hit_time,miss_time,LRU,addrs, addr_size)

print(cache_map.DM)
print(cache_map.hit)
print(cache_map.miss)