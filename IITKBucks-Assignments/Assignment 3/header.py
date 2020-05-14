import os.path
from os import path

class Input:
    def __init__(self, transaction_ID, arr_index, sign, len_sign=None):
        self.transaction_ID = transaction_ID
        self.arr_index = arr_index
        self.sign = sign
        self.len_sign = len_sign

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
        if self.len_sign == None:
            self.len_sign = len(self.sign)//2
        return True

class Output:
    def __init__(self, coin, pub_key=None, key_len=None, path_to_pub=None,):
        self.coin = coin
        self.path_to_pub = path_to_pub
        self.pub_key = pub_key
        self.key_len = key_len

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

def transactionFromByteArray(trans_data):
    offset = 0
    in_arr = []
    out_arr = []
    no_of_input = int.from_bytes(trans_data[:4], 'big')
    offset += 4
    for i in range(no_of_input):
        trans_ID = trans_data[offset:offset+32].hex()
        offset += 32
        index = int.from_bytes(trans_data[offset:offset+4], 'big')
        offset +=4
        sign_len = int.from_bytes(trans_data[offset:offset+4], 'big')
        offset +=4
        sign = trans_data[offset:offset+sign_len].hex()
        offset += sign_len
        inp_obj = Input(trans_ID, index, sign, sign_len)
        in_arr.append(inp_obj)

    no_of_output = int.from_bytes(trans_data[offset:offset+4], 'big')
    offset += 4
    for i in range(no_of_output):
        coins = int.from_bytes(trans_data[offset:offset+8], 'big')
        offset +=8
        key_len = int.from_bytes(trans_data[offset:offset+4], 'big')
        offset +=4
        key = trans_data[offset:offset+key_len].decode()
        offset += key_len
        out_obj = Output(coins, key, key_len)
        out_arr.append(out_obj)
    return [in_arr, out_arr]
