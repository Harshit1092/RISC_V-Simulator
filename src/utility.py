# Utility Functions
def ImmediateSign(imm, num):
    if imm & (1 << (num - 1)) == 0:
        return imm
    neg = (1 << num) - 1
    imm = imm ^ neg
    imm += 1
    imm *= -1
    return imm

def nhex(num):
	if num < 0:
		num += 2**32
	return hex(num)

def nint(s, base, bits=32):
	num = int(s, base)
	if num >= 2**(bits-1):
		num -= 2**bits
	return num

def sign_extend(data):
	if data[2] == '8' or data[2] == '9' or data[2] == 'a' or data[2] == 'b' or data[2] == 'c' or data[2] == 'd' or data[2] == 'e' or data[2] == 'f':
		data = data[:2] + (10 - len(data)) * 'f' + data[2:]
	else:
		data = data[:2] + (10 - len(data)) * '0' + data[2:]
	return data



