from Block import block
from BlockChain import BlockChain
from hashlib import sha256
from constants.py import BLOCK_REWARD

def verifyBlock(block, blockchain = None):
    if block.index is 0:
        verifyFirstBlock()
    parent_hash = sha256(blockchain.chain[block.index-1].getHeader()).hexdigest()
    if parent_hash is not block.parent_hash:
        return False
    if sha256(block.body.hexdigest() is not block.body_hash):
        return False
    if int(sha256(block.getHeader()).hexdigest(),16) > int(block.target, 16):
        return False
    #Verify transaction data
    transaction_fee = 0
    for index,transaction in enumerate(block.transactions):
        if index is 0:
            pass
        if not transaction.isValid():
            return False
        transaction_fee += transactionFee(transaction, blockchain)
    transaction_fee += BLOCK_REWARD
    return verifyFirstTransaction(block.transactions[0], transaction_fee):

def verifyFirstTransaction(transaction, transaction_fee):
    if len(transaction.inp_arr) is not 0 or len(transaction.out_arr) is not 1:
        return False
    if transaction.out_arr[0].coin > transaction_fee:
        return False
    return True

def verifyFirstBlock(block):
    parent_hash = '0000000000000000000000000000000000000000000000000000000000000000'
    target = '0000000f00000000000000000000000000000000000000000000000000000000'
    if block.parent_hash is not parent_hash or block.target is not target or len(block.transactions) is not 1:
        return False
    return True

def transactionFee(transaction, blockchain):
    out_coin = 0
    inp_coin = 0
    for i in transaction.inp_arr:
        inp_coin += blockchain.unused_output[(i.transaction_ID, i.arr_index)].coin
    for i in transaction.out_arr:
        out_coin += i.coin
    return (inp_coin-out_coin)
