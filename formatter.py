# formatter.py
"""
Formatting helpers for display/demo output.

Responsibilities:
- section titles
- package pretty print
- verification result pretty print
- validation table print
"""

from typing import Dict, Any


def print_title(title: str) -> None:
    line = "=" * 60
    print(f"\n{line}")
    print(title)
    print(line)


def shorten(value: Any, max_len: int = 48) -> str:
    text = str(value)
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


def print_package(package: Dict[str, Any]) -> None:
    print_title("Generated Package")
    ordered_fields = [
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
    for key in ordered_fields:
        value = package.get(key, "")
        print(f"{key:<15}: {shorten(value, 72)}")


def print_verification_result(result: Dict[str, Any]) -> None:
    print_title("Verification Result")
    print(f"{'status':<15}: {result.get('status')}")
    print(f"{'reason':<15}: {result.get('reason')}")
    print(f"{'plaintext':<15}: {result.get('plaintext')}")


def print_menu() -> None:
    print_title("Dynamic Watermarking Prototype")
    print("1. Generate secure message package")
    print("2. Verify current message package")
    print("3. Run validation scenarios")
    print("4. Reset one-time usage state")
    print("5. Show current usage state count")
    print("0. Exit")


def print_validation_header() -> None:
    print_title("Prototype Validation Results")
    print(f"{'Scenario':<38} {'Expected':<10} {'Actual':<10} Reason")
    print("-" * 90)


def print_validation_row(title: str, expected: str, actual_result: Dict[str, Any]) -> None:
    actual = actual_result.get("status", "")
    reason = actual_result.get("reason", "")
    print(f"{title:<38} {expected:<10} {actual:<10} {reason}")