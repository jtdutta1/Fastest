import csv
class UnusualCSVStore:
    """
    v0.8
    This is currently in a bare form without any exception handling.
    """
    def __init__(self, data=None, filename=None):
        if data is not None:            
            self.__header__ = data[0]
            self.__data__ = data[1:]
        elif filename is not None:
            self.__filename__ = filename
            data = self.__load_data__()
            self.__header__ = data[0]
            self.__data__ = data[1:]
    
    def __load_data__(self):
        with open(self.__filename__, 'r') as foo:
            data = csv.reader(foo, delimiter=',')
        return data
    
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