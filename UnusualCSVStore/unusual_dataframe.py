import csv
class UnusualCSVStore:
    """
    v0.8
    This is currently in a bare form without any exception handling.
    """
    def __init__(self, data):
        self.__header__ = data[0]
        self.__data__ = data[1:]
    
    def store_data(self, filename="temp.csv", file_mode="w+"):
        with open(filename, file_mode) as foo:
            foo.write(self.__repr__())
    
    def add_data(self, data):
        assert(len(data) == len(self.__header__))
        self.__data__.extend(data)
    
    def __repr__(self):
        data = ''
        data += ','.join(self.__header__) + '\n'
        temp = []
        nheaders = len(self.__header__)
        count_headers = 0
        for i in self.__data__:
            l = [str(j) for j in i]
            s = ' '.join(l)
            s = '[' + s + ']'
            temp.append(s)
            count_headers += 1
            if count_headers == nheaders:
                data += ','.join(temp) + '\n'
                temp = []
                count_headers = 0
        return data

    def __str__(self):
        return self.__repr__()

class UnusualDataframe:
    """
    v1
    General purpose class for handling this unusual datatype of yours. 
    """
    def __init__(self, data, header=None, store_header=True):
        if header is not None:
            self.__header__ = header
            self.__data__ = data
        else:
            if store_header:
                self.__header__ = data[0]
                self.__data__ = data[1:]
            else:
                self.__header__ = None
                self.__data__ = data
        
    def __repr__(self):
        data = ''
        if self.__header__ is not None:
            data += ','.join(self.__header__) + '\n'
        temp = []
        # nheaders = len(self.__header__)
        # count_headers = 0
        for i in self.__data__:
            for j in i:
                l = [str(k) for k in j]
                s = ' '.join(l)
                s = '[' + s + ']'
                temp.append(s)
            # if count_headers == nheaders:
            data += ','.join(temp) + '\n'
            temp = []
        return data
    
    def add_data(self, data):
        # assert(len(data) == len(self.__header__))
        self.__data__.extend(data)
    
    def store_data(self, filename="temp.csv", file_mode="w+"):
        with open(filename, file_mode) as foo:
            foo.write(self.__repr__())