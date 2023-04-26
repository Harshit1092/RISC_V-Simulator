
import math
import random

class Cache:
    def __init__(self, cacheSize, blockSize, associativity, ways,replacementPolicy):
        self.cacheSize = cacheSize
        self.blockSize = blockSize
        self.associativity = associativity
        self.ways = ways
        self.sets = 0
        self.numberOfIndexBits = 0
        self.numberOfBlockOffsetBits = int(math.ceil(math.log(blockSize, 2)))
        self.replacementPolicy=replacementPolicy # 0 for LRU,1 for FIFO,2 for random,3 for LFU ,4 for LIFO
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
        
        # Initialize Cache (cache[index][tag][block, recency,islastin,First,frequency,leastfrequency])
        self.cache = [dict() for i in range(self.sets)]
        
    def getIndex(self,addr):
        addr=hex(addr)
        addr=bin(int(addr[2:],16))[2:]
        addr=(32-len(addr))*'0'+addr
        if self.numberOfIndexBits==0:
            return 0
        else:
            return int(addr[-(self.numberOfBlockOffsetBits+self.numberOfIndexBits):-self.numberOfBlockOffsetBits],2)

    def getTag(self,addr):
        addr=hex(addr)
        addr=bin(int(addr[2:],16))[2:]
        addr=(32-len(addr))*'0'+addr
        return int(addr[:-(self.numberOfBlockOffsetBits+self.numberOfIndexBits)],2)
    
    def getOffset(self,addr):
        addr=hex(addr)
        addr=bin(int(addr[2:],16))[2:]
        addr=(32-len(addr))*'0'+addr
        return int(addr[-(self.numberOfBlockOffsetBits):],2)
    
    def updateFirstin(self,ind):
        for cacheTag in self.cache[ind].keys():
            self.cache[ind][cacheTag][3]-=1

    def updateleastfrequency(self,ind,tag):
        least=self.cache[ind][tag][4]
        for cache_tag in self.cache[ind].keys():
            least=min(least,self.cache[ind][cache_tag][4])
        for cache_tag in self.cache[ind].keys():
            self.cache[ind][cache_tag][5]=least

    def replaceBlock(self,ind,cache_tag,addr,mem):
        self.cache[ind].pop(cache_tag)
        tag=self.getTag(addr)
        self.cache[ind][tag]=['',self.ways-1,1,len(self.cache[ind]),0,0]
        self.updateFirstin(ind)
        for cache_tag in self.cache[ind].keys():
            self.cache[ind][cache_tag][5]=0
        addr=(addr//self.blockSize)*self.blockSize
        for i in range(self.blockSize):
            self.cache[ind][tag][0] += mem[addr+i]

    def updateRecency(self,ind,tag):
        self.cache[ind][tag][1]=self.ways
        for cache_tag in self.cache[ind].keys():
            if self.cache[ind][cache_tag][1]!=0:
                self.cache[ind][cache_tag][1]-=1

    def addBlock(self,addr,mem):
        ind=self.getIndex(addr)
        tag=self.getTag(addr)
        for cacheTag in self.cache[ind].keys():
            self.cache[ind][cacheTag][2]==0
        self.cache[ind][tag]=['',self.ways-1,1,len(self.cache[ind]),0,0]
        for cache_tag in self.cache[ind].keys():
            self.cache[ind][cache_tag][5]=0
        addr=(addr//self.blockSize)*self.blockSize
        for i in range(self.blockSize):
            self.cache[ind][tag][0] += mem[addr+i]
    
    def read(self, address, mem):
        index = self.getIndex(address)
        tag = self.getTag(address)
        offset = self.getOffset(address)

        guiData = {}
        guiData['action'] = 'read'
        guiData['index'] = index
        guiData['offset'] = offset
        guiData['status'] = 'found'

        self.readCount = self.readCount + 1
        
        if tag not in self.cache[index].keys():
            self.missCount = self.missCount + 1
            if len(self.cache[index]) != self.ways:
                self.addBlock(address,mem)
                guiData['status'] = 'added'
            else:
                if self.associativity==1:
                    for cacheTag in self.cache[index].keys():
                        if self.cache[index][cacheTag][1] == 0:
                            self.replaceBlock(index,cacheTag,address,mem)
                            guiData['status'] = 'replaced'
                            guiData['victim'] = cacheTag
                            break
                else:
                    if self.replacementPolicy==0:#LRU
                        for cacheTag in self.cache[index].keys():
                            if self.cache[index][cacheTag][1] == 0:
                                self.replaceBlock(index,cacheTag,address,mem)
                                guiData['status'] = 'replaced'
                                guiData['victim'] = cacheTag
                                break
                    elif self.replacementPolicy==4:#LIFO
                        for cacheTag in self.cache[index].keys():
                            if self.cache[index][cacheTag][2] == 1:
                                self.replaceBlock(index,cacheTag,address,mem)
                                guiData['status'] = 'replaced'
                                guiData['victim'] = cacheTag
                                break
                    elif self.replacementPolicy==2:#random
                        x=len(self.cache[index])
                        cacheTag=random.choice(list(self.cache[index]))
                        guiData['status'] = 'replaced'
                        guiData['victim'] = cacheTag
                        self.replaceBlock(index,cacheTag,address,mem)
                    elif self.replacementPolicy==1:#FIFO
                        for cacheTag in self.cache[index].keys():
                            if self.cache[index][cacheTag][3] == 0:
                                self.replaceBlock(index,cacheTag,address,mem)
                                guiData['status'] = 'replaced'
                                guiData['victim'] = cacheTag
                                break
                    else: #LFU
                        for cacheTag in self.cache[index].keys():
                            if self.cache[index][cacheTag][4] == self.cache[index][cacheTag][5]:
                                self.replaceBlock(index,cacheTag,address,mem)
                                guiData['status'] = 'replaced'
                                guiData['victim'] = cacheTag
                                break
        else:
            self.hitCount = self.hitCount + 1
            self.cache[index][tag][4]+=1
            self.updateleastfrequency(index,tag)


        block = self.cache[index][tag][0]
        self.updateRecency(index,tag)
        return block[2 * offset: 2 * offset + 8], guiData
    
    # Write through and No Write Allocate
    def write(self, address, data, mem, type):
        index = self.getIndex(address)
        tag = self.getTag(address)
        offset = self.getOffset(address)

        guiData = {}
        guiData['action'] = 'write'
        guiData['index'] = index
        guiData['offset'] = offset
        guiData['status'] = 'not found'

        self.writeCount += 1

        if tag in self.cache[index].keys():
            guiData['status'] = 'found'
            if type == 4:
                self.cache[index][tag][0] = self.cache[index][tag][0][:2 * offset] + data[8:10] + data[6:8] + data[4:6] + data[2:4] + self.cache[index][tag][0][2 * offset + 8:]
            elif type == 2:
                self.cache[index][tag][0] = self.cache[index][tag][0][:2 * offset] + data[8:10] + data[6:8] + self.cache[index][tag][0][2 * offset + 8:]
            elif type == 1:
                self.cache[index][tag][0] = self.cache[index][tag][0][:2 * offset] + data[8:10] + self.cache[index][tag][0][2 * offset + 8:]
        
        if type == 4:
            mem[address + 3] = data[2:4]
            mem[address + 2] = data[4:6]
            mem[address + 1] = data[6:8]
            mem[address] = data[8:10]
        if type == 2:
            mem[address + 1] = data[6:8]
            mem[address] = data[8:10]
        if type == 1:
            mem[address] = data[8:10]
        
        return guiData
    
    def makeCacheTable(self):
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
                row_data.append(["Tag: " + str(hex(self.getTag(address))), "Index: " + str(hex(self.getIndex(address)))])
            while len(row_data) < self.ways:
                row_data.append([0,0,0])
            table.append(row_data)
        
        return table

    