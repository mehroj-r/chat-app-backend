import os

def get_secret(secret_id, backup=None):
    return os.getenv(secret_id, backup)
