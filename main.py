#!/bin/python3.7

import dcimage
import dcstego
import dcutils


key = b'0123456789abcdef'
carrier_image_name = 'images/big-pic.jpg'
secret_image_name = 'images/jojo_meme_001.png'
steno_image_name = 'images/big-pic-stenod.png'
output_image_name = 'images/output.png'


def create_image():
    print('creating image')
    # get the data from the image to hide
    raw_secret_data = dcutils.get_raw_bytes_from_file(secret_image_name)
    # hide the image in another image
    steno_image = dcstego.steno_image(key, raw_secret_data, carrier_image_name)
    # write the new image to storage
    width, height = dcimage.get_image_size(carrier_image_name)
    dcimage.save_bytes_to_image(steno_image, steno_image_name, width, height)
    print('image created')


def extract_image():
    print('extracting image')
    extracted_data = dcstego.unsteno_image(key, steno_image_name)
    # we use generic file IO rather than PILLOW as data will not always be an image
    dcutils.save_bytes_to_file(output_image_name, extracted_data)
    print('image extracted')

try:
#    create_image()
    extract_image()

except BufferError as buffer_error:
    print(buffer_error)

except ValueError as value_error:
    print(value_error)


