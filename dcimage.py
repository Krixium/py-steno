'''dcimage.py - Contains code for interacting with image files.

    Authors:
        Benny Wang
        William Murphy

    Functions:
        int_arr_to_rgb_arr(arr: list) -> list
        rgb_arr_to_int_arr(arr: list) -> list
        get_image_size(filename: str) -> [int, int]
        save_bytes_to_image(arr: list, filename: str, width: int, height: int)
'''
from PIL import Image


def int_arr_to_rgb_arr(arr: list) -> list:
    '''Converts a flat list of integer values to an array of RGB tuples.

    Example:
        [10, 20, 30, 40, 50, 60]
        becomes
        [(10, 20, 30), (40, 50, 60)]

    Args:
        arr (list): The array of integer values to turn into RGB tuples.

    Returns:
        output (list): An array of integer values in the pattern of [(r, g, b), (r, g, b) ...].
    '''
    output = []
    for i in range(0, len(arr), 3):
        output.append((arr[i], arr[i + 1], arr[i + 2]))
    return output


def rgb_arr_to_int_arr(arr: list) -> list:
    '''Flatens an array of RGB tuples to an array of ints.

    Example:
        [(10, 20, 30), (40, 50, 60)]
        becomes
        [10, 20, 30, 40, 50, 60]

    Args:
        arr (list): The array of RGB tuples

    Returns:
        output (list): An array of integer values in the pattern of [r, g, b, r, g, b, ...].
    '''
    output = []
    for tup in arr:
        for val in tup:
            output.append(val)
    return output


def get_image_size(filename: str) -> [int, int]:
    '''Gets the width and height of the image.

    Args:
        filename (str): The name of the image to get the height and width from.

    Returns:
        width (int), height (int) - The width and the height of the image given.
    '''
    image = Image.open(filename)
    return image.size


def get_bytes_from_image(filename: str):
    '''Extracts the RGB values of an image and returns it as a flattened array.

    Args:
        filename (str): The name of the image file.

    Returns:
        data (bytearray): A list of integers in the order of r, g, b, r, g, b, ...
    '''
    image = Image.open(filename)
    pixels = list(image.getdata())
    return rgb_arr_to_int_arr(pixels)


def save_bytes_to_image(arr: list, filename: str, width: int, height: int):
    """Saves a list of bytes as a PNG image.

    Args:
        arr (list): A flat array of rgb values.
        filename (str): The name to save the image as.
        width (int): The width of the new image.
        height (int): The height of the new image.

    """
    image = Image.new(mode='RGB', size=(width, height))
    image.putdata(int_arr_to_rgb_arr(arr))
    image.save(filename, 'PNG')