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

    assert isinstance(data, bytes), "Input data is not of type bytes"

    with open(file_name, "wb") as file:
        file.write(data)


def find_file_markers(data: str) -> Tuple[int, int, str]:
    """Function to identify the start and the end of a various file formats within a string.

    Args:
        data: String that contains the data. The string has to contain the data as hex values.

    Returns:
        The index of the start of the data file and the index of the end of the data within the input string.
        If no header is found also no footer will be returned.

    """

    formats = {
        'jpg': ['ffd8', 'ffd9'],
        'png': ['89504e470d', '44ae426082']
    }

    header_index = -1
    footer_index = -1
    file_type = None

    for item in formats.items():
        header_index = data.find(item[1][0])
        footer_index = data.find(item[1][1], header_index)

        if footer_index != -1 and (footer_index - header_index) % 2 == 0:
            print(f'File of type {item[0]} found.')

            footer_index = footer_index + len(item[1][1])
            file_type = item[0]

            break

    return header_index, footer_index, file_type
