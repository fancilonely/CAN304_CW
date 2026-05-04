# config.py

AES_KEY = b"0123456789ABCDEF0123456789ABCDEF"   # 32 bytes for AES-256
TOKEN_KEY = b"token-secret-key-32-bytes-long!!"
INTEGRITY_KEY = b"integrity-secret-key-32bytes!"

# metadata time window in seconds
ALLOWED_TIME_SKEW = 300

# simple in-memory one-time usage record for prototype stage
USED_MESSAGE_IDS: set[str] = set()