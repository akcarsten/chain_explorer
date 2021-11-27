def write_binary_to_file(data: bytes, filename: str) -> None:
    """Function to write ninary data to file.

    Args:
        data: Binary data to be written to file.
        filename: Output file name. For example: image.jpg

    """

    assert type(data) is bytes, "Input data is not of type bytes"

    f = open(filename, "wb")
    f.write(data)
    f.close()
