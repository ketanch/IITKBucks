import threading
from hashlib import sha256
from flask import Flask, request, jsonify
import json

app = Flask(__name__)
thread = None
nonce = None

def worker(data):
    global nonce
    n = 0
    target = 0x0000000f00000000000000000000000000000000000000000000000000000000
    while True:
        buff = (data+str(n)).encode()
        if int(sha256(buff).hexdigest(), 16) <= target:
            print("MINED")
            nonce = n
            return nonce
        n += 1

@app.route('/start', methods = ["POST"])
def start():
    data = json.loads(request.get_json())['data']
    thread = threading.Thread(target = worker, args = (data,))
    thread.start()
    return "Mining Started.", 200

@app.route('/result', methods = ["GET"])
def result():
    if nonce is None:
        return jsonify({"result":"searching", "nonce":-1})
    return jsonify({"result":"found", "nonce":nonce})

if __name__ == '__main__':
    app.run(debug=True, port = 8787)
