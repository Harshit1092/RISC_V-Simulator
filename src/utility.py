# Utility Functions
def ImmediateSign(imm, num):
    if imm & (1 << (num - 1)) == 0:
        return
    neg = (1 << num) - 1
    imm = imm ^ neg
    imm += 1
    imm *= -1
    return imm

