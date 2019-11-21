import statistics
import sys
import math

class cache:
    #initialize cache with user inputs, and set valids to zero
    #note that block size is in terms of bytes
    def __init__(self,block_size,num_blocks,associativity):
        self.block_size = block_size
        self.num_blocks = num_blocks
        self.associativity = associativity
        self.tags = [0] * num_blocks
        self.valid = [0] * num_blocks
        self.offset_bits = math.ceil(math.log2(block_size))
        self.index_bits = math.ceil(math.log2(num_blocks))
        self.tag_bits = 32 - self.offset_bits - self.index_bits
    def printCache(self):
        for

    def placeAddress(self):
        print(blank)

class test:
    def __init__(self, file_name):
        self.file_name = file_name
        self.input_arr = []
        with open(file_name, 'rt') as myfile:
            i = 0
            for myline in myfile:
                self.input_arr.append(int(myline, 16))
                i = i + 1


c1 = cache(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
print("block size: ", c1.block_size)
print("number of blocks: ", c1.num_blocks)
print("Associativity: ", c1.associativity)
print("offset bit #: ", c1.offset_bits)
print("index bit #: ", c1.index_bits)
print("tag bit #: ", c1.tag_bits)
test1 = test(sys.argv[4]).input_arr
print(test1)
