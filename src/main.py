from processor import *
from state import *
from btb import *

pc_tmp = []

if __name__ == '__main__':
    
    file1="demofile.txt"
    knob_input=open("input.txt", "r")
    knobs=[]
    for line in knob_input:
        if(line[0]=="T"):
            knobs.append(True)
        else:
            knobs.append(False)

    knob_input.close()
    pipelining_knob=knobs[0]  #knob1
    forwarding_knob=knobs[1]   #knob2
    print_registers_each_cycle=knobs[2]    #knob3
    print_pipeline_registers=knobs[3]   #knob4
    print_specific_pipeline_registers =knobs[4]  #knob5

    #initial calling of classes.
    processor = processor(file1)
    btb=BTB()

    # Signals
    PC = 0
    clock_cycles = 0
    prog_end = False

    if not pipelining_knob:

        processor.pipelingEnabled=False
        while True:

            curr_instruction=State(PC)
            processor.fetch(curr_instruction)
            clock_cycles +=1
            if print_registers_each_cycle:
                print("CLOCK CYCLE:", clock_cycles)
                print("Register Data:-")
                for i in range(32):
                    print("R" + str(i) + ":", processor.registers[i], end=" ")
                    print("\n")
                pc_tmp.append([-1, -1, -1, -1, curr_instruction.PC])

            processor.decode(curr_instruction)
            clock_cycles +=1
            if print_registers_each_cycle:
                print("CLOCK CYCLE:", clock_cycles)
                print("Register Data:-")
                for i in range(32):
                    print("R" + str(i) + ":", processor.registers[i], end=" ")
                    print("\n")
            pc_tmp.append([-1, -1, -1, curr_instruction.PC,-1])

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

            processor.MemoryAccess(curr_instruction)
            clock_cycles +=1
            if print_registers_each_cycle:
                print("CLOCK CYCLE:", clock_cycles)
                print("Register Data:-")
                for i in range(32):
                    print("R" + str(i) + ":", processor.registers[i], end=" ")
                    print("\n")
            pc_tmp.append([-1,curr_instruction.PC,-1,-1,-1])

            processor.writeBack(curr_instruction)
            clock_cycles +=1
            if print_registers_each_cycle:
                print("CLOCK CYCLE:", clock_cycles)
                print("Register Data:-")
                for i in range(32):
                    print("R" + str(i) + ":", processor.registers[i], end=" ")
                    print("\n")
            pc_tmp.append([curr_instruction.PC,-1,-1,-1,-1])

            PC=processor.PC_next

    processor.writeDataMemory()