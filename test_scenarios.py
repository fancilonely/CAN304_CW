# test_scenarios.py
"""
Formal validation scenarios for the prototype.

Scenarios:
- T1 Normal Reception
- T2 Message Tampering
- T3 Token Mismatch
- T4 Metadata Mismatch / Wrong Receiver
- T5 Replay / Reuse
"""

from copy import deepcopy

from sender import package_message
from receiver import verify_and_receive, rebuild_core
from crypto_utils import generate_integrity_tag
from config import INTEGRITY_KEY
from storage import reset_used_messages


def print_case(title: str, expected: str, actual_result: dict) -> None:
    actual = actual_result["status"]
    reason = actual_result["reason"]
    print(f"{title:<35} Expected: {expected:<7} Actual: {actual:<7} Reason: {reason}")


def main():
    original_pkg = package_message(
        sender="alice",
        receiver="bob",
        plaintext="Top secret message."
    )

    print("=== Prototype Validation Results ===")

    # T1 Normal Reception
    reset_used_messages()
    pkg1 = deepcopy(original_pkg)
    result1 = verify_and_receive(pkg1, expected_receiver="bob")
    print_case("T1 Normal Reception", "ACCEPT", result1)

    # T2 Message Tampering
    reset_used_messages()
    pkg2 = deepcopy(original_pkg)
    pkg2["ciphertext"] = pkg2["ciphertext"][:-2] + "AA"
    result2 = verify_and_receive(pkg2, expected_receiver="bob")
    print_case("T2 Message Tampering", "REJECT", result2)

    # T3 Token Mismatch
    reset_used_messages()
    pkg3 = deepcopy(original_pkg)
    pkg3["token"] = "deadbeef" * 8
    pkg3["integrity_tag"] = generate_integrity_tag(INTEGRITY_KEY, rebuild_core(pkg3))
    result3 = verify_and_receive(pkg3, expected_receiver="bob")
    print_case("T3 Token Mismatch", "REJECT", result3)

    # T4 Metadata Mismatch / Wrong Receiver
    reset_used_messages()
    pkg4 = deepcopy(original_pkg)
    pkg4["receiver"] = "charlie"
    pkg4["integrity_tag"] = generate_integrity_tag(INTEGRITY_KEY, rebuild_core(pkg4))
    result4 = verify_and_receive(pkg4, expected_receiver="bob")
    print_case("T4 Metadata Mismatch / Wrong Receiver", "REJECT", result4)

    # T5 Replay / Reuse
    reset_used_messages()
    pkg5 = deepcopy(original_pkg)
    first_result = verify_and_receive(pkg5, expected_receiver="bob")
    second_result = verify_and_receive(pkg5, expected_receiver="bob")
    print_case("T5 Replay First Attempt", "ACCEPT", first_result)
    print_case("T5 Replay Second Attempt", "REJECT", second_result)


if __name__ == "__main__":
    main()