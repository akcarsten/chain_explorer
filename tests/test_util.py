import pytest
import os
import blockexplorer.util as util


jpg_strings_new = [
    ({'png': [[], []], 'jpg': [[20], [72]], 'gif': [[], []], 'zip': [[], []]},
     'sometextofnointerestffd8ffe000104a4649460001thisshouldnotbedetected0ffd9thisisalsonotrelevant'),

    ({'png': [[11], [55]], 'jpg': [[], []], 'gif': [[], []], 'zip': [[], []]},
     'howaboutpng89504e470dthisshould0notbedetected44ae426082thisisalsonotrelevant'),

    ({'png': [[], []], 'jpg': [[], []], 'gif': [[], []], 'zip': [[], []]},
     'there_is_no_image_in_here'),

    ({'png': [[], []], 'jpg': [[13], []], 'gif': [[], []], 'zip': [[], []]},
     'onlyTheHeaderffd8'),

    ({'png': [[], []], 'jpg': [[], [17]], 'gif': [[], []], 'zip': [[], []]},
     'onlyTheFooterffd9'),

    ({'png': [[], [66]], 'jpg': [[0], [52]], 'gif': [[], []], 'zip': [[], []]},
     'ffd8ffe000104a4649460001MIXED89504e470JPGand0PNGffd9OHno44ae426082')
]

test_folders = [
    'test_folder',
    'test_folder/subfolder',
    'test_folder\\subfolder'
]

test_markers = [
    (([1], [3]), [[1], [3]]),
    (([1, 4], [3, 8]), [[1, 4], [3, 8]]),
    (([1, 4, 9], [3, 8, 21]), [[1, 4, 9], [3, 8, 21]]),
    (([9], [21]), [[9], [3, 8, 21]]),
]


@pytest.mark.parametrize("expected, string", jpg_strings_new)
def test_find_markers(expected, string):

    assert expected == util.find_markers(string)


@pytest.mark.parametrize("expected, markers", test_markers)
def test_match_markers(expected, markers):

    assert expected == util.match_markers(markers)


@pytest.mark.parametrize("test_structure", test_folders)
def test_create_folders(test_structure, tmp_path):

    directory = f'{tmp_path}/{test_structure}'
    util.create_folder(directory)

    assert os.path.isdir(directory)


def test_write_to_txt():
    
    with pytest.raises(AssertionError):
        util.write_to_txt(['Oh no a list!'], 'this_will_not_be_written.txt')