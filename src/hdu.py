class HDU:
    #If forwarding is not enabled
    def dataHazardStalling(self, pipeline_instructions):
        countHazards = 0
        isDataHazard = False
        
        decode_state = pipeline_instructions[-2]
        instruction = bin(int(decode_state.IR[2:],16))[2:]
        instruction = (32-len(instruction)) * '0' + instruction
        
        decode_opcode = int(instruction[25:32],2)
        if(decode_opcode in [19, 103, 3]):
            decode_state.RS1 = instruction[12:17]
            decode_state.RS2 = -1
        else:
            decode_state.RS1 = instruction[12:17]
            decode_state.RS2 = instruction[7:12]
            
        states = pipeline_instructions[:-1]
        to_from = {'to': -1, 'from': -1}
        
        # Extracting all states
        execute_state = states[-2]
        decode_state = states[1]
        memory_state = states[-3]
        
        # Checking dependency between execute state and decode state
        if execute_state.RD != -1 and execute_state.RD != 0 and not execute_state.stall and not decode_state.stall:
            if execute_state.RD == decode_state.RS1 or execute_state.RD == decode_state.RS2:
                isDataHazard = True
                countHazards = countHazards + 1
                to_from = {'to': 3, 'from': 2}
        
        #checking dependency between memory state and decode state
        if memory_state.RD != -1 and memory_state.RS1 != 0 and not memory_state.stall and not decode_state.stall:
            if memory_state.RD == decode_state.RS1 or memory_state.RD == decode_state.RS2:
                isDataHazard = True
                countHazards = countHazards + 1
                to_from = {'to': 3, 'from': 1}
        
        return [isDataHazard, countHazards, to_from]