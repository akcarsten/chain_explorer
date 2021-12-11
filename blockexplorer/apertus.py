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


def __extract_data(scripts: str, header_index: int, footer_index: int) -> bytes:
    """Function to extract the data from a hex string.
    The result is decoded to bytes and can be directly written to file

    Args:
        scripts: Hex string that contains data in form of a known file type (e.g. .jpg or .png)
        header_index: Start of the data
        footer_index: End of the data

    Returns:
        data in binary format.

    """

    image = scripts[header_index:footer_index]

    return exp.decode_hex_message(image)[0]


def __add_extension(file_name: str, file_extension: str) -> str:
    """Function to add an extension to a file name

     Args:
         file_name: String with the target file name lacking the extension (e.g. .txt)

    Returns:
        File name with correct extension.

     """

    return f'{file_name}.{file_extension}'


def __get_data(tx_hash: str, max_value: float = float('inf')):
    """Function to download all data from a AtomSea & EMBII upload.
    No interpretation of the data is performed only the collected out scripts are returned as a string.

    Args:
        tx_hash: root transaction hash
        max_value: Allows to set a threshold for the value of each transaction that will be included.
        Typically scripts of interest are in transactions with low value.

    Returns:
        Concatenated out scripts of all transactions.

    """

    raw_tx = exp.get_transaction(tx_hash)

    out_scripts = exp.collect_out_scripts(raw_tx, max_value=max_value)
    out_scripts = ''.join(out_scripts)

    tx_list = __extract_transactions(out_scripts)

    scripts = exp.collect_multi_out_scripts(tx_list, max_value=max_value)

    return ''.join(scripts)


def download_image(tx_hash: str, file_name: str, max_value: float = float('inf')) -> None:
    """Function to download and decode image data that was uploaded via AtomSea & EMBII.
    The result will be written to file

    Args:
        tx_hash: root transaction hash
        file_name: filename under which the result will be saved. The correct extension will be added automatically.
        max_value: Allows to set a threshold for the value of each transaction that will be included.
        Typically scripts of interest are in transactions with low value.

    """

    scripts = __get_data(tx_hash, max_value)

    header_index, footer_index, file_type = util.find_file_markers(scripts)
    image = __extract_data(scripts, header_index, footer_index)

    file_name = __add_extension(file_name, file_type)

    util.write_binary_to_file(image, file_name)


def download_data(tx_hash: str, file_name: str, max_value: float = float('inf')) -> None:
    """Function to download raw data that was uploaded via AtomSea & EMBII.
    The result will be written to a .txt file

    Args:
        tx_hash: root transaction hash
        file_name: filename under which the result will be saved. The correct extension will be added automatically.
        max_value: Allows to set a threshold for the value of each transaction that will be included.
        Typically scripts of interest are in transactions with low value.

    """

    if not file_name.endswith('.txt'):
        file_name = __add_extension(file_name, 'txt')

    scripts = __get_data(tx_hash, max_value)
    util.write_to_txt(scripts, file_name)
