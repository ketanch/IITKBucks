from . import Block, Transaction
class BlockChain:
    
    def __init__(self):
        self.chain = []
        self.pendingTransactions = []
        self.unused_output = []
    
    def getPendingTransactions(self):
        pending_trans_list = []
        for transaction in self.pendingTransactions:
            pending_trans_list.append(transaction.as_json())
        return pending_trans_list
    
    def addBlock(self, new_block):
        self.chain.append(new_block)
