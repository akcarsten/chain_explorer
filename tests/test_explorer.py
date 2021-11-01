import pytest
import blockexplorer.explorer as exp

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

    block = exp.get_by_block(0)

    assert block[key] == value


@pytest.mark.parametrize("key, value", blockinfo)
def test_get_by_hash(key, value):

    block = exp.get_by_hash('000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f')

    assert block[key] == value


def test_collect_messages():

    block = exp.get_by_block(0)
    msgs = exp.collect_messages(block)

    assert msgs[0][0].find('d65732030332f4a616e2f323030') == 29
    assert msgs[1][0].find('130b7105cd6a828e03909a67962') == 29

