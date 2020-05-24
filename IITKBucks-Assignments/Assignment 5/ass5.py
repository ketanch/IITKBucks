import block
import time

index = int(input("Enter index of block: "))
parent_hash = input("Enter parent hash: ")
target = input("Enter target: ")
body_file = input("Input block body file: ")
data = open(body_file,'rb').read()
body = block.BlockBodyMake(inps = [],body = data)

header = block.BlockHeaderMake(index, parent_hash, body.getBodyHash(), target)
print("Finding Nonce and Timestamp: ")
t1 = time.perf_counter()
[nonce, timestamp, final_hash] = header.findNonceAndTimestamp()
t2 = time.perf_counter()
print("Hash: %s\nNonce: %d\nTimestamp: %f\nTime: %dmin %dsec"%(final_hash, nonce,timestamp,int((t2-t1)/60),int((t2-t1))%60))
