#!/usr/bin/python

import dcimage
import dcstego

key = b'0123456789abcdef'
msg = b'The quick brown fox jumps over the lazy dog'

width, height = dcimage.get_image_size('images/jojo_meme_001.png')

print('creating image')
steno_image = dcstego.steno_image(key, msg, 'images/jojo_meme_001.png')
dcimage.save_bytes_to_image(steno_image, 'images/jojo_meme_001_stuffed.png', width, height)

print('extracting message')
secret_msg = dcstego.unsteno_image(key, 'images/jojo_meme_001_stuffed.png')
print(secret_msg)