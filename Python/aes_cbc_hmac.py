#!/usr/bin/env python3
"""
AES-CBC + PKCS7 + HMAC-SHA256 (truncated to 8 bytes)

Inputs:
  - AES key (128 or 256 bits) in hex
  - HMAC key (256 bits) in hex
  - IV (16 bytes) in hex
  - Plaintext from string, hex, or file
HMAC input (default): IV || ciphertext
"""

import argparse
import binascii
import sys
from typing import Tuple

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes, hmac


def _hex_to_bytes(s: str) -> bytes:
    s = s.strip().lower().replace("0x", "").replace(" ", "")
    return binascii.unhexlify(s)


def pkcs7_pad(block_size_bytes: int, data: bytes) -> bytes:
    """PKCS#7 pad to a multiple of block_size_bytes (16 for AES)."""
    padder = padding.PKCS7(block_size_bytes * 8).padder()
    return padder.update(data) + padder.finalize()


def aes_cbc_encrypt(aes_key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()


def hmac_sha256_truncated(hkey: bytes, data: bytes, truncate_len: int = 8) -> bytes:
    h = hmac.HMAC(hkey, hashes.SHA256())
    h.update(data)
    tag_full = h.finalize()
    return tag_full[:truncate_len]


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="AES-CBC (PKCS7) + HMAC-SHA256 (truncated to 8 bytes)"
    )
    ap.add_argument("--aes-key", required=True, help="AES key (hex), 16 or 32 bytes")
    ap.add_argument("--hmac-key", required=True, help="HMAC-SHA256 key (hex), 32 bytes")
    ap.add_argument("--iv", required=True, help="IV (hex), 16 bytes")

    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--pt", help="Plaintext as UTF-8 string")
    src.add_argument("--pt-hex", help="Plaintext as hex string")
    src.add_argument("--pt-file", help="Plaintext from file (read as raw bytes)")

    ap.add_argument(
        "--hmac-over",
        choices=["ciphertext", "iv+ciphertext", "plaintext"],
        default="iv+ciphertext",
        help="What to authenticate (default: iv+ciphertext)",
    )
    ap.add_argument(
        "--out-format",
        choices=["hex", "base64"],
        default="hex",
        help="Output encoding for ciphertext and tag",
    )
    return ap.parse_args()


def load_plaintext(args: argparse.Namespace) -> bytes:
    if args.pt is not None:
        return args.pt.encode("utf-8")
    if args.pt_hex is not None:
        return _hex_to_bytes(args.pt_hex)
    if args.pt_file is not None:
        with open(args.pt_file, "rb") as f:
            return f.read()
    raise ValueError("No plaintext source provided")


def validate_lengths(aes_key: bytes, hmac_key: bytes, iv: bytes) -> None:
    if len(aes_key) not in (16, 32):
        raise ValueError(f"AES key must be 16 or 32 bytes, got {len(aes_key)}")
    if len(hmac_key) != 32:
        raise ValueError(f"HMAC key must be 32 bytes, got {len(hmac_key)}")
    if len(iv) != 16:
        raise ValueError(f"IV must be 16 bytes, got {len(iv)}")


def encode_output(b: bytes, fmt: str) -> str:
    if fmt == "hex":
        return binascii.hexlify(b).decode("ascii")
    elif fmt == "base64":
        import base64

        return base64.b64encode(b).decode("ascii")
    else:
        raise ValueError("Unsupported output format")


def main() -> int:
    args = parse_args()

    try:
        aes_key = _hex_to_bytes(args.aes_key)
        hmac_key = _hex_to_bytes(args.hmac_key)
        iv = _hex_to_bytes(args.iv)
        validate_lengths(aes_key, hmac_key, iv)

        plaintext = load_plaintext(args)
        padded = pkcs7_pad(16, plaintext)
        ciphertext = aes_cbc_encrypt(aes_key, iv, padded)

        if args.hmac_over == "ciphertext":
            hmac_input = ciphertext
        elif args.hmac_over == "iv+ciphertext":
            hmac_input = iv + ciphertext
        elif args.hmac_over == "plaintext":
            hmac_input = plaintext
        else:
            raise ValueError("Invalid --hmac-over choice")

        tag8 = hmac_sha256_truncated(hmac_key, hmac_input, 8)

        print("ciphertext:", encode_output(ciphertext, args.out_format))
        print("hmac_trunc8:", encode_output(tag8, args.out_format))
        return 0
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

