import time
import struct
import hashlib

class BlockBodyMake:
    def __init__(self, inps, body=None):
        self.no_of_inp = len(inps)
        self.inps = inps
        self.body = body
    
    def getBody(self):
        self.body = self.no_of_inp.to_bytes(4, 'big')
        for i in range(self.no_of_inp):
            self.body += len(self.inps[i]).to_bytes(4, 'big')+self.inps
        return self.body

    def getBodyHash(self):
        return hashlib.sha256(self.body).hexdigest()

class BlockHeaderMake:
    def __init__(self, index, parent_hash, block_body_hash, target):
        self.index = index
        self.parent_hash = parent_hash
        self.block_body_hash = block_body_hash
        self.target = target
        self.nonce = None
        self.timestamp = None
        self.header = None
    
    def Header(self):
        self.header = self.index.to_bytes(4, 'big')+bytes.fromhex(self.parent_hash)+bytes.fromhex(self.block_body_hash)+bytes.fromhex(self.target)+bytes(struct.pack("f", self.timestamp))+self.nonce.to_bytes(8, 'big')
        return self.header

    def HeaderHash(self):
        return hashlib.sha256(self.Header()).hexdigest()
    
    def findNonceAndTimestamp(self):
        for i in range(2**64):
            self.nonce = i
            self.timestamp = time.time()
            if int(self.HeaderHash(),16) <= int(self.target,16):
                break
        return [self.nonce, self.timestamp, self.HeaderHash()]
