import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def encrypt(public_key, message):
    key = RSA.import_key(base64.b64decode(public_key))
    cipher = PKCS1_OAEP.new(key)
    return base64.b64encode(cipher.encrypt(message.encode())).decode()
