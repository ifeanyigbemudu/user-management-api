import bcrypt

def hash_password(password: str):
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt)


def check_password(password: str, hashed: bytes):
    if bcrypt.checkpw(password.encode("utf-8"), hashed):
        return True
    else:
        return False
