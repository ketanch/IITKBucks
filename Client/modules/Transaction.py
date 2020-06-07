from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_PSS
import hashlib

class Transaction:
    def __init__(self, inp_arr, out_arr):
        self.inp_arr = inp_arr
        self.out_arr = out_arr
    
    def isValid(self, unused_trans):
        data_out += len(self.out_arr).to_bytes(4,'big')
        for i in trans.out_arr:
            data_out += i.generateByte()
        out_hash = hashlib.sha256(data_out)
        if not all((i.transaction_ID, i.arr_index) in unused_trans.keys() for i in self.inp_arr):
            return False
        if not all(verify(unused_trans[(i.transaction_ID, i.arr_index)].pub_key, i.generateSign(out_hash), i.sign) for i in self.inp_arr):
            return False
        inp_coins = 0
        out_coins = 0
        for i in self.inp_arr:
            inp_coins += unused_trans[(i.transaction_ID, i.arr_index)].coin
        for i in self.out_arr:
            out_coins += i.coin
        if out_coins > inp_coins:
            return False
        return True

    def getTransID(self):
        return hashlib.sha256(transactionToByteArray(self)).hexdigest()

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
        inp_obj = Input(trans_ID, index, sign)
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

def verify(pub_key, text, sign):
    return PKCS1_PSS.new(pub_key).verify(text, sign)
