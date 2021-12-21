"""Block Explorer Apertus Module Documentation.

The Apertus module offers downloads and decodes data from the Bitcoin blockchain that was uploaded
via the AtomSea & EMBII tool.'


"""

import os
import re
from typing import Union
from blockexplorer import explorer as exp
from blockexplorer import util

# TEXT DECODING NEEDS TO BE IMPLEMENTED
# SPEND ARGUMENT IN "exp.collect_out_scripts" NOT REACHABLE HERE
# -> RESTRUCTURE TO CLASS TO DEFINE "max_value" AND "spent" AS PROPERTIES


def __extract_transactions(out_scripts: str, decode: bool = True) -> list:
    """Function to extract transaction hashes from a string.
    The string is expected to come from the AtomSea & EMBII encoding.

    Args:
        out_scripts: Concatenated string of all output scripts in the root transaction either in Hex encoding or UTF-8.
        decode: Boolean to choose if input should first be converted to utf-8.

    Returns:
        List of all transactions belonging to the uploaded data set.

    """

    if not out_scripts:
        return []

    if decode:
        binary_scripts = exp.decode_hex_message(out_scripts)[0]
        utf8_scripts = binary_scripts.decode('utf-8', errors='ignore')
    else:
        utf8_scripts = out_scripts

    formatted_scripts = utf8_scripts.split('\r\n')
    formatted_scripts[0] = formatted_scripts[0][:64]

    if len(formatted_scripts) > 1:
        formatted_scripts = formatted_scripts[:-1]

    return formatted_scripts


def __extract_data(out_scripts: str, header_index: int, footer_index: int) -> bytes:
    """Function to extract the data from a hex string.
    The result is decoded to bytes and can be directly written to file

    Args:
        out_scripts: Hex string that contains data in form of a known file type (e.g. .jpg or .png)
        header_index: Start of the data
        footer_index: End of the data

    Returns:
        data in binary format.

    """

    image = out_scripts[header_index:footer_index]

    return exp.decode_hex_message(image)[0]


def __get_out_scripts(tx_hash: Union[list, str], max_value: float = float('inf')) -> str:
    """Function to collect all out scripts and concatenate them as a string.

    Args:
        tx_hash: root transaction hash
        max_value: Allows to set a threshold for the value of each transaction that will be included.

    Returns:
        All relevant transaction out scripts as one concatenated string.

    """

    out_scripts = exp.collect_multi_out_scripts(tx_hash, max_value=max_value)

    return ''.join(out_scripts)


def __append_transaction_list(out_scripts: str, tx_list: list,  max_value: float = float('inf')):
    """Function to add additional transaction data. This may be necessary if signed transactions refer to
    older non-signed uploads. In the current version the pattern 'SIG\\' is used to identify such a potential link.

    Args:
        out_scripts:
        tx_list:
        max_value: Allows to set a threshold for the value of each transaction that will be included.

    Returns:
        Original transaction list appended with additional transactions of relevance that were found.

    """

    decoded_scripts = exp.decode_hex_message(out_scripts)[0].decode('utf-8')
    if decoded_scripts.find('SIG\\') != -1:
        idx = decoded_scripts.find('LNK') + 28
        tx_hash = decoded_scripts[idx:idx + 64]
    elif decoded_scripts[64] == '>':
        end_point = decoded_scripts.find('<', 64)

        msg_length = decoded_scripts[65:end_point]
        num_digits = len(msg_length)
        msg_length = int(msg_length)

        idx = 66 + num_digits
        tx_hash = decoded_scripts[idx:idx + msg_length]
    else:
        tx_hash = []

    tx_hash = __extract_transactions(tx_hash, decode=False)
    out_scripts = __get_out_scripts(tx_hash, max_value)
    tx_list.extend(__extract_transactions(out_scripts))

    return tx_list


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

    out_scripts = __get_out_scripts(tx_hash, max_value)

    tx_list = __extract_transactions(out_scripts)
    tx_list = __append_transaction_list(out_scripts, tx_list,  max_value=max_value)

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
    elif isinstance(data_source, str):
        data = data_source
    else:
        raise ValueError('Input has to be a valid transaction hash or link to a data .txt file.')

    return data


def download_txt_message(data_source: str, file_name: str, max_value: float = float('inf')) -> None:
    """Function to decode and download text messages that were uploaded with Apertus.

    Args:
        data_source: root transaction hash or link to .txt file with data.
        file_name: filename under which the result will be saved. The correct extension will be added automatically.
        max_value: Allows to set a threshold for the value of each transaction that will be included.
        Typically, scripts of interest are in transactions with low value.

    Returns:

    """

    data = __load_data(data_source, max_value)
    decoded_data = exp.decode_hex_message(data)[0].decode('utf-8', errors='ignore')

    first_number = re.findall(r'\d+', decoded_data)[0]

    txt_start = decoded_data.find(first_number) + len(first_number)
    txt_message = decoded_data[txt_start:int(first_number) + 1]

    util.write_to_txt(txt_message, file_name)


def download_file(data_source: str, file_name: str, max_value: float = float('inf')) -> None:
    """Function to download and decode files that were uploaded via Apertus.
    The result will be written to file

    Args:
        data_source: root transaction hash or link to .txt file with data.
        file_name: filename under which the result will be saved. The correct extension will be added automatically.
        max_value: Allows to set a threshold for the value of each transaction that will be included.
        Typically, scripts of interest are in transactions with low value.

    """

    data = __load_data(data_source, max_value)

    download_txt_message(data, file_name, max_value=5500)

    markers = util.find_markers(data)

    n_file = 0
    for item in markers.items():

        if not item[1][0] and not item[1][1]:
            continue

        start_of_file, end_of_file = util.match_markers(item[1])

        if not end_of_file:
            continue

        for i_file, file_start in enumerate(start_of_file):

            # In case start marker has no corresponding end point
            if len(end_of_file) < i_file + 1:
                continue

            image = __extract_data(data, file_start, end_of_file[i_file])

            current_file_name = f'{file_name}_{n_file}'
            current_file_name = util.add_extension(current_file_name, item[0])

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
        file_name = util.add_extension(file_name, 'txt')

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
