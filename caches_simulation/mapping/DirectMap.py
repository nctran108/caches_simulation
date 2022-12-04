import pandas as pd
import math
from caches_simulation.caches import Caches

class DirectMap(Caches):
    """
    this class generate DirectMap and store it in dataframe

    Parameters
    ----------
    offsets : int
    index : int
    tag : int
    LRU : bool
    addrs : ndarray, Iterable, list or Series
    """
    def __init__(self,offsets : int,index : int,tag : int,LRU : bool,addrs : list):
        super(Caches, self).__init__()
        self.O = offsets
        self.I = index
        self.T = tag
        self.hit = 0
        self.miss = 0
        self.LRU = LRU
        self.addrs = pd.DataFrame(addrs,columns=["data_address"])
    
    def __str__(self) -> str:
        """
        this function print out all result parameter when use print function
        """
        # get total number of data addresses
        total = len(self.addrs)
        # generate DirectMap function to calculate hits and misses
        self.DM()
        # call Caches.hit_rate function to calculate hit rate
        hitRate = self.hit_rate(self.hit,total)*100
        # call Caches.miss_rate function to calculate miss rate
        missRate = self.miss_rate(self.miss,total)*100
        # calculate cache size = 2^I * 2^O
        cacheSize = str(int(math.pow(2,self.I) * math.pow(2,self.O)))
        # create dict with all result above and use the dict to create dataframe
        df = pd.DataFrame.from_dict({"Cache size (Words)" : cacheSize,
                            "Reads" : total,
                            "Hits" : self.hit,
                            "Misses" : self.miss,
                            "Hit Rate (percents)" : hitRate,
                            "Miss Rate (percents)" : missRate}, orient="index")
        # return string of the datafram with no header
        return df.to_string(header=False)
    
    def DM(self):
        """
        this function generate DirectMap to calculate hits and misses
        """
        # call generate_index function from parent object to create list of binaries for the dataframe index
        index = pd.DataFrame({'index': self.generate_index(self.I)})
        # create dataframe with three columns
        df = pd.DataFrame(columns=["index","valid","Tag"])
        # set index values to dataframe index column
        df["index"] = index
        # set index column as index of the dataframe
        df = df.set_index("index")
        # set all row of value column equal 0
        df["valid"] = 0

        # joint data block column from block_column function with the dataframe above
        df = pd.concat((df,self.block_columns()), axis=1)

        # loop each data address to perform DirectMap
        for data in self.addrs["data_address"]:
            # get index from data
            id = data[self.T:self.I+self.T]
            # get tag from data
            tag = data[:self.T]

            # get valid value from the index
            valid = df.at[id,"valid"]

            # if valid equal 0 then it a miss
            if valid == 0:
                # update miss
                self.miss += 1
                # set valid to 1
                df.at[id,"valid"] = 1
                # store tag into cache
                df.at[id,"Tag"] = tag
                # store memory addresses into data blocks
                df = self.store_data(id,data,df)
            # if valid equal 1 then the cache already have memory addresses 
            else:
                # check if data tag is not the same the cache tag then it is a miss
                if tag != df._get_value(id,"Tag"):
                    # update miss
                    self.miss += 1
                    # store new tag to cache
                    df.at[id,"Tag"] = tag
                    # store new memory addresses to cache data blocks
                    df = self.store_data(id,data,df)
                # if the tag is the same then it is a hit
                else:
                    # update hit
                    self.hit += 1
        return df