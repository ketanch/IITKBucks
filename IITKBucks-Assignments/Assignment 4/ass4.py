import header
import hashlib

file_path = input("Enter file path: ")
file_data = open(file_path,'rb').read()
file_hash = hashlib.sha256(file_data).hexdigest()
print("Transaction ID: ", file_hash)
[inp_arr, out_arr] = header.transactionFromByteArray(file_data)
print("\nNumber of inputs: ",len(inp_arr))
a=1
for i in inp_arr:
    print("  Input %d:"%a)
    i.show()
    a+=1
    print("\n")
a=1
print("\nNumber of outputs: ",len(out_arr))
for i in out_arr:
    print("  Output %d"%a)
    i.show()
    a+=1
    print("\n")