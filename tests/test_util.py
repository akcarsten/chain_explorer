import pytest
import os
import blockexplorer.util as util


jpg_strings_new = [
    ({'png': [[], []], 'jpg': [[20], [72]], 'gif': [[], []], 'zip': [[], []], 'mp3': [[], []]},
     'sometextofnointerestffd8ffe000104a4649460001thisshouldnotbedetected0ffd9thisisalsonotrelevant'),

    ({'png': [[11], [55]], 'jpg': [[], []], 'gif': [[], []], 'zip': [[], []], 'mp3': [[], []]},
     'howaboutpng89504e470dthisshould0notbedetected44ae426082thisisalsonotrelevant'),

    ({'png': [[], []], 'jpg': [[], []], 'gif': [[], []], 'zip': [[], []], 'mp3': [[], []]},
     'there_is_no_image_in_here'),

    ({'png': [[], []], 'jpg': [[13], []], 'gif': [[], []], 'zip': [[], []], 'mp3': [[], []]},
     'onlyTheHeaderffd8'),

    ({'png': [[], []], 'jpg': [[], [17]], 'gif': [[], []], 'zip': [[], []], 'mp3': [[], []]},
     'onlyTheFooterffd9'),

    ({'png': [[], [66]], 'jpg': [[0], [52]], 'gif': [[], []], 'zip': [[], []], 'mp3': [[], []]},
     'ffd8ffe000104a4649460001MIXED89504e470JPGand0PNGffd9OHno44ae426082'),

    ({'png': [[], []], 'jpg': [[], []], 'gif': [[], []], 'zip': [[], []], 'mp3': [[14, 43], [20, 49]]},
     'justNumbersAnd494433toMarkAnMp3HereIsTheEnd494433orNot')
]

test_folders = [
    'test_folder',
    'test_folder/subfolder',
    'test_folder\\subfolder'
]

test_markers = [
    (([1], [3]), [[1], [3]]),
    (([1, 4], [3, 8]), [[1, 4], [3, 8]]),
    (([1, 1, 4, 9], [3, 21, 8, 21]), [[1, 4, 9], [3, 8, 21]]),
    (([9], [21]), [[9], [3, 8, 21]]),
]


@pytest.mark.parametrize("expected, string", jpg_strings_new)
def test_find_markers(expected, string):

    assert util.find_markers(string) == expected


@pytest.mark.parametrize("expected, markers", test_markers)
def test_match_markers(expected, markers):

    assert util.match_markers(markers) == expected


@pytest.mark.parametrize("test_structure", test_folders)
def test_create_folders(test_structure, tmp_path):

    directory = f'{tmp_path}/{test_structure}'
    util.create_folder(directory)

    assert os.path.isdir(directory)


def test_write_to_txt():
    
    with pytest.raises(AssertionError):
        util.write_to_txt(['Oh no a list!'], 'this_will_not_be_written.txt')


@pytest.mark.parametrize("expected, string",
                         [(False, 'notAtransaction'),
                          (True, '78f0e6de0ce007f4dd4a09085e649d7e354f70bc7da06d697b167f353f115b8e')])
def test_is_transaction(expected, string):

    assert util.is_transaction(string) is expected


@pytest.mark.parametrize("expected, base, extension",
                         [('no_extension_here.txt', 'no_extension_here', 'txt'),
                          ('no_extension_here.txt', 'no_extension_here.', 'txt')])
def test_add_extension(expected, base, extension):

    assert util.add_extension(base, extension) == expected


@pytest.mark.parametrize("expected, test_string",
                         [(True, '89ABCDEFGHJKLMNPQ12345'),
                          (False, 'not base58 sorry.')])
def test_is_base58(expected, test_string):

    assert util.is_base58(test_string) == expected


@pytest.mark.parametrize("expected, test_string",
                         [(True, '89ABCDEFab'),
                          (False, 'not SHA256 sorry.')])
def test_is_sha256(expected, test_string):

    assert util.is_sha256(test_string) == expected

