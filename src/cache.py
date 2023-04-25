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
        # Set Associative
        else:
            self.sets = self.cacheSize // self.blockSize
            self.sets = self.sets // self.ways
            self.numberOfIndexBits = int(math.ceil(math.log(self.sets, 2)))
        
        self.cache = [dict() for i in range(self.sets)]