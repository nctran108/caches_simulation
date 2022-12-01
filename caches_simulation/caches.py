import numpy as np
import pandas as pd
import math

class Caches:
    def __init__(self,block_size, blocks, associativity, hit_time, miss_time, LRU, addrs, data_size) -> None:
        self.O = math.log2(block_size*4)
        self.set = blocks/associativity
        self.I = math.log2(self.set)
        self.T = data_size - self.I - self.O
        self.hit = 0
        self.hit_time = hit_time
        self.miss = 0
        self.miss_time = miss_time
        self.LRU = LRU
        self.addrs = pd.DataFrame(addrs,columns=["data_address"])
        self.DM = self.DirectMap()
        
    def __str__(self) -> str:

        return "caches"

    def hit_rate(self):
        pass

    def miss_rate(self):
        return 1 - self.hit_rate()

    def hits(self):
        pass

    def misses(self):
        return len(self.addrs) - self.hits()

    def DirectMap(self):
        index = self.generate_index(self.I)
        df = pd.DataFrame(columns=["index","valid","Tag"])
        df["index"] = index
        df = df.set_index("index")
        df["valid"] = 0
        
        for i in range(int(math.pow(2,self.O))):
            data = "data[" + str(bin(i)[2:].zfill(int(self.O))) + "]"
            df[data] = np.nan
        for data in self.addrs["data_address"]:
            id = data[int(self.O):int(self.O+self.I)]
            tag = data[int(self.O+self.I):]
            valid = df.at[id,"valid"]
            #print(valid)
            if valid == 0:
                self.miss += 1
                df.at[id,"valid"] = 1
                df.at[id,"Tag"] = tag
                for i in range(int(math.pow(2,self.O))):
                    d = "data[" + str(bin(i)[2:].zfill(int(self.O))) + "]"
                    data_addr = data[int(self.O):] + bin(i)[2:].zfill(int(self.O))
                    df.at[id,d] = hex(int(data_addr,2))
            else:
                if tag != df._get_value(id,"Tag"):
                    self.miss += 1
                    df.at[id,"Tag"] = tag
                    for i in range(int(math.pow(2,self.O))):
                        d = "data[" + str(bin(i)[2:].zfill(int(self.O))) + "]"
                        data_addr = data[int(self.O):] + bin(i)[2:].zfill(int(self.O))
                        df.at[id,d] = hex(int(data_addr,2))
                else:
                    self.hit += 1
        return df
    
    def generate_index(self, index_size):
        index = []
        if index_size == 0:
            return pd.DataFrame()
        for i in range(int(math.pow(2,index_size))):
            index.append(bin(i)[2:].zfill(int(index_size)))
        return pd.DataFrame({'index': index})
