import hashlib
import os


class HashGenerator:
    def __init__(self, buffer_size=2**10):  # , hash_algos):
        '''
        HashGenerator constructor

        :returns: an instance of HashGenerator with a specified buffer size,
        or a buffer size of 2^10 by default.
        '''
        self.buffer_size = buffer_size
        # self.hash_algos = hash_algos

    def compute(self, algo, fpath):
        '''
        Function to compute the specified hash of the file.

        :param algo: the hash algorithm to run on the file at fpath
        :param fpath: the path to the file to run the hash algo on
        :returns: a string reprsenting the hash value of the file
        '''
        # verify that fpath is indeed a file, if so load it
        if not os.path.isfile(fpath):
            return {"success": False, "value": "Path given is not a file"}
        else:
            hash_algo = None
            # open the file and determine the hash algorithm
            with open(fpath, 'rb') as f:
                if algo == "MD5":
                    hash_algo = hashlib.md5()
                elif algo == "SHA1":
                    hash_algo = hashlib.sha1()
                elif algo == "SHA256":
                    hash_algo = hashlib.sha256()
                elif algo == "SHA512":
                    hash_algo = hashlib.sha512()
                else:
                    # unknown hash algorithm has been specified
                    return {
                        "success": False,
                        "value": "Algorithm not integrated yet."
                        }
                return {
                    "success": True,
                    "value": self.get_hash(f, hash_algo)
                    }

    def get_hash(self, f, file_hash):
        '''
        Evaluate the hash of the given file

        :param f: the file to compute the hash of
        :param file_hash: the hash algorithm to be used
        :returns: a string representing the hash or an exception
        '''
        try:
            while chunk := f.read(self.buffer_size):
                file_hash.update(chunk)
            return file_hash.hexdigest()
        except Exception as e:
            return e
