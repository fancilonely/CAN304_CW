# sender.py
"""
Sender-side packaging logic.
Builds a secure package from plaintext input.
"""

import time
import uuid
from typing import Dict, Any

from config import AES_KEY, TOKEN_KEY, INTEGRITY_KEY, PACKAGE_VERSION
from crypto_utils import (
    encrypt_message,
    generate_token,
    generate_integrity_tag,
)


def build_package_core(
    version: int,
    message_id: str,
    sender: str,
    receiver: str,
    timestamp: int,
    nonce: str,
    ciphertext: str,
    token: str,
) -> Dict[str, Any]:
    """Build package core fields."""
    return {
        "version": version,
        "message_id": message_id,
        "sender": sender,
        "receiver": receiver,
        "timestamp": timestamp,
        "nonce": nonce,
        "ciphertext": ciphertext,
        "token": token,
    }


def package_message(sender: str, receiver: str, plaintext: str) -> Dict[str, Any]:
    """
    Package a plaintext message into a secure transmission package.
    """
    message_id = str(uuid.uuid4())
    timestamp = int(time.time())

    nonce, ciphertext = encrypt_message(AES_KEY, plaintext)

    token = generate_token(
        TOKEN_KEY,
        sender=sender,
        receiver=receiver,
        timestamp=timestamp,
        message_id=message_id,
        ciphertext=ciphertext,
    )

    package_core = build_package_core(
        version=PACKAGE_VERSION,
        message_id=message_id,
        sender=sender,
        receiver=receiver,
        timestamp=timestamp,
        nonce=nonce,
        ciphertext=ciphertext,
        token=token,
    )

    integrity_tag = generate_integrity_tag(INTEGRITY_KEY, package_core)

    package = {
        **package_core,
        "integrity_tag": integrity_tag,
    }

    return package