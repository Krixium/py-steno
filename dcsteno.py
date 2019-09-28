import dcutils
import dcimage


def steno_image():
    key = b'sixteen byte key'
    msg = 'the quick brown fox jumps over the lazy dog'

    # get packet to hide in image
    secret = dcutils.generate_packet(msg, key)

    # get bytes of the image
    carrier = dcimage.get_bytes_from_image('images/jojo_meme_001.png')

    # hide packet in image
    dcutils.stuff_packet_into_carrier(secret, carrier)

    width, height = dcimage.get_image_size('images/jojo_meme_001.png')

    # save image
    dcimage.save_bytes_to_image(carrier, 'images/jojo_meme_001_stuffed.png', width, height)


def unsteno_image():
    key = b'sixteen byte key'

    # get the image bytes
    carrier = dcimage.get_bytes_from_image('images/jojo_meme_001_stuffed.png')

    # extract bits from bytes
    packet = dcutils.extract_packet_from_carrier(carrier)

    # extract message
    msg = dcutils.extract_msg_from_packet(packet, key)

    print(msg)