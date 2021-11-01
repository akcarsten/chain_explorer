# -*- coding: utf-8 -*-
"""Block Explorer Module Documentation.

Block Explorer offers functions to retrieve information about blocks on the Bitcoin Blockchain via 'blockchain.info'


"""

import requests
import codecs


def get_by_block(block: int) -> dict:
    """Function to retrieve all data from a specified block of the Bitcoin blockchain y providing the block number.

    Args:
        block: block number of interest

    Returns:
        Dictionary with the block data

    """

    url = 'https://blockchain.info/block-height/'

    return requests.get(url + str(block) + "?format=json").json()['blocks'][0]


def get_by_hash(block_hash: str) -> dict:
    """Function to retrieve all data from a specified block of the Bitcoin blockchain by providing the block hash.

    Args:
        block_hash: block hash of interest

    Returns:
        Dictionary with the block data

    """

    url = 'https://blockchain.info/rawblock/'

    return requests.get(url + block_hash).json()