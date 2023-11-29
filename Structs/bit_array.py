class Bit_array:
    def __init__(self, size: int = 1):
        self.__list = [None] * size
        self.__size = size

    @property
    def size(self):
        return self.__size

    def all(self, value):
        if 0 <= value <= 1:
            for i in range(len(self.__list)):
                self.__list[i] = value

    def __setitem__(self, key: int, value):
        if key > self.__size or value > 1 or value < 0:
            return
        self.__list[key] = value

    def __getitem__(self, item):
        if item > self.__size:
            return
        return self.__list[item]


