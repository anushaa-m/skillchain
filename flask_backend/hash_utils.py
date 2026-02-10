import hashlib

def generate_hash(file):

    file_bytes = file.read()

    sha256 = hashlib.sha256(file_bytes).hexdigest()

    return sha256