# receiver.py
"""
Receiver-side verification logic.

Verification order:
1. required fields
2. metadata consistency
3. integrity tag
4. watermark token
5. one-time usage
6. legal decryption

Return format:
{
    "status": "ACCEPT" or "REJECT",
    "reason": "...",
    "plaintext": str or None
}
"""

import time
from typing import Dict, Any, Optional

from config import AES_KEY, TOKEN_KEY, INTEGRITY_KEY, ALLOWED_TIME_SKEW, PACKAGE_VERSION
from crypto_utils import (
    decrypt_message,
    generate_token,
    generate_integrity_tag,
)
from storage import is_message_used, mark_message_used


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


def reject(reason: str) -> Dict[str, Any]:
    """Standard reject result."""
    return {
        "status": "REJECT",
        "reason": reason,
        "plaintext": None,
    }


def accept(plaintext: str) -> Dict[str, Any]:
    """Standard accept result."""
    return {
        "status": "ACCEPT",
        "reason": "valid message",
        "plaintext": plaintext,
    }


def rebuild_core(package: Dict[str, Any]) -> Dict[str, Any]:
    """Rebuild core fields for integrity verification."""
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


def check_required_fields(package: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Check missing required fields."""
    for field in REQUIRED_FIELDS:
        if field not in package:
            return reject(f"missing field: {field}")
    return None


def check_metadata(package: Dict[str, Any], expected_receiver: str) -> Optional[Dict[str, Any]]:
    """Check metadata consistency."""
    if package["version"] != PACKAGE_VERSION:
        return reject("unsupported package version")

    if package["receiver"] != expected_receiver:
        return reject("metadata mismatch (wrong receiver)")

    now = int(time.time())
    if abs(now - int(package["timestamp"])) > ALLOWED_TIME_SKEW:
        return reject("metadata mismatch (timestamp outside allowed window)")

    return None


def check_integrity(package: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Check integrity tag."""
    package_core = rebuild_core(package)
    expected_integrity = generate_integrity_tag(INTEGRITY_KEY, package_core)
    if expected_integrity != package["integrity_tag"]:
        return reject("integrity check failed")
    return None


def check_token(package: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Check watermark token."""
    expected_token = generate_token(
        TOKEN_KEY,
        sender=package["sender"],
        receiver=package["receiver"],
        timestamp=int(package["timestamp"]),
        message_id=package["message_id"],
        ciphertext=package["ciphertext"],
    )
    if expected_token != package["token"]:
        return reject("watermark token mismatch")
    return None


def check_one_time_usage(package: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Check one-time usage status."""
    if is_message_used(package["message_id"]):
        return reject("one-time usage already consumed")
    return None


def verify_and_receive(package: Dict[str, Any], expected_receiver: str) -> Dict[str, Any]:
    """
    Full receiver-side verification pipeline.
    """
    result = check_required_fields(package)
    if result:
        return result

    result = check_metadata(package, expected_receiver)
    if result:
        return result

    result = check_integrity(package)
    if result:
        return result

    result = check_token(package)
    if result:
        return result

    result = check_one_time_usage(package)
    if result:
        return result

    try:
        plaintext = decrypt_message(
            AES_KEY,
            package["nonce"],
            package["ciphertext"]
        )
    except Exception:
        return reject("legal decryption failed")

    mark_message_used(package["message_id"])
    return accept(plaintext)