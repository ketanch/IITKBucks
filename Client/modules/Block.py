from Transaction import *
import struct

class Block:

    def __init__(self, index=None, parent_hash=None, body_hash=None, target=None, timestamp=None, nonce=None, body=None, transactions=[]):
        self.index = index
        self.parent_hash = parent_hash
        self.body_hash = body_hash
        self.target = target
        self.timestamp = timestamp
        self.nonce = nonce
        self.body = body
        self.transactions = transactions
        
    def getHeader(self):
        data = (
            self.index.to_bytes(4,'big')
            + bytes.fromhex(self.parent_hash)
            + bytes.fromhex(self.body_hash)
            + bytes.fromhex(self.target)
            + struct.pack(">d", self.timestamp)
            + self.nonce.to_bytes(8,'big')
        )
        return data

    def constructTransactions(self, data):
        transactions = []
        offset = 0
        no_of_trans = int.from_bytes(data[offset:offset+4], 'big')
        offset += 4
        for i in range(no_of_trans):
            size = int.from_bytes(data[offset:offset+4], 'big')
            offset += 4
            transactions.append(Trasaction(transactionFromByteArray(data[offset:offset+size])))
            offset += size
        return transactions

    def blockFromByte(self, data):
        self.index = int.from_bytes(data[:4], 'big')
        self.parent_hash = data[4:36].hex()
        self.body_hash = data[36:68].hex()
        self.target = data[68:100].hex()
        self.timestamp = struct.unpack(">d",data[100:108])
        self.nonce = int.from_bytes(data[108:116],'big')
        self.body = data[116:]
        self.transactions = self.constructTransactions(self.body)
        
    def blockToByte(self):
        data = (
            self.getHeader()
            + self.body
        )
        return data
        
    def save(self):
        with open('blocks/{}.dat'.format(self.index),'wb') as f:
            f.write(self.blockToByte())

    def GenesisBlock(self):
        self.target = '0000000f00000000000000000000000000000000000000000000000000000000'
        self.parent_hash = '0000000000000000000000000000000000000000000000000000000000000000'
