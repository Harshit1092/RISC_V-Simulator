import math

class Cache:
    def __init__(self, cacheSize, blockSize, associativity, ways):
        self.cacheSize = cacheSize
        self.blockSize = blockSize
        self.associativity = associativity
        self.sets = cacheSize / (blockSize * associativity)
        self.numberOfIndexBits = 0
        self.numberOfBlockOffsetBits = int(math.ceil(math.log(blockSize, 2)))

        self.readCount = 0
        self.writeCount = 0
        self.hitCount = 0
        self.missCount = 0

        self.set()

    def set(self):
        # Fully Associative
        if self.associativity == 0:
            self.sets = 1
            self.ways = self.cacheSize // self.blockSize
        # Direct Mapped
        elif self.associativity == 1:
            self.sets = self.cacheSize // self.blockSize
            self.numberOfIndexBits = int(math.ceil(math.log(self.sets, 2)))
            self.ways = 1
        # Set Associative
        else:
            self.sets = self.cacheSize // self.blockSize
            self.sets = self.sets // self.ways
            self.numberOfIndexBits = int(math.ceil(math.log(self.sets, 2)))
        
        # Initialize Cache (cache[index][tag][block, recency])
        self.cache = [dict() for i in range(self.sets)]
        
        
        
    def read(self, address, mem):
        index = self.getIndex(address)
        tag = self.getTag(address)
        offset = self.getOffset(address)
        
        self.readCount = self.readCount + 1
        
        if tag not in self.cache[index].keys():
            self.missCount = self.missCount + 1
            if len(self.cache[index]) != self.ways:
                self.addBlock(address,mem)
            else:
                for cacheTag in self.cache[index].keys():
                    if self.cache[index][cacheTag][1] == 0:
                        self.replaceBlock(index,cacheTag,address,mem)
                        break
        else:
            self.hitCount = self.hitCount + 1
        
        block = self.cache[index][tag][0]
        self.updateRecency(index,tag)
        return block[2 * offset: 2 * offset + 8]
    
    # Write through and No Write Allocate
    def write(self, address, data, mem, type):
        index = getIndex(address)
        tag = getTag(address)
        offset = getOffset(address)

        self.writeCount += 1

        if tag in self.cache[index].keys():
            if type == 4:
                self.cache[index][tag][0] = self.cache[index][tag][0][:2 * offset] + data[8:10] + data[6:8] + data[4:6] + data[2:4] + self.cache[index][tag][0][2 * offset + 8:]
            elif type == 2:
                self.cache[index][tag][0] = self.cache[index][tag][0][:2 * offset] + data[8:10] + data[6:8] + self.cache[index][tag][0][2 * offset + 8:]
            elif type == 1:
                self.cache[index][tag][0] = self.cache[index][tag][0][:2 * offset] + data[8:10] + self.cache[index][tag][0][2 * offset + 8:]
        
        if type == 3:
            mem[address + 3] = data[2:4]
            mem[address + 2] = data[4:6]
            mem[address + 1] = data[6:8]
            mem[address] = data[8:10]
        if type == 1:
            mem[address + 1] = data[6:8]
            mem[address] = data[8:10]
        if type == 0:
            mem[address] = data[8:10]
        return block[2 * offset:2 * offset + 8]
    
    def makeTable(self):
        table = []
        for row in range(self.sets):
            row_data = []
            for tag in self.cache[row].keys():
                index = bin(row)[2:]
                index = "0"*(self.numberOfIndexBits - len(index)) + index
                index = index[:self.numberOfIndexBits]
                tag1 = bin(tag)[2:]
                tag1 = "0"*(32 - self.numberOfBlockOffsetBits - self.numberOfIndexBits) + tag1
                offset = "0"*self.numberOfBlockOffsetBits
                address = int(tag1 + index + offset,2)
                row_data.append([str(hex(address)), "0x" + str(self.cache[row][tag][0]),1,self.cache[row][tag][1],bin(int(self.cache[row][tag][0],16))])
            for i in range(self.ways - len(row_data)):
                row_data.append([0,0,0,0,0])
            table.append(row_data)
        
        return table
