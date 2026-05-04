# test_scenarios.py

from copy import deepcopy

from sender import package_message
from receiver import verify_and_receive
from crypto_utils import generate_integrity_tag
from config import INTEGRITY_KEY, USED_MESSAGE_IDS


def print_result(title: str, result):
    print(f"\n=== {title} ===")
    print(result)


def rebuild_core(package: dict) -> dict:
    """
    Rebuild the package core fields used for integrity calculation.
    Must match sender.py / receiver.py logic exactly.
    """
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


def main():
    # reset in-memory one-time state for clean testing
    USED_MESSAGE_IDS.clear()

    # create one fresh valid package
    original_pkg = package_message(
        sender="alice",
        receiver="bob",
        plaintext="Top secret message."
    )

    # -----------------------------
    # T1 Normal Reception
    # -----------------------------
    USED_MESSAGE_IDS.clear()
    pkg1 = deepcopy(original_pkg)
    result1 = verify_and_receive(pkg1, expected_receiver="bob")
    print_result("T1 Normal Reception", result1)

    # -----------------------------
    # T2 Message Tampering
    # Change ciphertext directly without recomputing integrity tag
    # Expected: integrity check fails
    # -----------------------------
    USED_MESSAGE_IDS.clear()
    pkg2 = deepcopy(original_pkg)
    pkg2["ciphertext"] = pkg2["ciphertext"][:-2] + "AA"
    result2 = verify_and_receive(pkg2, expected_receiver="bob")
    print_result("T2 Message Tampering", result2)

    # -----------------------------
    # T3 Token Mismatch
    # Change token, then recompute integrity tag so that
    # it passes integrity but fails token verification
    # -----------------------------
    USED_MESSAGE_IDS.clear()
    pkg3 = deepcopy(original_pkg)
    pkg3["token"] = "deadbeef" * 8  # fake 64-hex token
    pkg3["integrity_tag"] = generate_integrity_tag(
        INTEGRITY_KEY,
        rebuild_core(pkg3)
    )
    result3 = verify_and_receive(pkg3, expected_receiver="bob")
    print_result("T3 Token Mismatch", result3)

    # -----------------------------
    # T4 Metadata Mismatch / Wrong Receiver
    # Change receiver in package, recompute integrity tag,
    # but receiver expected by system remains "bob"
    # Expected: metadata mismatch
    # -----------------------------
    USED_MESSAGE_IDS.clear()
    pkg4 = deepcopy(original_pkg)
    pkg4["receiver"] = "charlie"
    pkg4["integrity_tag"] = generate_integrity_tag(
        INTEGRITY_KEY,
        rebuild_core(pkg4)
    )
    result4 = verify_and_receive(pkg4, expected_receiver="bob")
    print_result("T4 Metadata Mismatch / Wrong Receiver", result4)

    # -----------------------------
    # T5 Replay / Reuse
    # Use same valid package twice
    # Expected: first accept, second reject
    # -----------------------------
    USED_MESSAGE_IDS.clear()
    pkg5 = deepcopy(original_pkg)
    result5_first = verify_and_receive(pkg5, expected_receiver="bob")
    result5_second = verify_and_receive(pkg5, expected_receiver="bob")
    print_result("T5 Replay First Attempt", result5_first)
    print_result("T5 Replay Second Attempt", result5_second)


if __name__ == "__main__":
    main()