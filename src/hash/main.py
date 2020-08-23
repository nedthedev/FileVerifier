import hashlib
import os

class HashGenerator:
    def __init__(self, hash_algos):
        self.hash_algos = hash_algos

    def compute(self, type, fpath):
        if not os.path.isfile(fpath):
            return {"success": False, "value": "Path given is not a file"}
        if type == "MD5":
            return {"success": True, "value": self.md5(fpath)}
        elif type == "SHA1":
            return {"success": True, "value": self.sha1(fpath)}
        elif type == "SHA256":
            return {"success": True, "value": self.sha256(fpath)}
        elif type == "SHA512":
            return {"success": True, "value": self.sha512(fpath)}
        else:
            return {"success": False, "value": "Algorithm not integrated yet."}

    def md5(self, fpath):
            return hashlib.md5(open(fpath,'rb').read()).hexdigest()

    def sha1(self, fpath):
        return hashlib.sha1(open(fpath,'rb').read()).hexdigest()

    def sha256(self, fpath):
        return hashlib.sha256(open(fpath,'rb').read()).hexdigest()

    def sha512(self, fpath):
        return hashlib.sha512(open(fpath,'rb').read()).hexdigest()