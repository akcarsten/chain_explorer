import pytest
from unittest.mock import patch
import hashlib
import chainexplorer.explorer as exp


def test_get_latest_block():

    latest_block = exp.get_latest_block()

    assert list(latest_block.keys()).sort() == ['height', 'hash', 'time', 'block_index', 'txIndexes'].sort()


blockinfo = [
    ('hash', '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f'),
    ('ver', 1),
    ('prev_block', '0000000000000000000000000000000000000000000000000000000000000000'),
    ('mrkl_root', '4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b'),
    ('time', 1231006505),
    ('bits', 486604799),
    ('next_block', ['00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048']),
    ('fee', 0),
    ('nonce', 2083236893),
    ('n_tx', 1,),
    ('size', 285),
    ('block_index', 0),
    ('main_chain', True),
    ('height', 0),
    ('weight', 1140)]


@pytest.mark.parametrize("key, value", blockinfo)
def test_get_by_block(key, value):

    raw_block = exp.get_by_block(0)

    assert raw_block[key] == value


@pytest.mark.parametrize("key, value", blockinfo)
def test_get_by_hash(key, value):

    raw_block = exp.get_by_hash(blockinfo[0][1])

    assert raw_block[key] == value


transaction = [
    ('hash', '4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b'),
    ('ver', 1),
    ('vin_sz', 1),
    ('vout_sz', 1),
    ('size', 204),
    ('weight', 816),
    ('fee', 0),
    ('relayed_by', '0.0.0.0'),
    ('lock_time', 0),
    ('tx_index', 2098408272645986),
    ('double_spend', False),
    ('time', 1231006505),
    ('block_index', 0),
    ('block_height', 0)
]


@pytest.mark.parametrize("key, value", transaction)
def test_get_transaction(key, value):

    tx = exp.get_transaction(transaction[0][1])

    assert tx[key] == value


def test_get_single_address():

    multi_address = exp.get_multi_address('1QF3Dp1AMudu17xT6PopWupGKKhWgP1FSc')

    assert list(multi_address.keys()) == \
           ['addresses', 'wallet', 'txs', 'info', 'recommend_include_fee']

    assert multi_address['txs'][0]['hash'] == '78f0e6de0ce007f4dd4a09085e649d7e354f70bc7da06d697b167f353f115b8e'


def test_collect_messages():

    raw_block = exp.get_by_block(0)
    msgs = exp.collect_messages(raw_block)

    assert msgs[0][0].find('d65732030332f4a616e2f323030') == 29
    assert msgs[1][0].find('130b7105cd6a828e03909a67962') == 29


@patch('builtins.print')
def test_show_block_info(mock_print):

    raw_block = exp.get_by_block(0)
    exp.show_block_info(raw_block)

    mock_print.assert_called_with('weight: 1140')


@patch('builtins.print')
def test_show_transactions(mock_print):

    raw_block = exp.get_by_block(0)

    raw_block['tx'][0].pop('out')
    raw_block['tx'][0].pop('inputs')

    exp.show_transactions(raw_block)

    mock_print.assert_called_with('block_height: 0')


@patch('builtins.print')
def test_show_transaction_info(mock_print):

    raw_tx = exp.get_transaction('6c53cd987119ef797d5adccd76241247988a0a5ef783572a9972e7371c5fb0cc')
    exp.show_transaction_info(raw_tx)

    mock_print.assert_called_with('fee: 297401')


messages = [
    ('54686973206973206a75737420612074657374', [b'This is just a test']),
    (['5361746f736869', '4e616b616d6f746f'], [b'Satoshi', b'Nakamoto'])
]


@pytest.mark.parametrize("key, value", messages)
def test_decode_hex_message(key, value):

    assert exp.decode_hex_message(key) == value


def test_collect_uploaded_data():

    raw_tx = exp.get_transaction('6c53cd987119ef797d5adccd76241247988a0a5ef783572a9972e7371c5fb0cc')
    data = exp.collect_uploaded_data(raw_tx)

    assert data.endswith("f1888ac147922cbce6b2c1206c687f486ed7afa55e73ea01488ac")


def test_collect_out_scripts():

    raw_tx = {'out': [
        {'script': '76a9140a6137396432363833636631313261303931363588ac',
         'value': 5500,
         'spent': False},
        {'script': '76a914326664613738636638313431643532376435636388ac',
         'value': 1000,
         'spent': False},
        {'script': '76a914326664613738636638313431643532376435636388ac',
         'value': 1000,
         'spent': True},
        {'script': '76a914326664613738636638313431643532376435636388ac',
         'value': 8000,
         'spent': True}
    ]}

    actual = exp.collect_out_scripts(raw_tx)

    expected = [
        '0a61373964323638336366313132613039313635',
        '3266646137386366383134316435323764356363']

    assert expected == actual


def test_collect_multi_out_scripts():

    tx_list = [
        '8881a937a437ff6ce83be3a89d77ea88ee12315f37f7ef0dd3742c30eef92dba',
        '575061146335bd57f2dc132112152d0eeea44cf187ea6a52ac02435a7e5bea44',
    ]

    actual = exp.collect_multi_out_scripts(tx_list, max_value=5500)

    expected = [
        '223339365ce2809c5468657265206973206e6f74',
        '3ed509881f9851e5bc4dd778f6a955d193af3dc5'
    ]

    assert [actual[0], actual[-1]] == expected


def test_download_data(tmp_path):

    file_name = str(tmp_path) + '.pdf'
    tx_hash = '54e48e5f5c656b26c3bca14a8c95aa583d07ebe84dde3b7dd4a78f4e4186e713'

    exp.download_data(tx_hash, file_name=file_name)

    with open(file_name, 'rb') as pdf_file:
        data = pdf_file.read()

    actual = hashlib.sha256(data).digest()
    expected = b'\xb1gA\x91\xa8\x8e\xc5\xcd\xd73\xe4$\n\x81\x801\x05\xdcA-lg\x08\xd5:\xb9O\xc2H\xf4\xf5S'

    assert actual == expected


coinbase_messages = [
    (0, '\x04\x00\x1d\x01\x04EThe Times 03/Jan/2009 Chancellor on brink of second bailout for banks'),
    (130635, '\x07Eligius\x021\x0e')
]


@pytest.mark.parametrize("block_number, decoded_message", coinbase_messages)
def test_decode_coinbase_script(block_number, decoded_message):

    assert exp.decode_coinbase_script(130635) == '\x07Eligius\x021\x0e'