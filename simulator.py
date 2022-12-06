import numpy as np
import math

from caches_simulation.mapping.NSetAssociate import NSetAssociate
from caches_simulation.mapping.DirectMap import DirectMap

class Simulation(object):
    """
    this class use to simulate caches 

    Parameter
    ---------
    block_size : int
    blocks : int
    associativity : int
    LRU : bool
    addrs : list
    size : int
    """
    def __init__(self, block_size: int, blocks: int, associativity: int, LRU: bool, addrs: list, size : int) -> None:
        self.block_size = block_size
        self.blocks = blocks
        self.checkAssociativity(associativity)
        self.associativity = associativity
        self.LRU = LRU
        self.addrs = addrs     
        self.size = size
    
    def checkAssociativity(self,associativity):
        """
        This function check if Associativity is valid to use or not
        """
        if isPowerOfTwo(associativity):
            if associativity > self.blocks:
                print("NumberValidError: The associativity value greater than number of lines(blocks)")
                exit()
        else:
            print("NumberValidError: The associativity value is not power of two")
            exit()

    def DirectMap(self):
        """
        This function build DirectMap cache and return DirectMap object
        """
        offset = int(math.log2(self.block_size))
        index = int(math.log2(self.blocks))
        tag = self.size - index - offset
        dm = DirectMap(offset,index,tag,self.LRU,self.addrs)
        return dm

    def DMTable(self,step: bool=False):
        """
        This function print out DirectMap table result
        """
        print(self.DirectMap().DM(step))

    def DMResult(self):
        """
        This Function print out DirectMap result
        """
        print(self.DirectMap())
    
    def NSetAssociate(self):
        """
        This function build DirectMap cache and return N Set Associate object
        """
        offset = int(math.log2(self.block_size))
        setID = int(self.blocks/self.associativity)
        index = int(math.log2(setID))
        tag = self.size - index - offset
        setAssociate = NSetAssociate(offset,index,tag,self.associativity,self.LRU,self.addrs)
        return setAssociate

    def NSATable(self,step: bool=False):
        """
        This function print out N Set Associate table result
        """
        print(self.NSetAssociate().NSA(step))

    def NASResult(self):
        """
        This Function print out N Set Associate result
        """
        print(self.NSetAssociate())


# get word addresses from sample1.txt
def read_int(fileName: str = "sample1.txt",size : int=6) -> np.array:
    addrs = np.loadtxt(fileName,dtype=int)
    addrs = [np.binary_repr(s,size) for s in addrs]
    return addrs

# get word addresses from addresses.txt
def read_hex(fileName: str = "addresses.txt", size : int = 20) -> np.array:
    addrs = np.loadtxt(fileName,dtype=str)
    addrs = [np.binary_repr(int(s, base=16),size) for s in addrs]
    return addrs

# Function to check
# if x is power of 2
def isPowerOfTwo(n: int) -> bool:
    return (math.ceil(math.log2(n)) == math.floor(math.log2(n)))
