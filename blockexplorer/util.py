"""Block Explorer Util Module Documentation.

The Util module offers convenience functions to work motr efficiently with Block Explorer data.'


"""

import re
import os
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


def write_to_txt(data: str, file_name: str) -> None:
    """Function to write data to .txt file.

    Args:
        data: Data to be written to .txt file.
        file_name: Output file name. For example: raw_data.txt

    """

    assert isinstance(data, str), f'input must be of type str not: {type(data)}'

    with open(file_name, "w+", encoding="utf-8") as file:
        file.write(data)


def read_from_txt(file_name: str) -> list:
    """Function to read data from .txt file.

    Args:
        file_name: Data to be written to .txt file.

    Returns:
        Content of the .txt file

    """

    with open(file_name, "r", encoding="utf-8") as file:
        lines = []
        for next_line in file:
            lines.append(next_line.strip())

    return lines


def find_file_markers(data: str) -> Tuple[int, int, str]:
    """Function to identify the start and the end of a various file formats within a string.

    Args:
        data: String that contains the data. The string has to contain the data as hex values.

    Returns:
        The index of the start of the data file and the index of the end of the data within the input string.
        If no header is found also no footer will be returned.

    """

    formats = {
        'png': ['89504e470d', '44ae426082'],
        'jpg': ['ffd8', 'ffd9']
    }

    header_index = -1
    footer_index = -1
    file_type = None

    for item in formats.items():

        header_marker = item[1][0]
        footer_marker = item[1][1]

        header_index = data.find(header_marker)
        footer_index = data.find(footer_marker, header_index)

        if footer_index != -1:

            # Search for all End Of File markers and choose the last one, to safe guard against multiple occurrence.
            last_eof = [eof.start() for eof in re.finditer(footer_marker, data)][-1]

            footer_index = last_eof + len(footer_marker)
            file_type = item[0]

            if (footer_index - header_index) % 2 == 0:
                print(f'File of type {file_type} found.')
                break

    return header_index, footer_index, file_type


def match_markers(markers: list) -> Tuple[list, list]:
    """Function to validate and match file markers retrieve with find_file_markers.
    For example, Start of Image (SOI) or End of Image (EOI) markers can randomly occur in image
    as well as non-image data. The typical expectation is to find as many SOI markers as EOI markers.

    This function takes the SOI markers and looks for matches in the EOI markers based on two criteria:
    1. The EOI marker must come after the SOI marker
    2. The total length of the SOI to EOI interval must be even, otherwise decoding to binary is not possible

    Both measures improve the quality of the markers but are no guaranty that the markers are no false positive.

    Args:
        markers: dictionary
    """

    start_of_file = markers[0]
    end_of_file = []

    for sof in start_of_file:
        for eof in markers[1]:
            if eof > sof and (eof + sof) % 2 == 0:
                end_of_file.append(eof)
                break

    return start_of_file, end_of_file


def create_folder(directory: str) -> None:
    """"Function to create a new directory or a directory with sub-directories.py

    Args:
        directory: String that contains the directory structure to be created

    """
    if not os.path.isdir(directory):
        os.makedirs(directory)
