import hashlib
import header
import sys

no_of_inp = int(input("\nENTER NO OF INPUTS: "))
input_arr = []
for i in range(no_of_inp):
    print(i+1,".")
    transaction_ID = input("Enter transaction ID(sha256): ")
    arr_index = input("Enter index of output: ")
    sign = input("Enter valid signature(hex): ")
    new_obj = header.Input(transaction_ID, arr_index, sign)
    if(not new_obj.isValid()):
        sys.exit()
    input_arr.append(new_obj)

no_of_out = int(input("\nENTER NO OF OUTPUTS: "))
output_arr = []
for i in range(no_of_out):
    print(i+1,".")
    coin = input("Enter no of coins: ")
    path_to_pub = input("Enter path to public key: ")
    new_obj = header.Output(coin, path_to_pub=path_to_pub)
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
    print("Created file: ", file_hash)
except:
    print("\nSome error occured while making transaction.")
