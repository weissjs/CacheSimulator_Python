import statistics
import sys
import math
from random import randint

class cache:
    #initialize cache with user inputs, and set valids to zero
    #note that block size is in terms of bytes
    def __init__(self,block_size,num_blocks,N, random):
        self.block_size = block_size
        self.num_blocks = num_blocks
        self.N = N
        self.tags = [0] * num_blocks
        self.valid = [0] * num_blocks
        self.offset_bits = math.ceil(math.log2(block_size))
        self.index_bits = math.ceil(math.log2(num_blocks))
        self.tag_bits = 32 - self.offset_bits - self.index_bits
        self.hit_count = 0
        self.miss_count = 0
        self.addresses = [0] * num_blocks
        self.set_num = num_blocks / N
        self.numCacheLines =  math.ceil((self.num_blocks * self.block_size) / (self.block_size * N))
        self.set_addresses =  [[0 for x in range(0, self.N)] for x in range(0, self.numCacheLines)]

        self.set_tags = [[0 for x in range(0, self.N)] for x in range(0, self.numCacheLines)]
        self.set_valid = [[0 for x in range(0,self.N)] for x in range(0, self.numCacheLines)]
        #print("got here")

    #this function will attempt to place the given address and data into
    #the cache. it returns either a 1 for a hit or a zero for a miss
    def placeAddressDirect(self, address):
        # index = address / block size

        index = math.floor(address / self.block_size) % self.num_blocks

        tag = address >> (self.index_bits + self.offset_bits)

        # print("placing: ", address)
        # print("index: ", index)
        # print("tag:  ", tag)
        # print("number of cache lines: ", self.numCacheLines)

        if self.tags[index] == tag:
            if self.valid[index] == 1:
                self.hit_count += 1
            else:
                self.tags[index] = tag
                self.valid[index] = 1
                self.miss_count += 1
        else:
            self.tags[index] = tag
            self.valid[index] = 1
            self.miss_count += 1

        self.addresses[index] = address

    def placeAddressAssociative(self, address):
        index = math.floor(address / self.block_size) % self.num_blocks


        set_num = math.floor(address / self.block_size) % (self.numCacheLines)
        tag = int(address / (self.numCacheLines * self.block_size))

        # print("placing: ", address)
        # print("index: ", index)
        # print("tag:  ", tag)
        # print("set number: ", set_num)
        # print("number of cache lines: ", self.numCacheLines)
        flag = 0
        if(tag in self.set_tags[set_num] and self.set_valid[set_num][self.set_tags[set_num].index(tag)]):
            self.set_addresses[set_num][self.set_tags[set_num].index(tag)] = address
            # print("hit")
            self.hit_count += 1

        else:
            for x in range(0, self.N):
                if(self.set_valid[set_num][x] == 0):
                    position = self.set_valid[set_num].index(0)
                    self.set_tags[set_num][x] = tag
                    self.set_valid[set_num][x] = 1
                    self.miss_count += 1
                    # print("miss at 2")
                    self.set_addresses[set_num][position] = address
                    flag = 1
                    break
            if(flag == 0): # does not find open spot
                position = 0;
                self.set_tags[set_num][0] = tag
                self.set_valid[set_num][0] = 1
                self.miss_count += 1
                # print("miss at 3")
                self.set_addresses[set_num][position] = address

    def printAssCache(self):
        i = 0
        while(i < self.numCacheLines):
            x = 0
            while(x < self.N):
                {print("set: ", i, "position: ", x, "valid: ",
                    self.set_valid[i][x], "tag: ",
                    self.set_tags[i][x], "start memory: ",
                    self.set_addresses[i][x])}
                x+=1
            i+=1
        print()

    def printCache(self):
        i = 0
        for x in self.tags:
            print("index is: ", i, "valid: ", self.valid[i], "tag: ",
                    self.tags[i], "start mem: ", self.addresses[i])
            i+=1
        print()


class test:
    def __init__(self, file_name):
        self.file_name = file_name
        self.input_arr = []
        with open(file_name, 'rt') as myfile:
            for myline in myfile:
                self.input_arr.append(int(myline, 16))


def main():

    num_blocks = int(sys.argv[2])
    block_size = int(sys.argv[1])
    assoc = int(sys.argv[3])


    if(num_blocks < 1 | block_size < 1 | assoc < 1):
        print("ERROR 0: Invalid inputs")
        return

    c1 = cache(block_size, num_blocks, assoc)
    test1 = test(sys.argv[4])

    if(c1.N * c1.numCacheLines != c1.num_blocks):
        print("Error 1: Assoc size does not match")
        return

    if(c1.N < 2):
        i = 0
        while i < len(test1.input_arr):
            c1.placeAddressDirect(test1.input_arr[i])
            #c1.printCache()
            i+=1
        c1.printCache()
    else:
        i = 0
        while i < len(test1.input_arr):
            c1.placeAddressAssociative(test1.input_arr[i])
            #c1.printAssCache()
            i+=1
        c1.printAssCache()

    total = c1.miss_count + c1.hit_count
    miss_rate = (c1.miss_count / total) * 100
    hit_rate = (c1.hit_count / total) * 100

    print("block size: ", c1.block_size)
    print("number of blocks: ", c1.num_blocks)
    print("Associativity: ", c1.N)
    print("offset bit #: ", c1.offset_bits)
    print("index bit #: ", c1.index_bits)
    print("tag bit #: ", c1.tag_bits)
    print("miss count: ", c1.miss_count)
    print("hit count: ", c1.hit_count)
    print("total: ", total)
    print("miss rate: ", miss_rate, "%")
    print("hit rate: ", hit_rate, "%")
if __name__ == '__main__':
    main()
