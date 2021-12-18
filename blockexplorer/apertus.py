"""Block Explorer Apertus Module Documentation.

The Apertus module offers downloads and decodes data from the Bitcoin blockchain that was uploaded
via the AtomSea & EMBII tool.'


"""

import os
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

    return f"{file_name.strip('.')}.{file_extension}"


def __get_transaction_data(tx_hash: str, max_value: float = float('inf')) -> str:
    """Function to download all data from a AtomSea & EMBII upload.
    No interpretation of the data is performed only the collected out scripts are returned as a string.

    Args:
        tx_hash: root transaction hash
        max_value: Allows to set a threshold for the value of each transaction that will be included.
        Typically, scripts of interest are in transactions with low value.

    Returns:
        Concatenated out scripts of all transactions.

    """

    raw_tx = exp.get_transaction(tx_hash)

    out_scripts = exp.collect_out_scripts(raw_tx, max_value=max_value)
    out_scripts = ''.join(out_scripts)

    tx_list = __extract_transactions(out_scripts)

    scripts = exp.collect_multi_out_scripts(tx_list, max_value=max_value)

    return ''.join(scripts)


def __get_txt_data(file_name: str) -> str:
    """Function to read data from a txt file. The txt file is expected to contain concatenated out scripts.

    Args:
        file_name: String with the path to the .txt file.

    Returns:
        Content of the txt file

    """

    return util.read_from_txt(file_name)[0]


def __load_data(data_source: str, max_value: float = float('inf')) -> str:
    """Function to load transaction data either directly from https://www.blockchain.com/
    or from a .txt file. The data in the .txt file must contain the concatenated out scripts as a string.
    Ideally the data was retrieved by __get_transaction_data.

    Args:
        data_source: String which is either a transaction hash or the path to a .txt file
        max_value: Allows to set a threshold for the value of each transaction that will be included.

    Returns:
        All concatenated out scripts that belong to an AtomSea & EMBII dataset.

    """

    if util.is_transaction(data_source):
        data = __get_transaction_data(data_source, max_value)
    elif data_source.endswith('.txt'):
        data = __get_txt_data(data_source)
    else:
        raise ValueError('Input has to be a valid transaction hash or link to a data .txt file.')

    return data


def download_file(data_source: str, file_name: str, max_value: float = float('inf')) -> None:
    """Function to download and decode files that were uploaded via AtomSea & EMBII.
    The result will be written to file

    Args:
        data_source: root transaction hash or link to .txt file with data.
        file_name: filename under which the result will be saved. The correct extension will be added automatically.
        max_value: Allows to set a threshold for the value of each transaction that will be included.
        Typically, scripts of interest are in transactions with low value.

    """

    data = __load_data(data_source, max_value)

    markers = util.find_markers(data)

    n_file = 0
    for item in markers.items():

        if len(item[1][0]) != 0 and len(item[1][1]) != 0:

            start_of_file, end_of_file = util.match_markers(item[1])

            for i_file, file_start in enumerate(start_of_file):
                image = __extract_data(data, file_start, end_of_file[i_file])

                current_file_name = f'{file_name}_{n_file}'
                current_file_name = __add_extension(current_file_name, item[0])

                util.write_binary_to_file(image, current_file_name)

                n_file += 1


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

    scripts = __get_transaction_data(tx_hash, max_value)
    util.write_to_txt(scripts, file_name)


def download_from_file(txt_file: str = './data/atomsea.txt', max_value: float = float('inf')) -> list:
    """Function to download multiple root transactions and everything connected to them.
    The root transactions are provided through a .txt file which by default is the atomsea.txt file
    in the data subdirectory.

    The data will be saved in a directory called atomsea/<tx_hash>/rawdata.txt file
    If a file with the same name already exists the download will be skipped. Also, if a download fails
    the corresponding transaction hash will be returned.
    Therefore, the function can be called multiple times to retrieve all root transactions in case
    internet connection breaks without downloading already retrieved data twice.

    Args:
        txt_file: File name of the .txt file where the root transactions are defined.
        max_value: Allows to set a threshold for the value of each transaction that will be included.

    Returns:
        A list with all transactions that failed to download.

    """

    root_tx = util.read_from_txt(txt_file)

    failed = []
    for tx_hash in root_tx:
        data_folder = f'atomsea/{tx_hash}'
        util.create_folder(data_folder)

        file_name = f'{data_folder}/rawdata.txt'
        if not os.path.isfile(file_name):
            try:
                download_data(tx_hash, file_name, max_value=max_value)
            except RuntimeError:
                failed.append(tx_hash)

    return failed
