import requests
import codecs


def get_by_block(block):
    url = 'https://blockchain.info/block-height/'
    return requests.get(url + str(block) + "?format=json").json()['blocks'][0]
