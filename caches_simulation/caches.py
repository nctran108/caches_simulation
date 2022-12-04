import pandas as pd
import math

class Caches(object):
    """
    this class contain all function that need to generate and calculate caches

    Parameters
    ----------
    offsets : int
    index : int
    tag : int
    LRU : bool
    addrs : ndarray, Iterable, list or Series
    """
    def __init__(self,offsets : int,index: int, tag : int,LRU: bool, addrs : None) -> None:
        self.O = offsets
        self.I = index
        self.T = tag
        self.LRU = LRU
        self.addrs = pd.DataFrame(addrs,columns=["data_address"])

    def hit_rate(self,hit: int,total: int) -> float:
        """
        this function calculate hit rate by divide hit over total
        """
        return round(float(hit) / total,4)

    def miss_rate(self, miss, total) -> float:
        """
        this function calculate miss rate by divide miss over total
        """
        return round(float(miss) / total,4)
    
    def generate_index(self, index_size : int, associativity: int = 1) -> list:
        """
        this function create a list of binary for number of lines for DirectMap, or generate set and index of each set
        for full set associate, no need to generate index
        """
        # create empty list
        index = []
        
        # check if index_size equal 0 then return empty dataframe
        if index_size == 0:
                return pd.DataFrame()
        
        # associativity equal 1 is DirectMap
        if associativity == 1:
            # create a list of binary base on index size
            for i in range(int(math.pow(2,index_size))):
                index.append(bin(i)[2:].zfill(int(index_size)))
        # if associativity greater than 1 then it is Set associate
        elif associativity > 1:
            # create a list of binary for set
            setID = [bin(i)[2:].zfill(int(index_size)) for i in range(int(math.pow(2,index_size)))]
            # create list index for each set
            id = [i for i in range(associativity)]
            # store both list into index list
            index = [setID, id]
        return index

    def block_columns(self) -> pd.DataFrame:
        """
        this function create datafram that contain all block data 
        """
        columns = []
        # generate binary of the offsets and convert it in this format data[bin]
        # then append each string to the list
        for i in range(int(math.pow(2,self.O))):
            columns.append("data[" + str(bin(i)[2:].zfill(self.O)) + "]")
        # create dataframe base of the list create above and return it
        return pd.DataFrame(columns=columns)

    def store_data(self, id : int, data : str, df : pd.DataFrame) -> pd.DataFrame:
        """
        this function create hex data to store into data blocks
        """
        # generate loop to get each column name in dataframe
        for i in range(int(math.pow(2,self.O))):
            # create column name with this format data[bin] base on number of offsets
            column = "data[" + str(bin(i)[2:].zfill(self.O)) + "]"
            # only have one block data if offset equal 0
            if self.O == 0:
                # since offset equal 0 then the data need to store equal original data
                data_addr = data
            else:
                # if offset greater than 0 then store data will equal data[tag+index] + offset
                # for example if offset = 1 then has two data that need to store which are data[tag+index] + "0" and data[tag+index] + "1"
                data_addr = data[:self.T+self.I] + bin(i)[2:].zfill(self.O)
            # store all data address into each data column
            df.at[id,column] = hex(int(data_addr,2))
        return df
