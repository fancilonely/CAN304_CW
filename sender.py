# sender.py

import time
import uuid
from typing import Dict, Any

from config import AES_KEY, TOKEN_KEY, INTEGRITY_KEY
from crypto_utils import (
    encrypt_message,
    generate_token,
    generate_integrity_tag,
)


def package_message(sender: str, receiver: str, plaintext: str) -> Dict[str, Any]:
    """
    Create a secure message package for transmission.
    Package includes:
      - ciphertext
      - token
      - integrity tag
      - metadata
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
        ciphertext=ciphertext
    )

    package_core = {
        "version": 1,
        "message_id": message_id,
        "sender": sender,
        "receiver": receiver,
        "timestamp": timestamp,
        "nonce": nonce,
        "ciphertext": ciphertext,
        "token": token,
    }

    integrity_tag = generate_integrity_tag(INTEGRITY_KEY, package_core)

    package = {
        **package_core,
        "integrity_tag": integrity_tag,
    }

    return package