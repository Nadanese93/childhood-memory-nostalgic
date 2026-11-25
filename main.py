"""Write the childhood-memory entry for the make.fun bounty.

The entry is a single sentence recalling a childhood memory. This script
validates it against the bounty gate (1-280 characters, not only
whitespace, exactly one sentence) and writes it, byte-for-byte, to
entry.txt in the output directory. After writing, it re-reads the file
and verifies the bytes on disk match the entry exactly.
"""

import os

ENTRY = (
    "The barber sat me on a stack of phone books so I could reach the mirror, "
    "dusted my neck with talc, and for years after, every haircut smelled like "
    "the first time someone treated me like a grown-up."
)


def _check_length(entry: str) -> None:
    if not 1 <= len(entry) <= 280:
        raise ValueError(
            f"entry length out of gate: must be 1-280 characters, got {len(entry)}"
        )


def _check_not_blank(entry: str) -> None:
    if not entry.strip():
        raise ValueError("entry must not be only whitespace")


def _check_single_line(entry: str) -> None:
    if "\n" in entry or "\r" in entry:
        raise ValueError(
            "entry must be exactly one sentence on a single line (no line breaks)"
        )


def validate(entry: str) -> None:
    """Raise a clear error if the entry fails any part of the bounty gate."""
    _check_length(entry)
    _check_not_blank(entry)
    _check_single_line(entry)


def _verify_written(path: str, entry: str) -> None:
    """Re-read entry.txt and raise if the bytes differ from the entry."""
    with open(path, "rb") as f:
        written = f.read()
    expected = entry.encode("utf-8")
    if written != expected:
        raise ValueError(
            f"verification failed: {path} does not match the entry "
            f"({len(written)} bytes on disk, {len(expected)} expected)"
        )


def main() -> None:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    _verify_written(path, ENTRY)
    print(f"wrote {path} ({len(ENTRY)} characters, verified)")


if __name__ == "__main__":
    main()
