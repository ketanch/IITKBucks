from flask import Flask, jsonify, Response, request
from models.BlockChain import *
app = Flask(__name__)

peers = []
blockchain = BlockChain()

@app.route('/getBlock/<int:block>', methods = ["GET"])
def getBlock(block):
    data = blockchain.chain[block].getBody()
    return Response(data, mimetype='application/octet-stream')

@app.route('/getPendingTransactions', methods = ["GET"])
def getPendingTransactions():
    return jsonify(blockchain.getPendingTransactions())

@app.route('/newPeer', methods = ["POST"])
def new_peer():
    url_data = request.get_json()
    peers.append(url_data['url'])
    return "URL {} was added successfully.".format(url_data['url']), 200

@app.route('/getPeers', methods = ["GET"])
def get_peer():
    return jsonify({"peers":peers})

@app.route('/newBlock', methods = ["POST"])
def new_block():
    block_data = request.get_data()
    new_block = Block()
    new_block.blockFromByte(block_data)
    blockchain.chain.append(new_block)
    return "Block successfully added.", 200

@app.route('/newTransaction', methods = ["POST"])
def new_transaction():
    json_data = request.get_json()
    transaction = Transaction()
    transaction.from_json(json_data)
    blockchain.pendingTransactions.append(transaction)
    return "Pending Transactions updated.", 200
