import os.path
from os import path

class Input:
    def __init__(self, transaction_ID, arr_index, sign):
        self.transaction_ID = transaction_ID
        self.arr_index = arr_index
        self.sign = sign
        self.len_sign = None

    def show(self):
        print("\tTransacction ID: ", self.transaction_ID)
        print("\tIndex: ", self.arr_index)
        print("\tLength of the signature: ", self.len_sign)
        print("\tSignature: ", self.sign)

    def generateByte(self):
        byte_trans_id = bytes.fromhex(self.transaction_ID)
        byte_arr_index = self.arr_index.to_bytes(4, 'big')
        byte_sign = bytes.fromhex(self.sign)
        byte_len_sign = self.len_sign.to_bytes(4,'big')
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
        elif(not (all(i in valid_char for i in self.sign) or len(self.sign)%2==0)):
            print("\nSignature is not valid.\n")
            return False
        self.arr_index = int(self.arr_index)
        self.len_sign = len(self.sign)//2
        return True

class Output:
    def __init__(self, coin, path_to_pub):
        self.coin = coin
        self.path_to_pub = path_to_pub
        self.pub_key = None
        self.key_len = None

    def show(self):
        print("\tNo of coins: ", self.coin)
        print("\tLength of public key: ", self.key_len)
        print("\tPublic Key:\n", self.pub_key)

    def generateByte(self):
        byte_coin = self.coin.to_bytes(8, 'big')
        byte_pub_key = self.pub_key.encode()
        byte_key_len = self.key_len.to_bytes(4, 'big')
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
        self.key_len = len(self.pub_key)
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

def transactionFromByteArray(trans_byte):
    pass
