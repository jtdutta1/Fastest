import csv
class UnusualDataframe:
    """
    v1
    General purpose class for handling this unusual datatype of yours. 
    """
    def __init__(self, data=None, filename=None, header=None, store_header=True):
        if data is not None:
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
        elif filename is not None:
            self.__filename__ = filename
            data = self.__load__data__()
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
    
    def __load__data__(self):
        # Read the entire file
        with open(self.__filename__, 'r') as foo:
            csvreader = csv.reader(foo, delimiter=',')
            data = []
            for row in csvreader:
                temp_row = []
                for column in row:
                    # print("Column: \n", column)
                    start = column.find('[')
                    # print(start)
                    if start == -1:
                        temp_row.append(column)
                    else:
                        l = column[1:-1].split(' ')
                        # Convert to individual datatypes
                        try:
                            l2 = [int(i) for i in l]
                        except ValueError:
                            # print(l)
                            l2 = [float(i) for i in l]
                        temp_row.append(l)
                data.append(temp_row)
            return data