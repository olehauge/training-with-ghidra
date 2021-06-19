from binascii import hexlify


def tohex(val: int, nbits: int) -> str:
  return hex((val + (1 << nbits)) % (1 << nbits))


def gen_password(key: int, username: bytes) -> str:
    result: str = ''
    username_hex: bytes = hexlify(username)
    username_ascii = str(username_hex, 'ascii')
    username_split: list[str] = [username_ascii[i:i + 2] for i in range(0, len(username_ascii), 2)]

    for char in username_split:
        result += '\\'
        char_integer = int(char, 16)
        XOR: str = hex(char_integer ^ key)
        AL = int(XOR[-2:], 16)
        sub_AL: int = AL - 19
        AL_hex: str = tohex(sub_AL, 8)  # Last byte.
        result += AL_hex
    return result.replace('0', '')


if __name__ == '__main__':
    # Provide key as an integer and username in the b'yourstringhere' format.
    print('Use: ' + gen_password(12345678, b'AAAABBBB') + ' as password for the supplied key and username.')
