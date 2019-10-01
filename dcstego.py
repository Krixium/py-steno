'''dcstego.py - Contains the high level code for the stenography process.

    Authors:
        Benny Wang
        William Murphy

    Functions:
        steno_image(key: bytes, msg: bytes, image: str) -> bytearray
        unsteno_image(key: bytes, image: str) -> bytearray
'''
import dcutils
import dcimage


def steno_image(key: bytes, msg: bytes, image: str) -> bytearray:
    '''Hides msg in image after encrypting it with key.

    Args:
        key (bytes): 16 bytes to use as the AES key.
        msg (bytes): The image to encrypt and then hide in the image.
        image (str): The name of the image to use as the carrier.

    Returns:
        carrier (bytearray): A bytearray that contains the steno'd RGB values of the image.
    '''
    # get packet to hide in image
    packet = dcutils.generate_packet(msg, key)

    # get bytes of the image
    carrier = dcimage.get_bytes_from_image(image)

    # check if the packet fits inside the carrier
    if len(packet) > calculate_max_packet_size(len(carrier)):
        raise BufferError('The packet is larger than what can be image.')

    # hide packet in image
    dcutils.stuff_packet_into_carrier(packet, carrier)

    # return the carrier bytes
    return carrier


def unsteno_image(key: bytes, image: str) -> bytearray:
    '''Extracts the message hidden in a steno'd image.

    Args:
        key (bytes): 16 bytes to use as the AES key.
        image (str): The name of the image to extract from.

    Returns:
        data (bytearray): The hidden message as a bytearray.
    '''
    # get the image bytes
    carrier = dcimage.get_bytes_from_image(image)

    # extract bits from bytes
    packet = dcutils.extract_packet_from_carrier(carrier)

    # return the bytes that were extracted from the image
    return dcutils.extract_msg_from_packet(packet, key)


def calculate_max_packet_size(carrier_size: int) -> int:
    '''Calculates the maximum packet size that can be stuffed into the carrier

    Args:
        carrier_size (int): The number of bytes in the carrier.

    Returns:
        max_size (int): The maximum total size of the packet. This includes the length header.
    '''
    return (carrier_size // 8) + 4

