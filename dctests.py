import dcutils


def test_stuffing():
    secret_bytes = [ 0x01, 0x02, 0x04, 0x08 ]
    carrier_bytes = [
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff]

    # stuffing test
    dcutils.stuff_packet_into_carrier(secret_bytes, carrier_bytes)
    dcutils.debug_print_array_as_bits(secret_bytes)
    dcutils.debug_print_array_as_bits(carrier_bytes)
    output = dcutils.extract_packet_from_carrier(carrier_bytes)
    dcutils.debug_print_array_as_bits(output)


def test_packeting():
    # generating encrpyted packet test
    # byte string format = total length (4B) + msg
    key = b'Sixteen byte key'
    msg = 'the quick bronw fox jumps over the lazy dog'
    print("msg", dcutils.extract_msg_from_packet(dcutils.generate_packet(msg, key), key))
