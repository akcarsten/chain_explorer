"""Block Explorer Util Module Documentation.

The Util module offers convenience functions to work motr efficiently with Block Explorer data.'


"""

from typing import Tuple


def write_binary_to_file(data: bytes, file_name: str) -> None:
    """Function to write binary data to file.

    Args:
        data: Binary data to be written to file.
        file_name: Output file name. For example: image.jpg

    """

    assert type(data) is bytes, "Input data is not of type bytes"

    f = open(file_name, "wb")
    f.write(data)
    f.close()


def find_jpg_markers(data: str) -> Tuple[int, int]:
    """Function to identify the start and the end of a jpg file within a string.

    Args:
        data: String that contains the jpg image. The string has to contain the jpg as hex values.

    Returns:
        The index of the start of the jpg image and the index of the end of the image within the input string.

    """

    header_index = data.find('ffd8')
    footer_index = data.find('ffd9', header_index)

    return header_index, footer_index
