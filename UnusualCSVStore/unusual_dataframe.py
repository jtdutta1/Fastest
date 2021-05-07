import csv
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