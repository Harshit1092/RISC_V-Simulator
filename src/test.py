from state import State
def execute():
    if State.stall:
        return
    InA=State.RA
    if State.MuxB_select:
        InB=State.Imm
    InB=State.RB

    for i in range(15):
        if(State.ALU_OP[i]==1):
            if i==0:
                State.RZ=InA+InB
                break
            elif i==1:
                State.RZ=InA-InB
                break
            elif i==2:
                if(InB!=0):
                    State.RZ=InA/InB
                break
            elif i==3:
                State.RZ=InA*InB
                break
            elif i==4:
                if(InB!=0):
                    State.RZ=InA-InB
                break
            elif i==5:
                State.RZ=InA^InB
                break
            elif i==6:
                if (InB>=0):
                    State.RZ=InA<<InB
                break
            elif i==7:
                #please write sra code here.
                break
            elif i==8:
                if (InB>=0):
                    State.RZ=InA>>InB
                break
            elif i==9:
                State.RZ=InA|InB
                break
            elif i==10:
                State.RZ=InA&InB
                break
            elif i==11:
                if(InA<InB):
                    State.RZ=1
                else:
                    State.RZ=0
                State.MuxINC_select=State.RZ
                break
            elif i==12:
                if(InA==InB):
                    State.RZ=1
                else:
                    State.RZ=0
                State.MuxINC_select=State.RZ
                break
            elif i==13:
                if(InA!=InB):
                    State.RZ=1
                else:
                    State.RZ=0
                State.MuxINC_select=State.RZ
                break
            elif i==14:
                if(InA>=InB):
                    State.RZ=1
                else:
                    State.RZ=0
                State.MuxINC_select=State.RZ
                break
            else:
                break
