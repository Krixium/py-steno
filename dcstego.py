'''dcstego.py - Contains the high level code for the stenography process.

    Authors:
        Benny Wang
        William Murphy

    Functions:
        steno_image(key: bytes, msg: bytes, image: str) -> bytearray
        unsteno_image(key: bytes, image: str) -> bytearray
        calculate_max_packet_size(carrier_size: int) -> int
        is_carrier_format_valid(filename: str) -> bool
'''
import dcutils
import dcimage


# These are the supported input formats for carrier images.
SUPPORTED_CARRIER_TYPES: list = ['png', 'jpg', 'jpeg', 'bmp', 'gif']

# This is the supported output format of the steno'd image.
SUPPORTED_OUTPUT_TYPE: str = 'png'


def steno_image(key: bytes, msg: bytes, image: str) -> bytearray:
    '''Hides msg in image after encrypting it with key.

    Args:
        key (bytes): 16 bytes to use as the AES key.
        msg (bytes): The image to encrypt and then hide in the image.
        image (str): The name of the image to use as the carrier.

    Returns:
        carrier (bytearray): A bytearray that contains the steno'd RGB values of the image.

    Raises:
        BufferError: If the packet is larger than what can be carried by the image.
        ValueError: If the format of the image is not supported.
    '''
    # check image format
    if not is_carrier_format_valid(image):
        raise ValueError("The carrier image format is not supported.")

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

    Raises:
        ValueError: If the image format is not supported.
    '''
    # check the input image type
    image_format = image.split('.')[-1].lower()
    if image_format != SUPPORTED_OUTPUT_TYPE:
        raise ValueError('This image format is not supported.')

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
    # carrier should have 8 bytes per 1 byte of data plus 4 for the header
    return (carrier_size // 8) + 4


def is_carrier_format_valid(filename: str) -> bool:
    '''Checks if the carrier image type is supported.

    Args:
        filename (str): The name to check.

    Returns:
        True if the image type is supported, false otherwise.
    '''
    image_format = filename.split('.')[-1].lower()
    for entry in SUPPORTED_CARRIER_TYPES:
        if entry == image_format:
            return True
    return False
