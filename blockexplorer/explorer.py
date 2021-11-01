import requests
import codecs


def get_by_block(block):
    url = 'https://blockchain.info/block-height/'

    return requests.get(url + str(block) + "?format=json").json()['blocks'][0]


def get_by_hash(block_hash):
    url = 'https://blockchain.info/rawblock/'

    return requests.get(url + block_hash).json()