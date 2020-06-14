class Input:
    def __init__(self, transaction_ID, arr_index, sign, len_sign=None):
        self.transaction_ID = transaction_ID
        self.arr_index = int(arr_index)
        self.sign = sign
        if len_sign == None:
            self.len_sign = len(self.sign)//2
        else:
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

    def generateSignContent(self, out_hash):
        return bytes.fromhex(self.transaction_ID)+self.arr_index.to_bytes(4, 'big')+out_hash
    
    def as_json(self):
        json_data = {}
        json_data["transactionID"] = self.transaction_ID
        json_data["index"] = self.arr_index
        json_data["signature"] = self.sign
        return json_data
