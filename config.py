# config.py
"""
Central configuration for the CAN304 prototype.
Team members should only change fixed global settings here.
"""

AES_KEY = b"0123456789ABCDEF0123456789ABCDEF"   # 32 bytes for AES-256
TOKEN_KEY = b"token-secret-key-32-bytes-long!!"
INTEGRITY_KEY = b"integrity-secret-key-32bytes!"

# Allowed time difference (seconds) between current time and package timestamp
ALLOWED_TIME_SKEW = 300

# Package version for compatibility / future extension
PACKAGE_VERSION = 1