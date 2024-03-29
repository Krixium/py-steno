"""dcutils.py - Contains utility functions for things like encryption and data processing.

    Authors:
        Benny Wang
        William Murphy

    Functions:
        def generate_key(size) -> bytes:
        get_raw_bytes_from_file(filename: str) -> bytearray
        save_bytes_to_file(filename: str, data: bytearray)
        encrypt_data(key: bytearray, data: bytearray) -> bytearray
        decrypt_data(key: bytearray, data: bytearray) -> bytearray
        generate_packet(msg: bytearray, key:bytearray) -> bytearray
        extract_msg_from_packet(packet: bytearray, key: bytearray) -> bytearray
        get_bit_at_pos(val: bytearray, pos: int) -> int
        stuff_packet_into_carrier(packet: bytearray, carrier: bytearray)
        extract_packet_from_carrier(carrier: bytearray) -> bytearray
"""
import Crypto
from Crypto import Random
from Crypto import Cipher
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


# this is a fingerprint to identify files that have been stenod.
FINGERPRINT = b"DEADBEEF"


def generate_key(size: int) -> bytes:
    """Generates a key as a byte array

    Args:
        size (int): The length of bytes to generate.

    Returns:
        key (bytes): A random string of bytes.
    """
    return get_random_bytes(size)


def get_raw_bytes_from_file(filename: str) -> bytearray:
    """Reads a file as bytes into memory.

    Args:
        filename (str): The name of the file to read.

    Returns:
        data (bytearray): The raw data of the file. If an error occurs an empty array is returned.
    """
    try:
        file = open(filename, "rb")
        data = file.read()
        file.close()
        return data
    except IOError as io_error:
        print(io_error)
        return bytearray()


def save_bytes_to_file(filename: str, data: bytearray):
    """Saves a byte array to a file.

    Args:
        filename (str): The name of the file to write too.
        data (bytearray): The data to write to the file.
    """
    try:
        file = open(filename, "wb")
        file.write(data)
        file.close()
    except IOError as io_error:
        print(io_error)


def encrypt_data(key: bytearray, data: bytearray) -> bytearray:
    """Encrypts the given data with the given key using AES in CFB mode.

    Args:
        key (bytearray): A bytearray of size 16, 24, or 32. This decides the number of rounds.
        data (bytearray): The data to encrypt.

    Returns:
        cipher (bytearray): The initialization vector followed by the encrypted data.
    """
    init_vector = Random.new().read(Crypto.Cipher.AES.block_size)
    cipher = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CFB, init_vector)
    return init_vector + cipher.encrypt(data)


def decrypt_data(key: bytearray, data: bytearray) -> bytearray:
    """Decrypts the given data with the given key using AES in CFB mode.

    Args:
        key (bytearray): A bytearray of size 16, 24, or 32. This decides the number of rounds.
        data (bytearray): The data to decrypt.

    Returns:
        plaintext (bytearray): The plaintext message.
    """
    init_vector = bytes(data[0:16])
    cipher = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CFB, init_vector)
    return cipher.decrypt(bytes(data[16:]))


def generate_packet(msg: bytearray, key: bytearray) -> bytearray:
    """Generates a packet to stuff into an image.

    The format of the packet is:
        | len(4B) | data (len B) |

    len is a singed integer.

    Args:
        msg (bytearray): The plaintext message to packetize.
        key (bytearray): The key to use for encryption.

    Returns:
        packet (bytearray): The packet of data that can be stuffed into an image.
    """
    data = encrypt_data(key, FINGERPRINT + msg)
    length = int(len(data)).to_bytes(4, "big")
    return length + data


def extract_msg_from_packet(packet: bytearray, key: bytearray) -> bytearray:
    """Extracts message from the packet.

    Args:
        packet (bytearray): The incoming packet.
        key (bytearray): The key for decryption.

    Returns:
        msg (str): The plaintext contained in the packet.

    Raises:
        ValueError: The input data is malformed.
    """
    length = int.from_bytes(packet[0:4], byteorder="big")
    data = decrypt_data(key, packet[4:length + 4])

    if data[0:len(FINGERPRINT)] != FINGERPRINT:
        raise ValueError("This data is malformed. The fingerprint couldn\'t be found.")

    return data[len(FINGERPRINT):]


def get_bit_at_pos(val: bytearray, pos: int) -> int:
    """Gets the value of the bit at the given position of the byte

    Args:
        val (bytearray): The byte to extract from.
        pos (int): The position in the byte from 0 to 7.

    Returns:
        bit (int): 1 or 0 depending on the value at the given position.
    """
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

    if (val & mask) > 0:
        return 1
    else:
        return 0


def stuff_packet_into_carrier(packet: bytearray, carrier: bytearray):
    """Stuffs the packet into the carrier image. The packet is placed
    into the image bit by bit into the least significant bit of each byte
    of the carrier image.

    Args:
        packet (bytearray): The packet to stuff.
        carrier (bytearray): The carrier to hold the packet.
    """
    i = 0
    j = 0

    while i < len(packet):
        carrier[j + 0] = (carrier[j + 0] & 0xfe) | get_bit_at_pos(packet[i], 0)
        carrier[j + 1] = (carrier[j + 1] & 0xfe) | get_bit_at_pos(packet[i], 1)
        carrier[j + 2] = (carrier[j + 2] & 0xfe) | get_bit_at_pos(packet[i], 2)
        carrier[j + 3] = (carrier[j + 3] & 0xfe) | get_bit_at_pos(packet[i], 3)
        carrier[j + 4] = (carrier[j + 4] & 0xfe) | get_bit_at_pos(packet[i], 4)
        carrier[j + 5] = (carrier[j + 5] & 0xfe) | get_bit_at_pos(packet[i], 5)
        carrier[j + 6] = (carrier[j + 6] & 0xfe) | get_bit_at_pos(packet[i], 6)
        carrier[j + 7] = (carrier[j + 7] & 0xfe) | get_bit_at_pos(packet[i], 7)

        i = i + 1
        j = j + 8


def extract_packet_from_carrier(carrier: bytearray) -> bytearray:
    """Extracts the packet from the carrier image.

    Args:
        carrier (bytearray): The carrier to extract from.

    Returns:
        output (bytearray): The hidden packet.
    """
    output = bytearray()
    for i in range(0, len(carrier), 8):
        if i + 8 > len(carrier):
            break
        value = 0
        value += (carrier[i + 0] & 0x01) << 0
        value += (carrier[i + 1] & 0x01) << 1
        value += (carrier[i + 2] & 0x01) << 2
        value += (carrier[i + 3] & 0x01) << 3
        value += (carrier[i + 4] & 0x01) << 4
        value += (carrier[i + 5] & 0x01) << 5
        value += (carrier[i + 6] & 0x01) << 6
        value += (carrier[i + 7] & 0x01) << 7
        output.append(value)
    return output
