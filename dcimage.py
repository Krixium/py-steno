from PIL import Image


def int_arr_to_tuple_arr(arr: list):
    output = []
    for i in range(0, len(arr), 3):
        output.append((arr[i], arr[i + 1], arr[i + 2]))
    return output


def tuple_arr_to_int_arr(arr: list):
    output = []
    for tup in arr:
        for val in tup:
            output.append(val)
    return output


def get_image_size(filename: str):
    image = Image.open(filename)
    return image.size


def get_bytes_from_image(filename: str):
    image = Image.open(filename)
    pixels = list(image.getdata())
    return tuple_arr_to_int_arr(pixels)


def save_bytes_to_image(arr: list, filename: str, width: int, height: int):
    image = Image.new(mode='RGB', size=(width, height))
    image.putdata(int_arr_to_tuple_arr(arr))
    image.save(filename, 'PNG')