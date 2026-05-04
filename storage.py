# storage.py
"""
One-time usage state manager.

Current version:
- In-memory storage only

Future upgrade:
- Replace with SQLite or another persistent backend
- Keep the same function signatures
"""

from typing import Set

_USED_MESSAGE_IDS: Set[str] = set()


def is_message_used(message_id: str) -> bool:
    """Return True if the message has already been consumed."""
    return message_id in _USED_MESSAGE_IDS


def mark_message_used(message_id: str) -> None:
    """Mark a message as consumed."""
    _USED_MESSAGE_IDS.add(message_id)


def reset_used_messages() -> None:
    """Clear all one-time usage records. Mainly for testing/demo."""
    _USED_MESSAGE_IDS.clear()


def get_used_message_count() -> int:
    """Return number of consumed messages currently stored."""
    return len(_USED_MESSAGE_IDS)