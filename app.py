# app.py
"""
Menu-driven demo entry for the CAN304 prototype.
"""

from typing import Optional, Dict, Any

from sender import package_message
from receiver import verify_and_receive
from storage import reset_used_messages, get_used_message_count
from formatter import (
    print_menu,
    print_package,
    print_verification_result,
    print_title,
)
from test_scenarios import run_validation_scenarios


def prompt_non_empty(prompt_text: str) -> str:
    while True:
        value = input(prompt_text).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def generate_package_interactive() -> Dict[str, Any]:
    print_title("Generate Secure Message Package")
    sender = prompt_non_empty("Sender: ")
    receiver = prompt_non_empty("Receiver: ")
    plaintext = prompt_non_empty("Plaintext message: ")

    package = package_message(sender=sender, receiver=receiver, plaintext=plaintext)
    print_package(package)
    return package


def verify_package_interactive(current_package: Optional[Dict[str, Any]]) -> None:
    if current_package is None:
        print("\nNo package is currently loaded. Please generate a package first.")
        return

    print_title("Verify Current Message Package")
    expected_receiver = prompt_non_empty("Expected receiver: ")
    result = verify_and_receive(current_package, expected_receiver=expected_receiver)
    print_verification_result(result)


def reset_state_interactive() -> None:
    reset_used_messages()
    print("\nOne-time usage state has been reset.")


def show_state_count() -> None:
    print(f"\nCurrent consumed-message count: {get_used_message_count()}")


def main() -> None:
    current_package: Optional[Dict[str, Any]] = None

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            current_package = generate_package_interactive()

        elif choice == "2":
            verify_package_interactive(current_package)

        elif choice == "3":
            run_validation_scenarios()

        elif choice == "4":
            reset_state_interactive()

        elif choice == "5":
            show_state_count()

        elif choice == "0":
            print("\nExiting prototype. Goodbye.")
            break

        else:
            print("\nInvalid option. Please choose again.")


if __name__ == "__main__":
    main()