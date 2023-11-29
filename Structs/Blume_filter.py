from math import log
from Structs.bit_array import Bit_array


class Blume_filter:
    def __init__(self,
                 size: int = 100,
                 expected: int = 10):
        super().__init__()
        self.__size = size
        self.__expected = expected

        self.__bitarray = Bit_array(size)
        self.__bitarray.all(0)

        self.number_hash_functions = int((self.__size / self.__expected) * log(2))

    def __hash_function(self, item: str):
        pre_hash = 5381
        for charecter in item:
            pre_hash = ((pre_hash << 5) + pre_hash) + ord(charecter)
        return pre_hash % self.__size

    def _hash(self, item: str, hash_offset: any):
        return self.__hash_function(str(hash_offset) + item)

    def append(self, item):
        item = item.lower()
        for i in range(self.number_hash_functions):
            self.__bitarray[self._hash(item, i)] = 1

    def extend(self, __iterable):
        for item in __iterable:
            self.append(item)

    def check(self, item):
        for i in range(self.number_hash_functions):
            if self.__bitarray[self._hash(item, i)] == 1:
                return True
        return False

    def __contains__(self, item):
        return self.check(item.lower())
