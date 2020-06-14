class Output:
    def __init__(self, coin, pub_key):
        self.coin = int(coin)
        self.pub_key = pub_key
        self.key_len = len(pub_key)

    def show(self):
        print("\tNo of coins: ", self.coin)
        print("\tLength of public key: ", self.key_len)
        print("\tPublic Key:\n", self.pub_key)

    def generateByte(self):
        byte_coin = self.coin.to_bytes(8, 'big')
        byte_pub_key = self.pub_key.encode()
        byte_key_len = self.key_len.to_bytes(4, 'big')
        byte_final = byte_coin+byte_key_len+byte_pub_key
        return byte_final
    
    def as_json(self):
        json_data = {}
        json_data["amount"] = self.coin
        json_data["recepient"] = self.pub_key
        return json_data
