from collections import defaultdict

class processor:
    def __init__(self,file1):
        self.dataMemory = defaultdict(lambda: '00') # initialising data memory
        self.instructionMemory = defaultdict(lambda: '00') # initialising instruction memory
        self.registers = ['0x00000000' for i in range(32)] # initialising registers
        self.registers[2]='0x7FFFFFF0' # sp
        self.registers[3]='0x10000000' # gp
        self.loadProgramMemory(file1) # read program.mc file to load our data and intruction memory
        self.pipelingEnabled = False # knob for pipelining
        self.PC_next = 0 # Next PC address
        self.PC_offset = 0 # PC offset

        # Control Signals
        self.registerWrite=False
        self.MuxB_select=False
        self.MuxY_select=False
        self.mem_write=False
        self.mem_read=False
        self.MuxMA_select=False
        self.MuxPC_select=False
        self.MuxINC_select=False
        self.numBytes=0
        # Counts
        self.Total_instructions=0
        self.ALU_instructions=0
        self.memory_instructions=0
        self.control_instructions=0
        self.branch_misprediction=0
        

    # Function to populate the instruction & data memory using the program.mc file    
    def loadProgramMemory(self, file1):
        try:
            fp = open(file1, 'r')
            flag = True
            for line in fp:
                tmp = line.split()
                if len(tmp) == 2:
                    address, instruction = tmp[0], tmp[1]
                    if(instruction == '$'):
                        flag = False
                        continue
                    if(flag):
                        idx = int(address[2:], 16)
                        self.instructionMemory[idx] = instruction[8:10]
                        self.instructionMemory[idx+1] = instruction[6:8]
                        self.instructionMemory[idx+2] = instruction[4:6]
                        self.instructionMemory[idx+3] = instruction[2:4]
                    else:
                        idx = int(address[2:], 16)
                        while len(instruction) < 10:
                            instruction = '0x' + '0' + instruction[2:]
                        self.dataMemory[idx] = instruction[8:10]
                        self.dataMemory[idx+1] = instruction[6:8]
                        self.dataMemory[idx+2] = instruction[4:6]
                        self.dataMemory[idx+3] = instruction[2:4]
        except:
            print(f'Error: Unable to open {file1} file.')
            exit(1)

    # Function to print the contents of the data memory

        


