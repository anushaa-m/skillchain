import hashlib

def generate_hash(file):
    file.seek(0)   # ⭐ CRITICAL FIX
    file_bytes = file.read()
    file.seek(0)   # reset again so Flask can still use file later

    return hashlib.sha256(file_bytes).hexdigest()
