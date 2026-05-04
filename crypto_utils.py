# crypto_utils.py
"""
Low-level cryptographic helper functions.

Responsibilities:
- AES-GCM encryption/decryption
- SHA-256 hashing
- watermark token generation
- integrity tag generation
"""

import os
import json
import hmac
import base64
import hashlib
from typing import Dict, Any
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def b64e(data: bytes) -> str:
    """Encode bytes to Base64 string."""
    return base64.b64encode(data).decode("utf-8")


def b64d(data: str) -> bytes:
    """Decode Base64 string to bytes."""
    return base64.b64decode(data.encode("utf-8"))


def sha256_hex(text: str) -> str:
    """Return SHA-256 hex digest of a string."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def encrypt_message(aes_key: bytes, plaintext: str) -> tuple[str, str]:
    """
    Encrypt plaintext using AES-GCM.
    Returns:
        (nonce_b64, ciphertext_b64)
    """
    aesgcm = AESGCM(aes_key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    return b64e(nonce), b64e(ciphertext)


def decrypt_message(aes_key: bytes, nonce_b64: str, ciphertext_b64: str) -> str:
    """
    Decrypt AES-GCM ciphertext.
    Raises an exception if decryption or authentication fails.
    """
    aesgcm = AESGCM(aes_key)
    plaintext = aesgcm.decrypt(
        b64d(nonce_b64),
        b64d(ciphertext_b64),
        None
    )
    return plaintext.decode("utf-8")


def generate_token(
    token_key: bytes,
    sender: str,
    receiver: str,
    timestamp: int,
    message_id: str,
    ciphertext: str
) -> str:
    """
    Generate a dynamic context-bound watermark token.

    Bound fields:
    - sender
    - receiver
    - timestamp
    - message_id
    - ciphertext hash
    """
    ciphertext_hash = sha256_hex(ciphertext)
    token_data = f"{sender}|{receiver}|{timestamp}|{message_id}|{ciphertext_hash}"
    return hmac.new(
        token_key,
        token_data.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def canonical_json(data: Dict[str, Any]) -> str:
    """
    Stable JSON serialization for integrity calculation.
    """
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def generate_integrity_tag(integrity_key: bytes, package_core: Dict[str, Any]) -> str:
    """
    Generate integrity tag over package core fields.
    """
    serialized = canonical_json(data=package_core)
    return hmac.new(
        integrity_key,
        serialized.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()