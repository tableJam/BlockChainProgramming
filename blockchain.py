import logging
import sys
import time
import util
import hashlib
import json
from ecdsa import NIST256p
from ecdsa import VerifyingKey

MD = 3
BLOCKCHAIN = 'HELLOWOLRD'
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def pprint(chains):
    for i, chain in enumerate(chains):
        print(f'{"="*25} Chain {i} {"="*25}')
        for k, v in chain.items():
            print(f'{k:20}{v}')
    print(f'{"*"*25}')

class BlockChain(object):
    def __init__(self,blockchain_address=None,port=None):
        self.transaction = []
        self.chain = []
        self.create_block(0,'init hash')
        self.address = '20001020'
        self.port = port
    
    def create_block(self,nonce,previous_hash):

        
        block = util.orderBlock({
            'timestanp':time.time(),
            'transaction':self.transaction,
            'nonce':nonce,
            'previous_hash':previous_hash
        })
        self.chain.append(block)
        self.transaction = []
        return block

    def hash(self,block):
        sorted_block = json.dumps(block,sort_keys=True)
        return hashlib.sha256(sorted_block.encode()).hexdigest()

    def verify_transaction(self,sender_public_key,transaction,sign):
        sha256 = hashlib.sha256()
        sha256.update(str(transaction).encode('utf-8'))
        message = sha256.digest()
        sign_byte = bytes().fromhex(sign)
        verify_key = VerifyingKey.from_string(
            bytes().fromhex(sender_public_key),curve=NIST256p
        )
        return verify_key.verify(sign_byte,message)


    def add_transaction(self,sender_address,resp_address,value,sender_public_key,sign):
        transaction = util.orderBlock(
            {
                'sender_address':sender_address,
                'resp_address':resp_address,
                'sender_public_key':sender_public_key,
                'sign':sign,
                'value':float(value)
            }
        )
        if sender_address == BLOCKCHAIN:
            self.transaction.append(transaction)
            return True;
        if self.verify_transaction(sender_public_key,transaction,sign):
            self.transaction.append(transaction)
            return True
        else:
            return False
    def create_transaction(self,sender_address,resp_address,value,sender_public_key,sign):
        is_transaction = self.add_transaction(sender_address,resp_address,value,sender_public_key,sign)
        #TODO
        #sync with other NODE
        return is_transaction


    def __valid_proof(self,transaction,previous_hash,nunce):
        guess_block = {
            'transaction':transaction,
            'previous_hash':previous_hash,
            'nunce':nunce
        }
        result = self.hash(guess_block)
        return result[:MD] == '0'*MD

    def proof_of_works(self):
        transaction = self.transaction.copy()
        previous_hash = self.hash(self.chain[-1])
        nunce = 0
        while self.__valid_proof(transaction,previous_hash,nunce) is False:
            nunce += 1
        return nunce

    def mining(self):
        self.add_transaction(BLOCKCHAIN,self.address,1.0)
        nunce = self.proof_of_works()
        previous_hash = self.hash(self.chain[-1])
        self.create_block(nunce,previous_hash)
        return True
    
    def calculate_total_amount(self,address):
        amount = 0.0
        for block in self.chain:
            for transaction in block['transaction']:
                value = transaction['value']
                if address == transaction['resp_address']:
                    amount += value
                if address == transaction['sender_address']:
                    amount += value
        return amount
