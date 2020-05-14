import os.path
from os import path

class Input:
    def __init__(self):
        self.transaction_ID = input("Enter transaction ID(sha256): ")
        self.arr_index = input("Enter index of output: ")
        self.sign = input("Enter valid signature(hex): ")

    def show(self):
        print("Transacction ID: ", self.transaction_ID)
        print("Output Index: ", self.arr_index)
        print("RSA Signature: ", self.sign)

    def generateByte(self):
        byte_trans_id = bytes.fromhex(self.transaction_ID)
        byte_arr_index = self.arr_index.to_bytes(4, 'big')
        byte_sign = bytes.fromhex(self.sign)
        len_sign = len(byte_sign)
        byte_len_sign = len_sign.to_bytes(4,'big')
        byte_final = byte_trans_id+byte_arr_index+byte_len_sign+byte_sign
        return byte_final

    def isValid(self):
        valid_char = '0123456789abcdefABCDEF'
        if(not all(i in valid_char for i in self.transaction_ID) or len(self.transaction_ID)!=64):
            print("\nTransaction Id not valid.\n")
            return False
        elif(not self.arr_index.isdigit()):
            print("\nOutput index not valid.\n")
            return False
        elif(not all(i in valid_char for i in self.sign)):
            print("\nSignature is not valid.\n")
            return False
        self.arr_index = int(self.arr_index)
        return True

class Output:
    def __init__(self):
        self.coin = input("Enter no of coins: ")
        self.path_to_pub = input("Enter path to public key: ")
        self.pub_key = ''

    def show(self):
        print("No of coins: ", self.coin)
        print("Public Key: ", self.pub_key)

    def generateByte(self):
        byte_coin = self.coin.to_bytes(8, 'big')
        byte_pub_key = self.pub_key.encode()
        key_len = len(byte_pub_key)
        byte_key_len = key_len.to_bytes(4, 'big')
        byte_final = byte_coin+byte_key_len+byte_pub_key
        return byte_final
        
    def isValid(self):
        if(not path.isfile(self.path_to_pub)):
            print("\nEnter a valid file path.\n")
            return False
        elif(not self.coin.isdigit()):
            print("\nNo of coins should be an integer.\n")
            return False
        self.coin = int(self.coin)
        self.pub_key = open(self.path_to_pub,'r').read()
        return True

class Transaction:
    def __init__(self, inp_arr, out_arr):
        self.inp_arr = inp_arr
        self.out_arr = out_arr

def transactionToByteArray(trans):
    data = len(trans.inp_arr).to_bytes(4,'big')
    for i in trans.inp_arr:
        data += i.generateByte()
    data += len(trans.out_arr).to_bytes(4,'big')
    for i in trans.out_arr:
        data += i.generateByte()
    return data

def transactionFromByteArray():
    pass
