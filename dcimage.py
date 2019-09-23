from PIL import Image


def int_array_to_tuple_array(array):
    output = []
    for i in range(0, len(array), 3):
        output.append((array[i], array[i + 1], array[i + 2]))
    return output


def tuple_array_to_int_array(array):
    output = []
    for tup in array:
        for val in tup:
            output.append(val)
    return output


def get_image_size(filename):
    image = Image.open(filename)
    return image.size


def get_bytes_from_image(filename):
    image = Image.open(filename)
    pixels = list(image.getdata())
    return tuple_array_to_int_array(pixels)


def save_bytes_to_image(array, filename, width, height):
    image = Image.new(mode='RGB', size=(width, height))
    image.putdata(int_array_to_tuple_array(array))
    image.save(filename, 'PNG')