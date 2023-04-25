from processor import *
from state import *
from btb import *
from hdu import *
from cache import *

pc_tmp = []
dataHazardPairs = []
controlHazardSignals = []

memoryTable = []

def evaluate(processor, pipelineInstructions):
    processor.writeBack(pipelineInstructions[0])
    guiMemory = processor.memoryAccess(pipelineInstructions[1])
    processor.execute(pipelineInstructions[2])
    controlHazard, controlPC, enter, color = processor.decode(pipelineInstructions[3], btb)

    if enter:
        controlHazardSignals.append(2)
    elif pipelineInstructions[2].stall and color !=0 and len(controlHazardSignals) > 0 and controlHazardSignals[-1] == 2:
        controlHazardSignals.append(controlHazardSignals[-1])
    else:
        controlHazardSignals.append(color)
    guiFetch = processor.fetch(pipelineInstructions[4],btb)
    memoryTable.append([guiFetch, guiMemory])
    return [pipelineInstructions[1],pipelineInstructions[2],pipelineInstructions[3],pipelineInstructions[4]], controlHazard, controlPC
        
def takeInput():
    knob_input=open("knobsInput.txt", "r")
    knobs=[]
    for line in knob_input:
        x=line.split()
        if x[0]=='True':
            if len(x)==1:
                knobs.append(True)
            else:
                knobs.append([True,x[1]])
        
        else:
            if len(x)==1:
                knobs.append(False)
            else:
                knobs.append([False,x[1]])
    knob_input.close()

    cache_input = open("cacheInput.txt", "r")
    cache = []
    for line in cache_input:
        x = line.split()
        for i in range(len(x)):
            cache.append(int(x[i]))
    cache_input.close()
    
    return knobs, cache

if __name__ == '__main__':
    
    file1="demofile.txt"
    knobs, cache = takeInput()

    # Knobs
    pipelining_knob=knobs[0]  # knob1
    forwarding_knob=knobs[1]   # knob2
    print_registers_each_cycle=knobs[2]    # knob3
    print_pipeline_registers=knobs[3]   # knob4
    print_specific_pipeline_registers =knobs[4]  # knob5

    # Data cache inputs
    dataCacheSize = int(cache[0])
    dataCacheBlockSize = int(cache[1]) # Word is 4B
    dataCacheAssociativity = int(cache[2]) # 0/1/2[FA/DM/SA]
    dataCacheWays = int(cache[3])

	# Instruction cache inputs
    instructionCacheSize = int(cache[4])
    instructionCacheBlock_size = int(cache[5]) # Word is 4B
    instructionCacheAssociativity = int(cache[6]) # 0/1/2[FA/DM/SA]
    instructionCacheWays = int(cache[7])

    # Various Counts
    stalls_due_to_data_hazard = 0
    number_of_data_hazards = 0
    stalls_due_to_control_hazard = 0
    totalStalls = 0

    # Initial calling of classes
    dataCache = Cache(dataCacheSize, dataCacheBlockSize, dataCacheAssociativity, dataCacheWays)
    instructionCache = Cache(instructionCacheSize, instructionCacheBlock_size, instructionCacheAssociativity, instructionCacheWays)
    processor = Processor(file1, dataCache, instructionCache)
    hdu=HDU()
    btb=BTB()

    # Signals
    PC = 0
    clock_cycles = 0
    prog_end = False

    if not pipelining_knob:

        processor.pipeliningEnabled=False
        while True:

            curr_instruction=State(PC)
            guiRead = processor.fetch(curr_instruction)
            clock_cycles +=1
            if print_registers_each_cycle:
                print("CLOCK CYCLE:", clock_cycles)
                print("Register Data:-")
                for i in range(32):
                    print("R" + str(i) + ":", processor.registers[i], end=" ")
                    print("\n")
            pc_tmp.append([-1, -1, -1, -1, curr_instruction.PC])
            memoryTable.append([guiRead, False])

            processor.decode(curr_instruction)
            clock_cycles +=1
            if print_registers_each_cycle:
                print("CLOCK CYCLE:", clock_cycles)
                print("Register Data:-")
                for i in range(32):
                    print("R" + str(i) + ":", processor.registers[i], end=" ")
                    print("\n")
            pc_tmp.append([-1, -1, -1, curr_instruction.PC,-1])
            memoryTable.append([False, False])

            if processor.terminate:
                prog_end = True
                break
            
            processor.execute(curr_instruction)
            clock_cycles +=1
            if print_registers_each_cycle:
                print("CLOCK CYCLE:", clock_cycles)
                print("Register Data:-")
                for i in range(32):
                    print("R" + str(i) + ":", processor.registers[i], end=" ")
                    print("\n")
            pc_tmp.append([-1, -1,curr_instruction.PC,-1,-1])
            memoryTable.append([False, False])

            guiData = processor.memoryAccess(curr_instruction)
            clock_cycles +=1
            if print_registers_each_cycle:
                print("CLOCK CYCLE:", clock_cycles)
                print("Register Data:-")
                for i in range(32):
                    print("R" + str(i) + ":", processor.registers[i], end=" ")
                    print("\n")
            pc_tmp.append([-1,curr_instruction.PC,-1,-1,-1])
            memoryTable.append([False, guiData])

            processor.writeBack(curr_instruction)
            clock_cycles +=1
            if print_registers_each_cycle:
                print("CLOCK CYCLE:", clock_cycles)
                print("Register Data:-")
                for i in range(32):
                    print("R" + str(i) + ":", processor.registers[i], end=" ")
                    print("\n")
            pc_tmp.append([curr_instruction.PC,-1,-1,-1,-1])
            memoryTable.append([False, False])
            PC=processor.PC_next

    else:
        processor.pipeliningEnabled = True
        pipelineInstructions = [State(0) for x in range(5)]
        for i in range(4):
            pipelineInstructions[i].stall = True
        
        while not prog_end:
            if not forwarding_knob:
                
                dataHazard = hdu.dataHazardStalling(pipelineInstructions)
                oldStates = pipelineInstructions
                pipelineInstructions, controlHazard, controlPC = evaluate(processor, pipelineInstructions)
                
                tmp = []
                for i in range(5):
                    if oldStates[i].stall:
                        tmp.append(-1)
                    else:
                        tmp.append(oldStates[i].PC)
                pc_tmp.append(tmp)

                dataHazardPairs.append(dataHazard[3])
                branch_taken = pipelineInstructions[3].branch_taken
                branch_pc = pipelineInstructions[3].PC_next

                PC += 4

                if branch_taken and not dataHazard[0]:
                    PC = branch_pc
                
                if controlHazard and not dataHazard[0]:
                    stalls_due_to_control_hazard += 1
                    PC = controlPC
                    pipelineInstructions.append(State(PC))
                    pipelineInstructions[-2].stall = True

                if dataHazard[0]:
                    number_of_data_hazards += dataHazard[1]
                    stalls_due_to_data_hazard += dataHazard[2]
                    pipelineInstructions = pipelineInstructions[:2] + [State(0)] + oldStates[3:]
                    pipelineInstructions[2].stall = True
                    PC -= 4
                
                if not controlHazard and not dataHazard[0]:
                    pipelineInstructions.append(State(PC))
                
                pipelineInstructions[-2].PC_next = PC

                prog_end = True
                for i in range(4):
                    x = pipelineInstructions[i]
                    if not x.stall:
                        prog_end = False
                        break
                clock_cycles+=1
            else:
                dataHazard, ifStall, stallPos, pipelineInstructions, toFrom = hdu.dataHazardForwarding(pipelineInstructions)

                oldStates = pipelineInstructions
                pipelineInstructions, controlHazard, controlPC = evaluate(processor, pipelineInstructions)

                tmp = []
                for i in range(5):
                    if oldStates[i].stall:
                        tmp.append(-1)
                    else:
                        tmp.append(oldStates[i].PC)
                pc_tmp.append(tmp)

                dataHazardPairs.append(toFrom)

                branch_taken = pipelineInstructions[3].branch_taken
                branch_pc = pipelineInstructions[3].PC_next

                PC += 4

                if branch_taken and not ifStall:
                    PC = branch_pc
                
                if controlHazard and not ifStall:
                    stalls_due_to_control_hazard += 1
                    PC = controlPC
                    pipelineInstructions.append(State(PC))
                    pipelineInstructions[-2].stall = True

                if ifStall:
                    stalls_due_to_data_hazard += 1

                    if stallPos == 0:
                        pipelineInstructions = pipelineInstructions[:1] + [State(0)] + oldStates[2:]
                        pipelineInstructions[1].stall = True
                        PC -= 4

                    elif stallPos == 1:
                        pipelineInstructions = pipelineInstructions[:2] + [State(0)] + oldStates[3:]
                        pipelineInstructions[2].stall = True
                        PC -= 4
                if(ifStall):
                    number_of_data_hazards += dataHazard

                if not controlHazard and not ifStall:
                    pipelineInstructions.append(State(PC))
                
                pipelineInstructions[-2].PC_next = PC

                for inst in pipelineInstructions:
                    inst.decode_forwarding_op1 = False
                    inst.decode_forwarding_op2 = False
                
                prog_end = True
                for i in range(4):
                    x = pipelineInstructions[i] 
                    if not x.stall:
                        prog_end = False
                        break
                
                clock_cycles += 1

            # Print the register values after each clock cycle
            if print_registers_each_cycle:
                print("CLOCK CYCLE:", clock_cycles)
                print("Register Data:-")
                for i in range(32):
                    print("R" + str(i) + ":", processor.registers[i], end=" ")
                print("\n")

            # Print specific pipeline registers
            if print_specific_pipeline_registers[0]:
                for inst in pipelineInstructions:
                    if inst.PC/4 == int(print_specific_pipeline_registers[1], 10):
                        if not print_registers_each_cycle:
                            print("CLOCK CYCLE:", clock_cycles)
                            print("Pipeline Registers:-")
                            print("Fetch # Decode =>", "Instruction:", pipelineInstructions[3].IR)
                            print("Decode # Execute => ", "Operand1: ", pipelineInstructions[2].RA, ", Operand2: ", pipelineInstructions[2].RB)
                            print("Execute # Memory => ", "Data: ", pipelineInstructions[1].RY)
                            print("Memory # WriteBack => ", "Data: ", pipelineInstructions[0].RY)
                            print("\n")

            # Print pipeline registers
            elif print_pipeline_registers:
                if not print_registers_each_cycle:
                    print("CLOCK CYCLE:", clock_cycles)
                    print("Pipeline Registers:-")
                    print("Fetch # Decode =>", "Instruction:", pipelineInstructions[3].IR)
                    print("Decode # Execute => ", "Operand1: ", pipelineInstructions[2].RA, ", Operand2: ", pipelineInstructions[2].RB)
                    print("Execute # Memory => ", "Data: ", pipelineInstructions[1].RY)
                    print("Memory # WriteBack => ", "Data: ", pipelineInstructions[0].RY)
                    print("\n")
     
    pc_tmp.pop(-1)

    cycleFile = open("cycle.txt", "w")
    for i in range(len(pc_tmp)):
        cycleFile.write(str(i + 1) + "  ")
        for j in range(len(pc_tmp[i])):
            code = str(processor.riscvCode[pc_tmp[i][j]])
            cycleFile.write(code + "  ")
        if pipelining_knob:
            cycleFile.write(str(dataHazardPairs[i]))
        cycleFile.write("\n")
    cycleFile.close()

    totalStalls = stalls_due_to_control_hazard + stalls_due_to_data_hazard
    processor.writeDataMemory()
    # Printing the stats at the end of the simulation
    statsFile = open("stats.txt", "w")

    statsFile.write("Pipeline Stats\n")
    # Pipeline Stats
    stats = [''] * 12
    stats[0] = "Number of clock cycles: " + str(clock_cycles) + "\n"
    stats[1] = "Number of instructions executed: " + str(processor.Total_instructions) + "\n"
    stats[2] = "CPI: " + str(clock_cycles / processor.Total_instructions) + "\n"
    stats[3] = "Number of data transfer (load & store) instructions executed: " + str(processor.memory_instructions) + "\n"
    stats[4] = "Number of ALU instructions executed: " + str(processor.ALU_instructions) + "\n"
    stats[5] = "Number of control instructions executed: " + str(processor.control_instructions) + "\n"
    stats[6] = "Number of stalls: " + str(totalStalls) + "\n"
    stats[7] = "Number of data hazards: " + str(number_of_data_hazards) + "\n"
    stats[8] = "Number of control hazards: "
    if processor.pipeliningEnabled:
        stats[8] += str(processor.control_instructions) + "\n"
    else:
        stats[8] += "0\n"
    stats[9] = "Number of branch mispredictions: " + str(processor.branch_misprediction) + "\n"
    stats[10] = "Number of stalls due to data hazards: " + str(stalls_due_to_data_hazard) + "\n"
    stats[11] = "Number of stalls due to control hazards: " + str(stalls_due_to_control_hazard) + "\n"

    statsFile.writelines(stats)

    statsFile.write("Cache Stats\n")
    # Cache Stats
    ic = [''] * 3
    dc = [''] * 4

    statsFile.write("Instruction Cache :-\n")
    ic[0] = "Number of accesses: Read -> " + str(processor.instCache.readCount) + ", Write -> " + str(processor.instCache.writeCount) + "\n"
    ic[1] = "Number of hits: " + str(processor.instCache.hitCount) + "\n"
    ic[2] = "Number of misses: " + str(processor.instCache.missCount) + "\n"
    
    statsFile.writelines(ic)

    statsFile.write("Data Cache :-\n")
    dc[0] = "Number of accesses: Read -> " + str(processor.dataCache.readCount) + ", Write -> " + str(processor.dataCache.writeCount) + "\n"
    dc[1] = "Number of hits: " + str(processor.dataCache.hitCount) + "\n"
    dc[2] = "Number of misses: " + str(processor.dataCache.missCount) + "\n"
    
    statsFile.writelines(dc)
    statsFile.close()

    hitMissFile = open("hit_miss.txt", "w")
    for i in range(memoryTable):
        if memoryTable[i][0]:
            d = memoryTable[i][0]
            if d['action'] == 'read':
                hitMissFile.write("Reading from set: " + str(d['index']) + " Victim: " + str(d.get('victim', '-1')) + " ")
                if d['status'] == 'found':
                    hitMissFile.write("(Read Hit)")
                elif d['status'] == 'added':
                    hitMissFile.write("(Read Miss: Added from main memory)")
                else:
                    hitMissFile.write("(Read Miss: Replaced from main memory)")
            elif d['action'] == 'write':
                hitMissFile.write("Writing in set: " + str(d['index']) + " Victim: " + str(d.get('victim', '-1')) + " ")
                if d['status'] == 'found':
                    hitMissFile.write("(Write Hit)")
                else:
                    hitMissFile.write("(Write Miss: Writing through in main memory)")
        hitMissFile.write("  ")
        if memoryTable[i][1]:
            d = memoryTable[i][1]
            if d['action'] == 'read':
                hitMissFile.write("Reading from set: " + str(d['index']) + " Victim: " + str(d.get('victim', '-1')) + " ")
                if d['status'] == 'found':
                    hitMissFile.write("(Read Hit)")
                elif d['status'] == 'added':
                    hitMissFile.write("(Read Miss: Added from main memory)")
                else:
                    hitMissFile.write("(Read Miss: Replaced from main memory)")
            elif d['action'] == 'write':
                hitMissFile.write("Writing in set: " + str(d['index']) + " Victim: " + str(d.get('victim', '-1')) + " ")
                if d['status'] == 'found':
                    hitMissFile.write("(Write Hit)")
                else:
                    hitMissFile.write("(Write Miss: Writing through in main memory)")
        hitMissFile.write("\n")