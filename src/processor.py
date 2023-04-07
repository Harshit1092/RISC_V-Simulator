from collections import defaultdict

class processor:
    def __init__(self,file1):
        self.dataMemory = defaultdict(lambda: '00') # initialising data memory
        self.instructionMemory = defaultdict(lambda: '00') # initialising instruction memory
        self.registers = ['0x00000000' for i in range(32)] # initialising registers
        self.registers[2]='0x7FFFFFF0' # sp
        self.registers[3]='0x10000000' # gp
        self.loadProgramMemory(file1) # read program.mc file to load our data and intruction memory
        self.pipeliningEnabled = False # knob for pipelining
        self.PC_next = 0 # Next PC address
        self.PC_offset = 0 # PC offset
        self.terminate = False # flag to terminate the program
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
        self.Total_instructions=0 # Total number of instructions executed
        self.ALU_instructions=0 # Total number of ALU instructions executed
        self.memory_instructions=0  # Total number of memory instructions executed
        self.control_instructions=0 # Total number of control instructions executed
        self.branch_misprediction=0 # Total number of branch mispredictions
        

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
                        instruction = '0x' + (10 - len(instruction))*'0' + instruction[2:]
                        self.dataMemory[idx] = instruction[8:10]
                        self.dataMemory[idx+1] = instruction[6:8]
                        self.dataMemory[idx+2] = instruction[4:6]
                        self.dataMemory[idx+3] = instruction[2:4]
        except:
            print(f"Error: Unable to open {file1} file.\n")
            exit(1)

    # Function to print the contents of the data memory in data.txt file and register values in reg.txt file
    def writeDataMemory(self):
        try:
            fp = open('data.txt', 'w')
            output = []
            for i in range(int('10000000', 16), int('10007ffd', 16), 4):
                output.append(hex(i) + ' 0x' + self.dataMemory[i] + self.dataMemory[i+1] + self.dataMemory[i+2] + self.dataMemory[i+3] + '\n')
            fp.writelines(output)
            fp.close()
        except:
            print("Error: Unable to open data.txt file for writing.\n")
            exit(1)

        try:
            fp = open('reg.txt', 'w')
            output = []
            for i in range(32):
                output.append('x' + str(i) + ' ' + self.registers[i] + '\n')
            fp.writelines(output)
            fp.close()
        except:
            print("Error: Unable to open reg.txt file for writing.\n")
            exit()


    def generateControlSignals(self, *args):
        self.registerWrite = args[0]
        self.MuxB_select = args[1]
        self.MuxY_select = args[2]
        self.mem_write = args[3]
        self.mem_read = args[4]
        self.MuxMA_select = args[5]
        self.MuxPC_select = args[6]
        self.MuxINC_select = args[7]
        self.numBytes = args[8]

    # Fetch instruction from instruction memory
    def fetch(self, state, *args):
        if state.stall == True:
            return
        state.IR = '0x' + self.instructionMemory[state.PC + 3] + self.instructionMemory[state.PC + 2] + self.instructionMemory[state.PC + 1] + self.instructionMemory[state.PC]
    
    # Decode instruction and identify the operation and operands
    def decode(self, state, *args):
        if state.stall == True:
            return False, 0, False, 0
        if state.IR == '0x401080BB':
            self.terminate = True
            state.stall = True
            return False, 0, False, 0
        
        for i in range(15):
            state.ALU_OP[i] = 0

        instruction = bin(int(state.IR[2:], 16))[2:]
        instruction = (32-len(instruction))*'0' + instruction

        # Opcode and func3
        opcode = int(instruction[25:32], 2)
        func3 = int(instruction[17:20], 2)

        # R Format
        if(opcode == 51):
            pass