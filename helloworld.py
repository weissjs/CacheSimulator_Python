import statistics
import sys
import math

class cache:
    #initialize cache with user inputs, and set valids to zero
    #note that block size is in terms of bytes
    def __init__(self,block_size,num_blocks,N):
        self.block_size = block_size
        self.num_blocks = num_blocks
        self.N = N
        self.tags = [0] * num_blocks * N
        self.valid = [0] * num_blocks * N
        self.offset_bits = math.ceil(math.log2(block_size))
        self.index_bits = math.ceil(math.log2(num_blocks))
        self.tag_bits = 32 - self.offset_bits - self.index_bits
        self.hit_count = 0
        self.miss_count = 0
        self.addresses = [0] * num_blocks
        self.set_num = num_blocks / N
        #print("got here")

    #this function will attempt to place the given address and data into
    #the cache. it returns either a 1 for a hit or a zero for a miss
    def placeAddressDirect(self, address):
        # index = address / block size

        index = math.floor(address / self.block_size) % self.num_blocks

        tag = address >> (self.index_bits + self.offset_bits)
        if self.tags[index] == tag:
            if self.valid[index] == 1:
                self.hit_count += 1
            elif self.valid[index] == 0:
                self.tags[index] = tag
                self.valid[index] = 1
                self.miss_count += 1
        else:
            self.tags[index] = tag
            self.valid[index] = 1
            self.miss_count += 1

        self.addresses[index] = address
    def placeAddressAssociative(self, address, N):
        numCacheLines = (self.num_blocks * self.block_size) / (self.block_size * N)
        index = math.floor(address / self.block_size) % self.num_blocks

        set_num = math.floor(address / self.block_size) % numCacheLines
        tag = address / (numCacheLines * block_size)



    def printCache(self):
        i = 0
        for x in self.tags:
            print("index is: ", i, "valid: ", self.valid[i], "tag: ",
                    self.tags[i], "start mem: ", self.addresses[i])
            i+=1



class test:
    def __init__(self, file_name):
        self.file_name = file_name
        self.input_arr = []
        with open(file_name, 'rt') as myfile:
            for myline in myfile:
                self.input_arr.append(int(myline, 16))

def main():
    c1 = cache(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))


    test1 = test(sys.argv[4])

    print(test1.input_arr)
    c1.printCache()
    c1.placeAddressDirect(0)
    c1.printCache()
    c1.placeAddressDirect(3)
    c1.printCache()
    c1.placeAddressDirect(11)
    c1.printCache()
    c1.placeAddressDirect(16)
    c1.printCache()
    c1.placeAddressDirect(21)
    c1.printCache()
    c1.placeAddressDirect(11)
    c1.printCache()
    c1.placeAddressDirect(16)
    c1.printCache()
    c1.placeAddressDirect(48)
    c1.printCache()
    c1.placeAddressDirect(16)
    c1.printCache()

    print("block size: ", c1.block_size)
    print("number of blocks: ", c1.num_blocks)
    print("Associativity: ", c1.associativity)
    print("offset bit #: ", c1.offset_bits)
    print("index bit #: ", c1.index_bits)
    print("tag bit #: ", c1.tag_bits)
    print("miss count: ", c1.miss_count)
    print("hit count: ", c1.hit_count)
if __name__ == '__main__':
    main()
