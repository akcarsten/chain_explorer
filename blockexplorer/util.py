"""Block Explorer Util Module Documentation.

The Util module offers convenience functions to work motr efficiently with Block Explorer data.'


"""

def write_binary_to_file(data: bytes, file_name: str) -> None:
    """Function to write ninary data to file.

    Args:
        data: Binary data to be written to file.
        file_name: Output file name. For example: image.jpg

    """

    assert type(data) is bytes, "Input data is not of type bytes"

    f = open(file_name, "wb")
    f.write(data)
    f.close()
