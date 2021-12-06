from Crypto.Cipher          import AES
from Crypto                 import Random
from Crypto.Protocol.KDF    import PBKDF2
import base64
import hashlib
import os

class AESCipher:
    def __init__(self):
        self.blocksize = 16
        self.pad = lambda s: s + (self.blocksize - len(s) % self.blocksize) * chr(self.blocksize - len(s) % self.blocksize)
        self.unpad = lambda s: s[0:-s[-1]]
        self.key = hashlib.sha256(os.environ.get('SALT'))
    
    def get_private_key(random):
        salt = hashlib.sha256(os.environ.get('SALT'))
        kdf = PBKDF2(random, salt, 64, 1000) # PBKDF2(PRF, Password, Salt, iteration, DLen)
        key = kdf[:32]
        return key
    
    def encrypt(self, random, raw):
        private_key = self.get_private_key(random)
        raw = self.pad(raw).encode('utf-8')
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))
    
    def decrypt(self, random, enc):
        private_key = self.get_private_key(random)
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[16:]))
    
    def encrypt_str(self, raw):
        return self.encrypt(raw).decode('utf-8')
    
    def decrypt_str(self, enc):
        return self.decrypt(enc).decode('utf-8')