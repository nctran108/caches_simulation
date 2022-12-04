import pandas as pd
import math
from random import choice
from caches_simulation.caches import Caches

class NSetAssociate(Caches):
    """
    this class generate Set Associate which include Full Set Associate
    then store it in dataframe

    Parameters
    ----------
    offsets : int
    index : int
    tag : int
    associate : int
    LRU : bool
    addrs : ndarray, Iterable, list or Series
    """
    def __init__(self,offsets,index,tag,associate,LRU,addrs):
        super(Caches, self).__init__()
        self.O = offsets
        self.I = index
        self.T = tag
        self.associativity = associate
        self.LRU = LRU
        self.addrs = pd.DataFrame(addrs,columns=["data_address"])
        self.hit = 0
        self.miss = 0
    
    def __str__(self) -> str:
        """
        this function print out all result parameter when use print function
        """
        # get total number of data addresses
        total = len(self.addrs)
        # generate Set Associate function to calculate hits and misses
        self.NSA()
        # call Caches.hit_rate function to calculate hit rate
        hitRate = self.hit_rate(self.hit,total)*100
        # call Caches.miss_rate function to calculate miss rate
        missRate = self.miss_rate(self.miss,total)*100
        # calculate cache size = 2^I * associativity * 2^O
        cacheSize = str(int(math.pow(2,self.I) * self.associativity * math.pow(2,self.O)))
        # create dict with all result above and use the dict to create dataframe
        df = pd.DataFrame.from_dict({"Cache size (Words)" : cacheSize,
                            "Reads" : total,
                            "Hits" : self.hit,
                            "Misses" : self.miss,
                            "Hit Rate (percents)" : hitRate,
                            "Miss Rate (percents)" : missRate}, orient="index")
        # return string of the datafram with no header
        return df.to_string(header=False)

    def NSA(self):
        """
        this function generate Set Associate to calculate hits and misses
        """
        # check if associativity less than number of lines then it is N set Associate
        if self.associativity < math.pow(2,self.I)*self.associativity:
            # generate iterator with [list of set, list of index]
            iterator = self.generate_index(self.I, self.associativity)
            # use iterator to create multi index for dataframe
            setID = pd.MultiIndex.from_product(iterator, names=["set","index"])
            # generate dataframe woth three columns and two indexs
            df = pd.DataFrame(columns=["valid","Tag","count"], index=setID)
        # if associativity equal number of lines then it is Full Set Associate
        else:
            # just create data frame of tree columns
            df = pd.DataFrame(columns=["valid","Tag","count"], index=range(int(math.pow(2,self.I)*self.associate)))
        # set all valid values equal 0
        df["valid"] = 0
        # set all count values equal 0
        df["count"] = 0
        # joint data blocks with dataframe above into one dataframe
        df = pd.concat((df,self.block_columns()), axis=1)

        # loop each data address to perform Set Associate
        for data in self.addrs["data_address"]:
            # get set values from data address
            set = data[self.T:self.I+self.T]
            # get tag value from data address
            tag = data[:self.T]
            # check if associativity less than number of lines then it is N set Associate
            #---------------- N Set Associate ---------------------#
            if self.associativity < math.pow(2,self.I)*self.associativity:
                # get all tag values in the set and store them in a list
                tag_list = list(df.loc[(set,slice(None)),"Tag"].unique())
                # if all valid value in the set equal one then the cache either hit or need to replace if miss
                if df.loc[(set,slice(None)),"valid"].all():
                    # if data tag is in the list then it is a hit
                    if tag in tag_list:
                        # update hit
                        self.hit += 1
                        # increate count value since it hits
                        df.at[(set,tag_list.index(tag)),"count"] += 1
                    # do not found tag which is a miss
                    else:
                        # update miss
                        self.miss += 1
                        # if LRU is true then use LRU replacement method
                        # which replace the least recently use or lowest count value in the set
                        if self.LRU:
                            # find the index in the set that has lowest count value
                            minCount = df["count"].groupby(level=[0]).idxmin()
                            # store that index to i
                            i = minCount.loc[set][1]
                        # use Random replacement when LRU is False
                        else:
                            # choice randomly an integer in index range and set i equal it
                            i = choice(df.index.levels[1].values)
                        # replace data tag into cache tag in row (set,i)
                        df.at[(set,i),"Tag"] = tag
                        # replace memory data into cache data blocks in row (set,i)
                        df = self.store_data((set,i),data,df)
                        # reset count to 0 in row (set,i)
                        df.at[(set,i),"count"] = 0
                # if not all valid values equal 1 then still have empty row to add
                else:
                    # check if data tag is in cache tags
                    # if true then it is a hit
                    if tag in tag_list:
                        # update hit
                        self.hit += 1
                        # increase count by 1
                        df.at[(set,tag_list.index(tag)),"count"] += 1
                    # if the tag is not exist then it is a miss and need to add in
                    else:
                        # check every index of the set
                        # if the valid value of the index equal zero then add date memory to the index
                        # then break the loop
                        for i in range(self.associativity):
                            # check if the valid value equal 0
                            if df.loc[(set,i)]['valid'] == 0:
                                # update miss
                                self.miss += 1
                                # update valid to 1
                                df.at[(set,i),"valid"] = 1
                                # store data tag to chache tag
                                df.at[(set,i),"Tag"] = tag
                                # store data memories to chaches data blocks
                                df = self.store_data((set,i),data,df)
                                break
            # if associativity equal number of lines then it is Full Set Associate
            # ----------------------Full Set Associate-------------------------- # 
            else:
                # if all valid values equal 1 then it can be hit or need to replace
                if df["valid"].all():
                    # if data tag exist in the cache tag then it is a hit
                    if tag in df["Tag"].unique():
                        # update hit
                        self.hit += 1
                        # count up by 1 for the tag
                        df.at[list(df["Tag"].unique()).index(tag),"count"] += 1
                    # if the tag is not exist in cache then it is a miss
                    else:
                        # update miss
                        self.miss += 1
                        # if LRU is True then use LRU replacement
                        if self.LRU:
                            # get the index that has the lowest count
                            i = df["count"].idxmin()
                        # else use Random replacement method
                        else:
                            # choice randomly an integer between index range
                            i = choice(df.index)
                        # replace data tag to chache tag index i
                        df.at[i,"Tag"] = tag
                        # replace data memories to data blocks index i
                        df = self.store_data(i,data,df)
                        # reset count to 0
                        df.at[i,"count"] = 0
                # if not all valid equal 1 then still has line to store
                else:
                    # if data tag is exist in cache tag then it is a hit
                    if tag in df["Tag"].unique():
                        # update hit
                        self.hit += 1
                        # increate count by 1 for the tag
                        df.at[list(df["Tag"].unique()).index(tag),"count"] += 1
                    # else it is a miss
                    else:
                        # update miss
                        self.miss += 1
                        # loop throught all index to find the next valid value equals 0
                        # if find the index then update and break the loop
                        for i in df.index:
                            # if the value equal 0
                            if df.iloc[i]["valid"] == 0:
                                # update valid value to 1
                                df.at[i,"valid"] = 1
                                # add data tag to cache tag
                                df.at[i,"Tag"] = tag
                                # add data mem to cache data blocks
                                df = self.store_data(i,data,df)
                                break
        return df
        