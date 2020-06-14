from flask import Flask, jsonify, Response
from models.BlockChain import BlockChain 
app = Flask(__name__)

blockchain = BlockChain()

@app.route('/getBlock/<int:block>', methods = ["GET"])
def getBlock(block):
    data = blockchain.chain[block].getBody()
    return Response(data, mimetype='application/octet-stream')

@app.route('/getPendingTransactions', methods = ["GET"])
def getPendingTransactions():
    return jsonify(blockchain.getPendingTransactions())
