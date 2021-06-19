import binascii


def tohex(val, nbits):
  return hex((val + (1 << nbits)) % (1 << nbits))


def gen_password(k, u):
    result = ''
    key = k
    u = binascii.hexlify(u)
    y = str(u, 'ascii')
    username = [y[i:i + 2] for i in range(0, len(y), 2)]

    for char in username:
        result = result + '\\'
        char_integer = int(char, 16)
        XOR = hex(char_integer ^ key)
        AL = int(XOR[-2:], 16)
        sub_AL = AL - 19
        AL_hex = tohex(sub_AL, 8)  # Last byte.
        result = result + AL_hex
    return result.replace('0', '')


if __name__ == '__main__':
    # Provide key as an integer and username in the b'yourstringhere' format.
    print('Use: ' + gen_password(12345678, b'AAAABBBB') + ' as password for the supplied key and username.')

