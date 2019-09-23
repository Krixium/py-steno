import Crypto
from Crypto import Random


def encrypt_data(key, data):
    init_vector = Random.new().read(Crypto.Cipher.AES.block_size)
    cipher = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CFB, init_vector)
    return init_vector + cipher.encrypt(data)


def decrypt_data(key, data):
    init_vector = data[0:16]
    cipher = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CFB, init_vector)
    return cipher.decrypt(data[16:])


def generate_packet(msg, key):
    data = encrypt_data(key, msg)
    length = int(len(data)).to_bytes(4, 'big')
    return length + data


def extract_msg_from_packet(packet, key):
    length = int.from_bytes(packet[0:4], byteorder='big')
    return decrypt_data(key, packet[4:length + 4])


def get_bit_at_pos(byte, pos):
    mask = 0xff
    if pos == 0:
        mask = 0x01
    if pos == 1:
        mask = 0x02
    if pos == 2:
        mask = 0x04
    if pos == 3:
        mask = 0x08
    if pos == 4:
        mask = 0x10
    if pos == 5:
        mask = 0x20
    if pos == 6:
        mask = 0x40
    if pos == 7:
        mask = 0x80

    if (byte & mask) > 0:
        return 1
    else:
        return 0


def stuff_secret_into_carrier(secret, carrier):
    i = 0
    j = 0

    while i < len(secret):
        carrier[j + 0] = (carrier[j + 0] & 0xfe) | get_bit_at_pos(secret[i], 0)
        carrier[j + 1] = (carrier[j + 1] & 0xfe) | get_bit_at_pos(secret[i], 1)
        carrier[j + 2] = (carrier[j + 2] & 0xfe) | get_bit_at_pos(secret[i], 2)
        carrier[j + 3] = (carrier[j + 3] & 0xfe) | get_bit_at_pos(secret[i], 3)
        carrier[j + 4] = (carrier[j + 4] & 0xfe) | get_bit_at_pos(secret[i], 4)
        carrier[j + 5] = (carrier[j + 5] & 0xfe) | get_bit_at_pos(secret[i], 5)
        carrier[j + 6] = (carrier[j + 6] & 0xfe) | get_bit_at_pos(secret[i], 6)
        carrier[j + 7] = (carrier[j + 7] & 0xfe) | get_bit_at_pos(secret[i], 7)

        i = i + 1
        j = j + 8


def extract_packet_from_carrier(carrier):
    output = []
    for i in range(0, len(carrier), 8):
        if i + 8 > len(carrier) - 1:
            break
        value = 0
        value += carrier[i + 0] & 0xfe << 0
        value += carrier[i + 1] & 0xfe << 1
        value += carrier[i + 2] & 0xfe << 2
        value += carrier[i + 3] & 0xfe << 3
        value += carrier[i + 4] & 0xfe << 4
        value += carrier[i + 5] & 0xfe << 5
        value += carrier[i + 6] & 0xfe << 6
        value += carrier[i + 7] & 0xfe << 7
        output.append(value)
    return output


def debug_print_array_as_bits(array):
    i = 0
    for num in array:
        print(format(num, '08b'), end=' ')
        if i % 8 == 7:
            print()
        i = i + 1
    print()
    print()