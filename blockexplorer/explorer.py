# -*- coding: utf-8 -*-
"""Block Explorer Module Documentation.

Block Explorer offers functions to retrieve information about blocks on the Bitcoin Blockchain via 'blockchain.info'


"""

import requests
from typing import Tuple
from typing import Union


def get_by_block(block: int) -> dict:
    """Function to retrieve all data from a specified block of the Bitcoin blockchain y providing the block number.

    Args:
        block: block number of interest

    Returns:
        dict: block data

    """

    url = 'https://blockchain.info/block-height/'

    return requests.get(url + str(block) + "?format=json").json()['blocks'][0]


def get_by_hash(block_hash: str) -> dict:
    """Function to retrieve all data from a specified block of the Bitcoin blockchain by providing the block hash.

    Args:
        block_hash: block hash of interest

    Returns:
        dict: block data

    """

    url = 'https://blockchain.info/rawblock/'

    return requests.get(url + block_hash).json()


def collect_messages(raw_block: dict) -> Tuple[list, list]:
    """Function to collect all input and output messages into two lists.

    Args:
        raw_block: Block information as dictionary retrieved by either 'get_by_block' or 'get_by_hash'

    Returns:
        tuple: with the input and output messages as lists

    """

    input_msg = []
    output_msg = []
    for i in raw_block['tx']:
        for output in i['out']:
            output_msg.append(output['script'])

        for inputs in i['inputs']:
            input_msg.append(inputs['script'])

    return input_msg, output_msg


def decode_hex_message(msg: Union[str, list]) -> list:
    """Function to decode hexadecimal messages to ASCII code.

    Args:
        msg: hexadecimal message either as a string or a list of strings.

    Returns:
        list: decoded hexadecimal input messages

    Examples:
        >>> decode_hex_message('5361746f736869')
        ['Satoshi']

    """

    if type(msg) == str:
        msg = [msg]

    decoded_msg = []
    for message in msg:
        decoded_msg.append(bytes.fromhex(message).decode('utf-8', errors='ignore'))

    return decoded_msg
