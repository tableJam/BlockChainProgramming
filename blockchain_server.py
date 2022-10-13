from ast import parse
from crypt import methods
import json

from requests import request
from flask import Flask
from flask import jsonify

import blockchain
import wallet
import transaction

app = Flask(__name__)
prev = {}

def get_blockchain():
 if not prev:
        minner_wallet = wallet.Wallet();
        block_chain = blockchain.BlockChain(minner_wallet.blockchain_address,app.config['port'])
        prev['blockchain'] = block_chain
 return prev['blockchain']


@app.route('/',methods=['GET','POST'])
def start_blockchain():
    blockchain = get_blockchain()
    response = {
        'chain':blockchain
    }
    return jsonify(response),200

@app.route('/transaction',methods=['GET','POST'])
def transaction():
    block_chain = get_blockchain()
    if request.method == 'GET':
        return jsonify({'transaction':block_chain.transaction_pool,'length':len(block_chain.transaction_pool)}), 200
    if request.method == 'POST':
        request_json = request.json
        TRANSACTION = transaction()
        required = {
            'sender_blockchain_address',
            'resp_blockchain_address',
            'value',
            'sing'
        }
        if not all(k in required for k in request_json):
            return jsonify({'message':'🤔 lack of infomation that you need'}), 400
        is_created = block_chain.create_transaction(
            request_json['sender_adress'],
            request_json['resp_address'],
            request_json['sender_public_key'],
            request_json['value']
        )
    return jsonify({'message':'OK'}),200 if is_created else jsonify({'message':'FAIL'}),400








@app.route('/show')
def show():
    return '<h1>🚀😍⛓️❤️💥</h1>'


if __name__ == '__main__':
    from argparse import ArgumentParser;
    parser = ArgumentParser()
    parser.add_argument('-p','--port',default=5000,type=int,help='port to linsten on')
    args = parser.parse_args()
    port = args.port
    app.config['port'] = port

    app.run(host='0.0.0.0',port=port)

