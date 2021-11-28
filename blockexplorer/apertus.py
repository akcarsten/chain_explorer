"""Block Explorer Apertus Module Documentation.

The Apertus module offers downloads and decodes data from the Bitcoin blockchain that was uploaded
via the AtomSea & EMBII tool.'


"""

from blockexplorer import explorer as exp
from blockexplorer import util

# TEXT DECODING NEEDS TO BE IMPLEMENTED


def __extract_transactions(out_scripts: str) -> list:
    """Function to extract transaction hashes from a string.
    The string is expected to come from the AtomSea & EMBII encoding.

    Args:
        out_scripts: Concatenated string from all output scripts in the root transaction.

    Returns:
        List of all transactions belonging to the uploaded data set.

    """

    binary_scripts = exp.decode_hex_message(out_scripts)[0]
    utf8_scripts = binary_scripts.decode('utf-8', errors='ignore')
    formatted_scripts = utf8_scripts.split('\r\n')
    formatted_scripts[0] = formatted_scripts[0][:64]

    return formatted_scripts[:-1]


def __extract_jpg(scripts: str, header_index: int, footer_index: int) -> bytes:
    """Function to extract the jpg data from a hex string.
    The result is decoded to bytes and can be directly written to file

    Args:
        scripts: Hex string that contains jpg data
        header_index: Start of the jpg data
        footer_index: End of the jpg data

    Returns:
        jpg image in binary format.

    """

    image = scripts[header_index:footer_index + 4]  # add 4 bytes to include the complete footer (ffd9)

    return exp.decode_hex_message(image)[0]


def download_image(tx_hash: str, file_name: str, max_value: float = float('inf')) -> None:
    """Function to download image data encoded in the AtomSea & EMBII encoding.
    The result will be written to file

    Args:
        tx_hash: root transaction hash
        file_name: filename under which the result will be saved. The correct extension will be added automatically.
        max_value: Allows to set a threshold for the value of each transaction that will be included.
        Typically scripts of interest are in transactions with low value.

    """

    raw_tx = exp.get_transaction(tx_hash)

    out_scripts = exp.collect_out_scripts(raw_tx, max_value=max_value)
    out_scripts = ''.join(out_scripts)

    tx_list = __extract_transactions(out_scripts)

    scripts = exp.collect_multi_out_scripts(tx_list, max_value=max_value)
    scripts = ''.join(scripts)

    header_index, footer_index = util.find_jpg_markers(scripts)

    image = []
    if header_index:  # Checking for the header is sufficient here since no footer is returned is the header is missing.
        image = __extract_jpg(scripts, header_index, footer_index)

        file_name = file_name + '.jpg'

    util.write_binary_to_file(image, file_name)
