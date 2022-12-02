import numpy as np
import pandas as pd
import math

class Caches:
    def __init__(self,offsets,setSize,index,tag,hit_time,miss_time,LRU,addrs) -> None:
        self.O = offsets
        self.I = index
        self.setSize = setSize
        self.T = tag
        self.hit_time = hit_time
        self.miss_time = miss_time
        self.LRU = LRU
        self.addrs = pd.DataFrame(addrs,columns=["data_address"])
        
    def __str__(self) -> str:

        return "caches"

    def hit_rate(self,hit,total):
        return hit / total

    def miss_rate(self, miss, total):
        return miss / total
    
    def generate_index(self, index_size):
        index = []
        if index_size == 0:
            return pd.DataFrame()
        for i in range(int(math.pow(2,index_size))):
            index.append(bin(i)[2:].zfill(int(index_size)))
        return pd.DataFrame({'index': index})

    def block_columns(self):
        columns = []
        for i in range(int(math.pow(2,self.O))):
            columns.append("data[" + str(bin(i)[2:].zfill(self.O)) + "]")
        return pd.DataFrame(columns=columns)

    def store_data(self, id, data, df):
        for i in range(int(math.pow(2,self.O))):
            column = "data[" + str(bin(i)[2:].zfill(self.O)) + "]"
            data_addr = data[:self.T+self.I] + bin(i)[2:].zfill(self.O)
            df.at[id,column] = hex(int(data_addr,2))
        return df
    
class DirectMap(Caches):
    def __init__(self,offsets,index,tag,LRU,addrs):
        super(Caches, self).__init__()
        self.O = offsets
        self.I = index
        self.T = tag
        self.hit = 0
        self.miss = 0
        self.LRU = LRU
        self.addrs = pd.DataFrame(addrs,columns=["data_address"])
    
    def DirectMap(self):
        index = self.generate_index(self.I)
        df = pd.DataFrame(columns=["index","valid","Tag"])
        df["index"] = index
        df = df.set_index("index")
        df["valid"] = 0

        df = pd.concat((df,self.block_columns()), axis=1)

        for data in self.addrs["data_address"]:
            id = data[self.T:self.I+self.T]
            tag = data[:self.T]
            valid = df.at[id,"valid"]

            if valid == 0:
                self.miss += 1
                df.at[id,"valid"] = 1
                df.at[id,"Tag"] = tag
                df = self.store_data(id,data,df)
            else:
                if tag != df._get_value(id,"Tag"):
                    self.miss += 1
                    df.at[id,"Tag"] = tag
                    df = self.store_data(id,data,df)
                else:
                    self.hit += 1
        return df
