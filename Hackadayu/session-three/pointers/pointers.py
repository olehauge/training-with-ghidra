from binascii import hexlify

from typing import List


def to_hex(val: int, nbits: int) -> str:
    return hex((val + (1 << nbits)) % (1 << nbits))


def gen_password(key: int, username: bytes) -> str:
    result: str = ''
    username_hex: bytes = hexlify(username)
    username_ascii = str(username_hex, 'ascii')
    username_split: List[str] = [username_ascii[i:i + 2] for i in range(0, len(username_ascii), 2)]
    random_value: int = 197921880

    for char in username_split:
        result += '\\'
        char_integer = int(char, 16)
        char_key: int = char_integer + key          # First addition
        xor: str = hex(char_key ^ random_value)     # XOR
        al = int(xor[-2:], 16)                      # Get last byte
        sub_al: int = al - 19                       # Subtract 19
        al_hex: str = to_hex(sub_al, 8)             # Last byte
        result += al_hex
    return result.replace('0', '')


if __name__ == '__main__':
    # Provide key as an integer and password in the b'yourstringhere' format.
    print('Use: ' + gen_password(12345678, b'CCCCDDDD') + ' as username for the supplied key and password.')

