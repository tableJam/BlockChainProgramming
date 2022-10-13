class Transaction(object):
    def __init__(self,sender_private_key,sender_public_key,sender_blockchain_address,resp_blockchain_address,value):
        self.sender_private_key = sender_private_key;
        self.sender_public_key = sender_public_key;
        self.sender_blockchain_address = sender_blockchain_address
        self.resp_blockchain_address = resp_blockchain_address
        self.value = value
    
    def sign(self):
        sha256 = hashlib.sha256()
        transaction = util.orderDict({
            'sender_blockchain_address':self.sender_blockchain_address,
            'resp_blockchain_address':self.resp_blockchain_address,
            'value':float(self.value)
        })
        sha256.update(str(transaction).encode('utf-8'))
        message = sha256.digest()
        private_key = SigningKey.from_string(bytes().fromhex(self.sender_private_key),curve=NIST256p)
        private_key_sign = private_key.sign(message)
        sign = private_key_sign.hex()
        return sign