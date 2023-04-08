class HDU:
    #If forwarding is not enabled
    def dataHazardStalling(self, pipeline_instructions):
        countHazards = 0
        isDataHazard = False
        print(f"pipeline0 : {pipeline_instructions[0].IR}")
        print(f"pipeline1 : {pipeline_instructions[1].IR}")
        print(f"pipeline2 : {pipeline_instructions[2].IR}")
        print(f"pipeline3 : {pipeline_instructions[3].IR}")
        print(f"pipeline4 : {pipeline_instructions[4].IR}")
        decode_state = pipeline_instructions[-2]
        instruction = bin(int(decode_state.IR[2:],16))[2:]
        instruction = (32-len(instruction)) * '0' + instruction
        print(f"inst : {instruction}")
        decode_opcode = int(instruction[25:32],2)
        if(decode_opcode in [19, 103, 3]):
            decode_state.RS1 = int(instruction[12:17],2)
            decode_state.RS2 = -1
        else:
            decode_state.RS1 = int(instruction[12:17],2)
            decode_state.RS2 = int(instruction[7:12],2)
            
        states = pipeline_instructions[:-1]
        to_from = {'to': -1, 'from': -1}
        
        # Extracting all states
        execute_state = states[-2]
        decode_state = states[-1]
        memory_state = states[-3]
        
        print(f"execute RD : {execute_state.RD}")
        print(f"decode RS1 : {decode_state.RS1}")
        print(f"decode RS2 : {decode_state.RS2}")
        print(f"Memory RD : {memory_state.RD}")
        # print(f"Memory : {memory_state.IR}")
        # print(f"RS2 : {decode_state.RS2}")
        # Checking dependency between execute state and decode state
        if execute_state.RD != -1 and execute_state.RD != 0 and not execute_state.stall and not decode_state.stall:
            if execute_state.RD == decode_state.RS1 or execute_state.RD == decode_state.RS2:
                isDataHazard = True
                countHazards = countHazards + 1
                to_from = {'to': 3, 'from': 2}
        
        #checking dependency between memory state and decode state
        if memory_state.RD != -1 and memory_state.RD != 0 and not memory_state.stall and not decode_state.stall:
            if memory_state.RD == decode_state.RS1 or memory_state.RD == decode_state.RS2:
                isDataHazard = True
                countHazards = countHazards + 1
                to_from = {'to': 3, 'from': 1}
                print("HELLO")
        # print(f"to_from : {to_from}")
        return [isDataHazard, countHazards, to_from]
    
    #If forwarding is enabled
    def dataHazardForwarding(self,pipeline_instructions):
        decode_state = pipeline_instructions[-2]
        execute_state = pipeline_instructions[-3]
        memory_state = pipeline_instructions[-4]
        writeback_state = pipeline_instructions[-5]
        
        instruction = bin(int(decode_state.IR[2:],16))[2:]
        instruction = (32-len(instruction)) * '0' + instruction
        decode_opcode = int(instruction[25:32],2)
        
        if(decode_opcode in [19, 103, 3]):
            decode_state.RS1 = instruction[12:17]
            decode_state.RS2 = -1
        else:
            decode_state.RS1 = instruction[12:17]
            decode_state.RS2 = instruction[7:12]
         
        #Initializing variables   
        countHazards = 0
        isStall = False
        stallPos = 2
        to_from = {'to': -1, 'from': -1}
        to_for = [""]*5
        
        
        #Extracting opcodes
        instruction = bin(int(execute_state.IR[2:], 16))[2:]
        instruction = (32 - len(instruction)) * '0' + instruction
        execute_opcode = int(instruction[25:32], 2)

        instruction = bin(int(memory_state.IR[2:], 16))[2:]
        instruction = (32 - len(instruction)) * '0' + instruction
        memory_opcode = int(instruction[25:32], 2)

        instruction = bin(int(writeback_state.IR[2:], 16))[2:]
        instruction = (32 - len(instruction)) * '0' + instruction
        writeback_opcode = int(instruction[25:32], 2)
        
        # M -> M forwarding
        if writeback_opcode == 3 and memory_opcode == 35 and not writeback_state.stall and not memory_state.stall:
            if writeback_state.RD != -1 and writeback_state.RD != 0 and writeback_state.RD == memory_state.RS2:
                memory_state.RY = writeback_state.RY
                countHazards = countHazards + 1
                to_from = {'to': -1, 'from': -1}
                to_for[1] = "forwarded from mem"
                
        # M -> E forwarding
        if writeback_state.RD != -1 and writeback_state.RD != 0 and not writeback_state.stall:
            if writeback_state.RD == execute_state.RS1 and not execute_state.stall:
                execute_state.RA = writeback_state.RY
                countHazards = countHazards + 1
                to_from = {'to': -1, 'from': -1}
                to_for[2] = "forwarded from mem"
        
            if writeback_state.RD == execute_state.RS2 and not execute_state.stall:
                if execute_opcode != 35:
                    execute_state.RB = writeback_state.RY
                else:
                    execute_state.RY = writeback_state.RY
                
                countHazards = countHazards + 1
                to_from = {'to': -1, 'from': -1}
                to_for[2] = "forwarded from mem"
                
        # E -> E forwarding
        if memory_state.RD != -1 and memory_state.RD != 0 and not memory_state.stall:
            if memory_opcode == 3:
                if execute_opcode == 35:
                    if execute_state.RS1 == memory_state.RD and not execute_state.stall:
                        countHazards = countHazards + 1
                        isStall = True
                        stallPos = 0
                        to_from = {'to':2, 'from': 1}
                else:
                    if (execute_state.RS1 == memory_state.RD or execute_state.RS2 == memory_state.RD) and not execute_state.stall:
                        countHazards = countHazards + 1
                        isStall = True
                        stallPos = 0
                        to_from = {'to':2, 'from': 1}
                    
            else:
                if execute_state.RS1 == memory_state.RD and not execute_state.stall:
                    execute_state.RA = memory_state.RY
                    countHazards += 1
                    to_from = {'to': -1, 'from': -1}
                    to_for[2] = "forwarded from execute"

                if execute_state.RS2 == memory_state.RD and not execute_state.stall:
                    if execute_opcode != 35: # store
                        execute_state.RB = memory_state.RY
                    else:
                        execute_state.RY = memory_state.RY
                    countHazards += 1
                    to_from = {'to': -1, 'from': -1}
                    to_for[2] = "forwarded from execute"
        
        if (decode_opcode == 99 or decode_opcode == 103) and not decode_state.stall: # SB and jalr
            # M -> D forwarding
            if writeback_state.RD != -1 and writeback_state.RD != 0 and not writeback_state.stall:
                if writeback_state.RD == decode_state.RS1:
                    decode_state.RA = writeback_state.RY
                    decode_state.decode_forwarding_op1 = True
                    countHazards += 1
                    to_from = {'to': -1, 'from': -1}
                    to_for[3] = "forwarded from mem"

                if writeback_state.RD == decode_state.RS2:
                    decode_state.RB = writeback_state.RY
                    decode_state.decode_forwarding_op2 = True
                    countHazards += 1
                    to_from = {'to': -1, 'from': -1}
                    to_for[3] = "forwarded from mem"

            # E -> D fowarding
            if memory_state.RD != -1 and memory_state.RD != 0 and not memory_state.stall:
                if memory_opcode == 3 and (memory_state.RD == decode_state.RS1 or memory_state.RD == decode_state.RS2): # load
                    countHazards += 1
                    isStall = True
                    if stallPos > 1:
                        stallPos = 1
                        to_from = {'to': 3, 'from': 1}

                else:
                    if memory_state.RD == decode_state.RS1:
                        decode_state.RA = memory_state.RY
                        decode_state.decode_forwarding_op1 = True
                        countHazards += 1
                        to_from = {'to': -1, 'from': -1}
                        to_for[3] = "forwarded from execute"

                    if memory_state.RD == decode_state.RS2:
                        decode_state.RB = memory_state.RY
                        decode_state.decode_forwarding_op2 = True
                        countHazards += 1
                        to_from = {'to': -1, 'from': -1}
                        to_for[3] = "forwarded from execute"

            # If control instruction depends on the previous instruction
            if execute_state.RD != -1 and execute_state.RD != 0 and (execute_state.RD == decode_state.RS1 or execute_state.RD == decode_state.RS2) and not execute_state.stall:
                countHazards += 1
                isStall = True
                if stallPos > 1:
                    stallPos = 1
                    to_from = {'to': 3, 'from': 2}

        to_from['from'] = to_for
        new_states = [writeback_state, memory_state, execute_state, decode_state, pipeline_instructions[-1]]
        return [countHazards, isStall, stallPos, new_states, to_from]
