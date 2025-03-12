import base64, json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def decrypt(message):
    with open("core/assets/keys.json", "r") as f:
        keys = json.load(f)
    private_key = keys["private"]
    key = RSA.import_key(base64.b64decode(private_key))
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(base64.b64decode(message)).decode()
