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

        self.set_tags = [[0 for x in range(0, self.N)] for x in range(0, self.numCacheLines)]
        self.set_valid = [[0 for x in range(0,self.N)] for x in range(0, self.numCacheLines)]
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
            else:
                #self.tags[index] = tag
                self.valid[index] = 1
                self.miss_count += 1
        else:
            self.tags[index] = tag
            self.valid[index] = 1
            self.miss_count += 1

            self.addresses[index] = address

    def placeAddressAssociative(self, address):
        index = math.floor(address / self.block_size) % self.num_blocks


        set_num = math.floor(address / self.block_size) % (self.numCacheLines + 1)
        tag = int(address / (self.numCacheLines * self.block_size))

        if(tag in self.set_tags[set_num]):
            position = self.set_tags[set_num].index(tag)
            if(self.set_valid[set_num][position]):
                self.hit_count += 1
            else:
                self.set_valid[set_num][position]
                self.miss_count += 1
        else:
            if(0 in self.set_valid[set_num]):
                position = self.set_valid[set_num].index(0)
                self.set_tags[set_num][position] = tag
                self.set_valid[set_num][position] = 1
                self.miss_count += 1
            else:
                self.set_tags[set_num][0] = tag
                self.set_valid[set_num][0] = 1
                self.miss_count += 1


    def printAssCache(self):
        i = 0
        while(i < self.numCacheLines):
            for x in self.set_tags[i]:
                position = self.set_tags[i].index(x)
                {print("set: ", i, "position: ", position, "valid: ",
                    self.set_valid[i][position], "tag: ",
                    self.set_tags[i][position])}
            i+=1

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
    c1.printAssCache()
    c1.placeAddressAssociative(0)
    c1.printAssCache()
    c1.placeAddressAssociative(3)
    c1.printAssCache()
    c1.placeAddressAssociative(11)
    c1.printAssCache()
    c1.placeAddressAssociative(16)
    c1.printAssCache()
    c1.placeAddressAssociative(21)
    c1.printAssCache()
    c1.placeAddressAssociative(11)
    c1.printAssCache()
    c1.placeAddressAssociative(16)
    c1.printAssCache()
    c1.placeAddressAssociative(48)
    c1.printAssCache()
    c1.placeAddressAssociative(16)
    c1.printAssCache()
    c1.placeAddressAssociative(0)

    print("block size: ", c1.block_size)
    print("number of blocks: ", c1.num_blocks)
    print("Associativity: ", c1.N)
    print("offset bit #: ", c1.offset_bits)
    print("index bit #: ", c1.index_bits)
    print("tag bit #: ", c1.tag_bits)
    print("miss count: ", c1.miss_count)
    print("hit count: ", c1.hit_count)
if __name__ == '__main__':
    main()
