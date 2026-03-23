#!/usr/bin/env python3
"""Compile django.po to django.mo without GNU gettext (uses polib)."""
from pathlib import Path

import polib


def main() -> None:
    root = Path(__file__).resolve().parent
    for po_path in root.joinpath("locale").rglob("*.po"):
        mo_path = po_path.with_suffix(".mo")
        po = polib.pofile(str(po_path))
        po.save_as_mofile(str(mo_path))
        print(f"Compiled {po_path.relative_to(root)} -> {mo_path.relative_to(root)}")


if __name__ == "__main__":
    main()
