# receiver.py

import time
from typing import Dict, Any, Tuple

from config import (
    AES_KEY,
    TOKEN_KEY,
    INTEGRITY_KEY,
    ALLOWED_TIME_SKEW,
    USED_MESSAGE_IDS,
)
from crypto_utils import (
    decrypt_message,
    generate_token,
    generate_integrity_tag,
)


REQUIRED_FIELDS = [
    "version",
    "message_id",
    "sender",
    "receiver",
    "timestamp",
    "nonce",
    "ciphertext",
    "token",
    "integrity_tag",
]


def _check_required_fields(package: Dict[str, Any]) -> Tuple[bool, str]:
    for field in REQUIRED_FIELDS:
        if field not in package:
            return False, f"REJECT: missing field '{field}'"
    return True, "OK"


def _check_metadata(package: Dict[str, Any], expected_receiver: str) -> Tuple[bool, str]:
    if package["receiver"] != expected_receiver:
        return False, "REJECT: metadata mismatch (wrong receiver)"

    now = int(time.time())
    if abs(now - int(package["timestamp"])) > ALLOWED_TIME_SKEW:
        return False, "REJECT: metadata mismatch (timestamp outside allowed window)"

    return True, "OK"


def _rebuild_core(package: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": package["version"],
        "message_id": package["message_id"],
        "sender": package["sender"],
        "receiver": package["receiver"],
        "timestamp": package["timestamp"],
        "nonce": package["nonce"],
        "ciphertext": package["ciphertext"],
        "token": package["token"],
    }


def verify_and_receive(package: Dict[str, Any], expected_receiver: str) -> Tuple[bool, str]:
    """
    Verify the incoming package according to the prototype pipeline.

    Returns:
        (success, message)
    """
    ok, msg = _check_required_fields(package)
    if not ok:
        return False, msg

    ok, msg = _check_metadata(package, expected_receiver)
    if not ok:
        return False, msg

    package_core = _rebuild_core(package)
    expected_integrity = generate_integrity_tag(INTEGRITY_KEY, package_core)
    if expected_integrity != package["integrity_tag"]:
        return False, "REJECT: integrity check failed"

    expected_token = generate_token(
        TOKEN_KEY,
        sender=package["sender"],
        receiver=package["receiver"],
        timestamp=int(package["timestamp"]),
        message_id=package["message_id"],
        ciphertext=package["ciphertext"],
    )
    if expected_token != package["token"]:
        return False, "REJECT: watermark token mismatch"

    if package["message_id"] in USED_MESSAGE_IDS:
        return False, "REJECT: one-time usage already consumed"

    try:
        plaintext = decrypt_message(
            AES_KEY,
            package["nonce"],
            package["ciphertext"]
        )
    except Exception:
        return False, "REJECT: legal decryption failed"

    USED_MESSAGE_IDS.add(package["message_id"])
    return True, f"ACCEPT: {plaintext}"