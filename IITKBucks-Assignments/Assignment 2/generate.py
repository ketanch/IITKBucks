from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
text = input("ENTER TEXT : ").encode()
pri_key = RSA.import_key(open('private.pem').read())
h = SHA256.new(text)
signature = pss.new(pri_key).sign(h)
print("The signature for this data is :\n",bytearray(signature).hex())