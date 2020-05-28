from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)

dictionary = {}
peers = ["http://localhost:12346/add","http://localhost:12347/add"]

def update_log(write_data):
    f = open('LOGFILE','a')
    f.write(write_data)
    f.close()

@app.route('/')
def hello():
    return "Visit either /add or /list to access a service."

@app.route('/add', methods=["POST"])
def _add():
    global dictionary
    try:
        req_data = request.get_json()
        key = req_data['key']
        value = req_data['value']
    except:
        write_data = "HOST : {} : Data received in invalid format.\n".format(request.remote_addr)
        update_log(write_data)
        return "Invalid format sent!"
    resp = ''
    if key in dictionary.keys():
        write_data = "HOST : {} : Key sent {} already existed.\n".format(request.remote_addr, key)
        resp = "Value already exists."
    else :
        dictionary[key] = value
        write_data = "HOST : {} : Key-value {}:\'{}\' added.\n".format(request.remote_addr, key, value)
        resp = "Successfully added."
        print("Updated database:\n",dictionary)
        write_data += "Sending request to peers...\n"
        for peer in peers:
            sent = requests.post(peer, json={"key":key,"value":value})
            write_data += "\tHOST : {} : Status code : {} : Received : {}\n".format(peer, sent.status_code, sent.text)
    update_log(write_data)
    return resp, 200

@app.route('/list', methods=["GET"])
def _list():
    write_data = "HOST : {} : Database sent.\n".format(request.remote_addr)
    update_log(write_data)
    return jsonify(dictionary)

if __name__ == '__main__':
    app.run(port = 12345)
