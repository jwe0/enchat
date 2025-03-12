import base64
from Crypto.PublicKey import RSA


def key_gen():
    key = RSA.generate(2048)
    
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    data = {
        "private" : base64.b64encode(private_key).decode(),
        "public" : base64.b64encode(public_key).decode()
    }
    return data
