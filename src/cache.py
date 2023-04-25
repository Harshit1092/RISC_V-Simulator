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
        return block[2 * offset:2 * offset + 8]