# app.py

from sender import package_message
from receiver import verify_and_receive


def main():
    package = package_message(
        sender="alice",
        receiver="bob",
        plaintext="This is a confidential one-time message."
    )

    print("=== Generated Package ===")
    print(package)

    print("\n=== First Verification ===")
    print(verify_and_receive(package, expected_receiver="bob"))

    print("\n=== Second Verification ===")
    print(verify_and_receive(package, expected_receiver="bob"))


if __name__ == "__main__":
    main()