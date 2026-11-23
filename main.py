#!/usr/bin/env python3
"""Entrypoint for news-image-20261123 (standard library only).

Checks that entry.png next to this file is a genuine JPEG under the
1 MiB cap and 1024x1024, then copies it to the output directory:
argv[1] first, then the MAKEFUN_OUTPUT_DIR environment variable,
then ./out next to this script.
"""
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
MAX_BYTES = 1024 * 1024


def jpeg_size(path):
    """Return (width, height) by parsing JPEG SOF markers (stdlib only)."""
    with open(path, "rb") as f:
        data = f.read()
    if len(data) < 4 or data[0:2] != b"\xff\xd8" or data[2] != 0xFF:
        raise ValueError("not a JPEG (bad SOI marker)")
    pos = 2
    while pos + 9 < len(data):
        if data[pos] != 0xFF:
            raise ValueError("bad JPEG marker at offset %d" % pos)
        marker = data[pos + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        seg_len = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        if marker in (0xC0, 0xC1, 0xC2):
            height, width = struct.unpack(">HH", data[pos + 5:pos + 9])
            return width, height
        pos += 2 + seg_len
    raise ValueError("no JPEG SOF marker found")


def main():
    if not os.path.isfile(SRC):
        print("FAIL: entry.png missing next to main.py", file=sys.stderr)
        return 1
    size = os.path.getsize(SRC)
    if size > MAX_BYTES:
        print("FAIL: entry.png is %d bytes, over the 1 MiB cap" % size, file=sys.stderr)
        return 1
    try:
        width, height = jpeg_size(SRC)
    except ValueError as exc:
        print("FAIL: %s" % exc, file=sys.stderr)
        return 1
    if (width, height) != (1024, 1024):
        print("FAIL: entry.png is %dx%d, expected 1024x1024" % (width, height), file=sys.stderr)
        return 1
    if len(sys.argv) > 1:
        outdir = sys.argv[1]
    elif os.environ.get("MAKEFUN_OUTPUT_DIR"):
        outdir = os.environ["MAKEFUN_OUTPUT_DIR"]
    else:
        outdir = os.path.join(HERE, "out")
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, "entry.png")
    shutil.copyfile(SRC, dst)
    print("OK: entry.png %dx%d %d bytes -> %s" % (width, height, size, dst))
    return 0


if __name__ == "__main__":
    sys.exit(main())
