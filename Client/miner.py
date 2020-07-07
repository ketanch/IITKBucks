import threading
from hashlib import sha256
from modules.Block import Block

class Miner(threading.Thread):
    def __init__(self, block):
        super().__init__()
        self.kill = threading.Event()
        self.block = block

    def run(self):
        status_code = 404
        for i in range(2**64):
            self.block.nonce = i
            self.block.timestamp = time.time()
            if int(sha256(self.getHeader()).hexdigest(),16) <= int(self.block.target,16) or self.kill.is_set():
                status_code = 200
                break
        return {"status":status_code}
    
    def halt(self):
        self.kill.set()
