"""Compile the project's small gettext catalogs without an external msgfmt binary."""

from __future__ import annotations

import ast
import struct
from pathlib import Path


def parse_po(path: Path) -> dict[str, str]:
    messages: dict[str, str] = {}
    msgid: list[str] = []
    msgstr: list[str] = []
    active: list[str] | None = None

    def flush() -> None:
        nonlocal msgid, msgstr, active
        if msgid or msgstr:
            messages["".join(msgid)] = "".join(msgstr)
        msgid, msgstr, active = [], [], None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("msgid "):
            flush()
            active = msgid
            active.append(ast.literal_eval(line[6:]))
        elif line.startswith("msgstr "):
            active = msgstr
            active.append(ast.literal_eval(line[7:]))
        elif line.startswith('"') and active is not None:
            active.append(ast.literal_eval(line))
        elif not line:
            flush()
    flush()
    return {key: value for key, value in messages.items() if value or key == ""}


def write_mo(messages: dict[str, str], destination: Path) -> None:
    entries = sorted(
        (key.encode("utf-8"), value.encode("utf-8"))
        for key, value in messages.items()
    )
    count = len(entries)
    originals_offset = 28
    translations_offset = originals_offset + count * 8
    pool_offset = translations_offset + count * 8

    original_pool = bytearray()
    translation_pool = bytearray()
    original_table: list[tuple[int, int]] = []
    translation_table: list[tuple[int, int]] = []

    for original, _ in entries:
        original_table.append((len(original), pool_offset + len(original_pool)))
        original_pool.extend(original + b"\0")

    translation_pool_offset = pool_offset + len(original_pool)
    for _, translation in entries:
        translation_table.append(
            (len(translation), translation_pool_offset + len(translation_pool))
        )
        translation_pool.extend(translation + b"\0")

    payload = bytearray(
        struct.pack(
            "<7I",
            0x950412DE,
            0,
            count,
            originals_offset,
            translations_offset,
            0,
            0,
        )
    )
    for length, offset in original_table:
        payload.extend(struct.pack("<2I", length, offset))
    for length, offset in translation_table:
        payload.extend(struct.pack("<2I", length, offset))
    payload.extend(original_pool)
    payload.extend(translation_pool)

    destination.write_bytes(payload)


def main() -> None:
    locale_root = Path(__file__).resolve().parent.parent / "locale"
    for source in locale_root.glob("*/LC_MESSAGES/django.po"):
        destination = source.with_suffix(".mo")
        write_mo(parse_po(source), destination)
        print(f"compiled {source.relative_to(locale_root)}")


if __name__ == "__main__":
    main()
