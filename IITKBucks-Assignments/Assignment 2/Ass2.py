from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

path = input("Enter the path to public key : ")
message = input("Enter unencrypted message : ").encode()
signature = input("Enter the signature : ")
pub_key = RSA.import_key(open(path).read())
a=bytes.fromhex(signature)
sha256hash = SHA256.new(message)
verifier = pss.new(pub_key)
try:
	verifier.verify(sha256hash, a)
	print("\nThe Signature is authentic")
except(ValueError, TypeError):
	print("\nThe Signature is not authentic")