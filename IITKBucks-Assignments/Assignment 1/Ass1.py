import hashlib
import sys
def compare(inp, tar):
	for i in range(0, 63):
		a=int(inp[i:i+2],16)
		b=int(tar[i:i+2],16)
		if a>b:
			return False
		elif a<b:
			return True
		else:
			pass
		i+=2
	return False
if(len(sys.argv)!=2):
	print("USAGE : python <string>")
	sys.exit()
inp = sys.argv[1]
i=0
target = "0000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF"
while 1:
	var = inp+str(i)
	i += 1
	sha256hash = hashlib.sha256(var.encode()).hexdigest()
	print("TRIED : ",var)
	if compare(sha256hash, target):
		print("RESULT FOUND : ",var)
		break
