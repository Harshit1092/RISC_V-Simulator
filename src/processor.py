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


    def generateControlSignals(state, *args):
        state.registerWrite = args[0]
        state.MuxB_select = args[1]
        state.MuxY_select = args[2]
        state.mem_write = args[3]
        state.mem_read = args[4]
        state.MuxMA_select = args[5]
        state.MuxPC_select = args[6]
        state.MuxINC_select = args[7]
        state.numBytes = args[8]

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
            state.ALU_OP[i] = False

        instruction = bin(int(state.IR[2:], 16))[2:]
        instruction = (32-len(instruction))*'0' + instruction

        # Opcode and func3
        opcode = instruction[25:32]
        func3 = instruction[17:20]

        # R Format
        if(opcode == '0110011'):
            self.generateControlSignals(state, True, False, False, False, False, True, False, 4)
            state.RD = instruction[20:25]
            state.RS1 = instruction[12:17]
            state.RS2 = instruction[7:12]
            func7 = int(instruction[0:7], 2)

            # ADD/SUB/MUL
            if(func3 == '000'):
                # ADD Instruction
                if(func7 == '0000000'):
                    state.ALU_OP[0] = True
                # SUB Instruction
                elif(func7 == '0000020'):
                    state.ALU_OP[1] = True
                # MUL Instruction
                elif(func7 == '0000001'):
                    state.ALU_OP[3] = True
                else:
                    print("Error: Unknown instruction")
                    exit(1)
            # AND
            elif(func3 == '007'):
                # AND Instruction
                if(func7 == '0000000'):
                    state.ALU_OP[10] = True
                else:
                    print("Error: Unknown instruction")
                    exit(1)
            # OR/REM
            elif(func3 == '006'):
                # OR Instruction
                if(func7 == '0000000'):
                    state.ALU_OP[9] = True
                # REM Instruction
                elif(func7 == '0000001'):
                    state.ALU_OP[4] = True
            # SLL
            elif(func3 == '001'):
                # SLL Instruction
                if(func7 == '0000000'):
                    state.ALU_OP[6] = True
                else:
                    print("Error: Unknown instruction")
                    exit(1)
            # SLT
            elif(func3 == '002'):
                # SLT Instruction
                if(func7 == '0000000'):
                    state.ALU_OP[11] = True;
                else:
                    print("Error: Unknown instruction")
                    exit(1)
            # SRL/SRA
            elif(func3 == '005'):
                # SRL Instruction
                if(func7 == '0000000'):
                    state.ALU_OP[8] = True
                # SRA Instruction
                elif(func7 == '0000002'):
                    state.ALU_OP[7] = True
                else:
                    print("Error: Unknown instruction")
                    exit(1)
            

                
    def execute(self,state):
        if (state.stall):
            return
        InA=state.RA
        if state.MuxB_select:
            InB=state.Imm
        InB=state.RB

        for i in range(15):
            if(state.ALU_OP[i]==1):
                if i==0:
                    state.RZ=InA+InB
                    break
                elif i==1:
                    state.RZ=InA-InB
                    break
                elif i==2:
                    if(InB!=0):
                        state.RZ=InA/InB
                    break
                elif i==3:
                    state.RZ=InA*InB
                    break
                elif i==4:
                    if(InB!=0):
                        state.RZ=InA-InB
                    break
                elif i==5:
                    state.RZ=InA^InB
                    break
                elif i==6:
                    if (InB>=0):
                        state.RZ=InA<<InB
                    break
                elif i==7:
                    #please write sra code here.
                    break
                elif i==8:
                    if (InB>=0):
                        state.RZ=InA>>InB
                    break
                elif i==9:
                    state.RZ=InA|InB
                    break
                elif i==10:
                    state.RZ=InA&InB
                    break
                elif i==11:
                    if(InA<InB):
                        state.RZ=1
                    else:
                        state.RZ=0
                    state.MuxINC_select=state.RZ
                    break
                elif i==12:
                    if(InA==InB):
                        state.RZ=1
                    else:
                        state.RZ=0
                    state.MuxINC_select=state.RZ
                    break
                elif i==13:
                    if(InA!=InB):
                        state.RZ=1
                    else:
                        state.RZ=0
                    state.MuxINC_select=state.RZ
                    break
                elif i==14:
                    if(InA>=InB):
                        state.RZ=1
                    else:
                        state.RZ=0
                    state.MuxINC_select=state.RZ
                    break
                else:
                    break


    def IAG(self,state):
        if(state.MuxPC_select==0):
            self.PC_next = state.RA
        
        else:
            if(state.MuxINC_select==0):
                self.PC_next += 4
            else:
                self.PC_next += state.Imm

