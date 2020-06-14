from . import Block
class BlockChain:

    def getPendingTransactions():
        pending_trans_list = []
        for transaction in self.pendingTransactions:
            pending_trans_list.append(transaction.as_json())
        return pending_trans_list
