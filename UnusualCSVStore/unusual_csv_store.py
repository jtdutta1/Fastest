import csv
class UnusualCSVStore:
    """
    This is currently in a bare form without any exception handling.
    """
    def __init__(self, data=None, filename=None):
        if data is not None:
            self.__data__ = data
        elif filename is not None:
            self.__filename__ = filename
            self.__data__ = self.__load_data__()
    
    def __load_data__(self):
        with open(self.__filename__, 'r') as foo:
            data = csv.reader(foo, delimiter=',')
        return data
    
    def store_data(self, filename="temp.csv", file_mode="w+"):
        with open(filename, file_mode) as foo:
            csvwriter = csv.writer(foo, delimiter=',')
            csvwriter.writerow(self.__data__[0])
            temp = []
            nheaders = len(self.__data__[0])
            count_headers = 0
            for i in self.__data__[1:]:
                l = [str(j) for j in i]
                s = ' '.join(l)
                s = '[' + s + ']'
                temp.append(s)
                count_headers += 1
                if count_headers == nheaders:
                    csvwriter.writerow(temp)
                    temp = []
                    count_headers = 0
    
    # def add_data(self, data):
# 