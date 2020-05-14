import hashlib
import header
import sys

no_of_inp = int(input("\nENTER NO OF INPUTS: "))
input_arr = []
for i in range(no_of_inp):
    print(i+1,".")
    new_obj = header.Input()
    if(not new_obj.isValid()):
        sys.exit()
    input_arr.append(new_obj)

no_of_out = int(input("\nENTER NO OF OUTPUTS: "))
output_arr = []
for i in range(no_of_out):
    print(i+1,".")
    new_obj = header.Output()
    if(not new_obj.isValid()):
        sys.exit()
    output_arr.append(new_obj)

try:
    new_transaction = header.Transaction(input_arr, output_arr)
    file_data = header.transactionToByteArray(new_transaction)
    file_hash = hashlib.sha256(file_data).hexdigest()+".dat"
    file_out = open(file_hash, 'wb')
    file_out.write(file_data)
    file_out.close()
    print("\nTransaction made successfully")
except:
    print("\nSome error occured while making transaction.")
