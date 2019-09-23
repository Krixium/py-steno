import dcutils


def test_stuffing():
    secret_bytes = [ 0x01, 0x02, 0x04, 0x08 ]
    carrier_bytes = [
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
        0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff]

    # stuffing test
    # stuff_secret_into_carrier(secret_bytes, carrier_bytes)
    dcutils.stuff_secret_into_carrier(secret_bytes, carrier_bytes)
    dcutils.debug_print_array_as_bits(secret_bytes)
    dcutils.debug_print_array_as_bits(carrier_bytes)


def test_packeting():
    # generating encrpyted packet test
    # byte string format = total length (4B) + msg
    key = b'Sixteen byte key'
    msg = 'the quick bronw fox jumps over the lazy dog'
    print("msg", dcutils.extract_packet(dcutils.generate_packet(msg, key), key))
