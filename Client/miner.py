import threading
from hashlib import sha256

class Miner(threading.Thread):
    def __init__(self):
        super().__init__()
        self.kill = threading.Event()

    def run(self, block):
        status_code = 404
        for i in range(2**64):
            block.nonce = i
            block.timestamp = time.time()
            if int(sha256(self.getHeader()).hexdigest(),16) <= int(block.target,16) or self.kill.is_set():
                status_code = 200
                break
        return {"status":status_code}
    
    def halt(self):
        self.kill.set()
