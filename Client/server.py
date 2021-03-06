from flask import Flask, jsonify, Response, request
from modules.BlockChain import *
app = Flask(__name__)
import requests
from modeules.Block import Block
from modules.Transaction import Transaction
from modules.Verify import *
from random import randint
from miner import Miner
import time
from hashlib import sha256
from models.constants import *
import json

my_addr = '127.0.0.1'
peers = []
peer_limit = 4
potential_peers = []
blockchain = BlockChain()
_miner = Miner()
alias = {}
mapper = {}


def peer_limit_exceeded():
    if peer_limit > len(peers):
        return False
    return True

def transaction_selector(pending_trans):
    trans_list = []
    total_size = 0
    for i in pending_trans:
        curr_len = i.byte_length
        if total_size+curr_len > (1000000-116):
            break
        total_size += curr_len
        trans_list.append(i)
    return trans_list

def find_new_peers():
    url = {"url":my_addr}
    for peer in potential_peers:
        if peer_limit_exceeded():
            break
        req = requests.post(peer+'/newPeer', json = url)
        if req.status_code == 200:
            peers.append(peer)
        else:
            get_req = requests.get(peer+'/getPeers')
            peer_list = get_req.json()["peers"]
            for new_peer in peer_list:
                if new_peer not in potential_peers and new_peer not in peers:
                    potential_peers.append(new_peer)

def process_block(block):
    for transaction in block.transactions:
        for inp_arr in transaction.inp_arr:
            for inp in inp_arr:
                del blockchain.unused_output[(inp.transactionID, arr_index)]
        for out_arr in transaction.out_arr:
            for i in len(out_arr):
                out_dict = {(transaction.id, i):out_arr[i]}
                blockchain.unused_output.update(out_dict)
        if transaction in blockchain.pendingTransactions:
            blockchain.pendingTransactions.remove(transaction)
    blockchain.chain.append(block)
    block.save()

def blocks_from_peers():
    url = peers[randint(0, len(peers)-1)] + '/getBlock/'
    no = 0
    req = requests.get(url+str(no))
    while req.status_code != 404:
        block_data = req.content
        block = Block()
        block.blockFromByte(block_data)
        process_block(block)
        no += 1
        req = requests.get(url+str(no))

def pending_trans_from_peers():
    json_data = requests.get(peers[randint(0, len(peers)-1)] + '/getPendingTransactions').json()
    for trans_data in json_data:
        trans = Transaction()
        trans.from_json()
        blockchain.pendingTransactions.append(trans)
        
def start_mining():
    transactions = []
    while True:
        if blockchain.pendingTransactions is not []:
            transactions = transaction_selector(blockchain.pendingTransactions)
            break
        time.sleep(1)
    block = Block(index = len(blockchain.chain),parent_hash = sha256(blockchain.chain[-1].getHeader).hexdigest(), transactions = transactions, target = TARGET)
    block.constructBody()
    _miner.block = block
    _miner.start()

def start_system():
    find_new_peers()
    blocks_from_peers()
    pending_trans_from_peers()
    start_mining()

def post_mining_steps(block):
    for i in block.transactions:
        blockchain.pendingTransactions.remove(i)
        for j in i.inp_arr:
            del blockchain.unused_output[(j.transaction_ID, j.arr_index)]
        for index,j in enumerate(i.out_arr):
            blockchain.unused_output[(i.id, index)] = j
        blockchain.chain.append(block)
        block.save()
    for peer in peers:
        header = {'Content-Type':'application/octet-stream'}
        req = requests.post('{}/newBlock'.format(peer), headers=header, data=block.blockToByte())
        print(req.text)

@app.route('/addAlias', methods = ["POST"])
def addAlias():
    global alias
    data = request.get_json()
    temp_alias = data['alias']
    publicKey = data['publicKey']
    if temp_alias in alias.keys():
        return "Alias already added.", 400
    alias[temp_alias] = publicKey
    for peer in peers:
        req = requests.post('{}/addAlias'.format(peer), headers = {'Content-Type':'application/json'}, json = json.dumps(data))
    return "Alias added successfully :)", 200

@app.route('/getPublicKey', methods = ["GET", "POST"])
def getPublicKey():
    temp_alias = request.get_json()['alias']
    try:
        return jsonify({"publicKey":alias[temp_alias]})
    except:
        return "Alias currently not set :)", 200

@app.route('/getUnusedOutputs', methods = ["POST"])
def getUnusedOutputs():
    data = request.get_json()
    temp_alias = data.get('alias', None)
    publicKey = data.get('publicKey', None)
    if temp_alias is None and publicKey is None:
        return "Send something valid!", 404
    if temp_alias is None:
        temp_alias = next((k for k in alias if alias[k] == publicKey), None)
        if temp_alias is None:
            return "Alias for this public key doesn't exist.", 404
    unusedOutputs = mapper[temp_alias]
    out = []
    for i in unusedOutputs:
        dic = {"transactionId":i[0], "index":i[1], "amount":blockchain.unused_output[i].coin}
        out.append(dic)
    return jsonify({"unusedOutputs":out}), 200

@app.route('/getBlock/<int:block>', methods = ["GET"])
def getBlock(block):
    if block < len(blockchain.chain[block]):
        data = blockchain.chain[block].getBody()
        return Response(data, mimetype='application/octet-stream'), 200
    return "End of blockchain.", 404

@app.route('/getPendingTransactions', methods = ["GET"])
def getPendingTransactions():
    return jsonify(blockchain.getPendingTransactions())

@app.route('/newPeer', methods = ["POST"])
def new_peer():
    url = request.get_json()['url']
    peers.append(url)
    if peer_limit_exceeded():
        return "Peer limit exceeded.", 500
    if url in peers:
        return "Peer {} exists.".format(url), 500
    return "URL {} was added successfully.".format(url), 200

@app.route('/getPeers', methods = ["GET"])
def get_peer():
    return jsonify({"peers":peers})

@app.route('/newBlock', methods = ["POST"])
def new_block():
    block_data = request.get_data()
    new_block = Block()
    new_block.blockFromByte(block_data)
    if not verifyBlock(new_block):
        return "Invalid Block sent!!", 500
    _miner.halt()
    _miner.join()
    post_mining_steps(new_block)
    start_mining()
    blockchain.chain.append(new_block)
    return "Block successfully added.", 200

@app.route('/newTransaction', methods = ["POST"])
def new_transaction():
    json_data = request.get_json()
    transaction = Transaction()
    transaction.from_json(json_data)
    blockchain.pendingTransactions.append(transaction)
    return "Pending Transactions updated.", 200

if __name__ == '__main__':
    app.run(debug = True, port = 8787)
    start_system()
