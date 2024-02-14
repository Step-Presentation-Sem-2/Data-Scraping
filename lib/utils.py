import hashlib


def hash_bytes(content: bytes):
    image_hash = hashlib.md5()
    image_hash.update(content)
    return image_hash.hexdigest()
