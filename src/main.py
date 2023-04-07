from processor import processor
from state import State
import time

pc_tmp = []

if __name__ == '__main__':
    
    file1=open("demofile.mc", "r")
    pipelining_knob=bool(input())  #knob1
    forwarding_knob=bool(input())   #knob2
    print_registers_each_cycle=bool(input())    #knob3
    print_pipeline_registers=bool(input())   #knob4
    print_specific_pipeline_registers =bool(input())  #knob5

    processor = processor(file1)

    # Signals
    PC = 0
    clock_cycles = 0
    prog_end = False

    if not pipelining_knob:

        curr_instruction=State(PC)
        processor.fetch(curr_instruction)
        clock_cycles +=1
        if print_registers_each_cycle:
            print("CLOCK CYCLE:", clock_cycles)
            print("Register Data:-")
            for i in range(32):
                print("R" + str(i) + ":", processor.R[i], end=" ")
                print("\n")
            pc_tmp.append([-1, -1, -1, -1, instruction.PC])

        processor.decode(curr_instruction)
        clock_cycles +=1
        if print_registers_each_cycle:
            print("CLOCK CYCLE:", clock_cycles)
            print("Register Data:-")
            for i in range(32):
                print("R" + str(i) + ":", processor.R[i], end=" ")
                print("\n")
            pc_tmp.append([-1, -1, -1, -1, instruction.PC])
        

    file1.close()