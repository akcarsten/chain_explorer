import pytest
import os
import shutil
import blockexplorer.util as util


jpg_strings = [
    ((20, 72, 'jpg'), 'sometextofnointerestffd8ffe000104a4649460001thisshouldnotbedetected0ffd9thisisalsonotrelevant'),
    ((11, 55, 'png'), 'howaboutpng89504e470dthisshould0notbedetected44ae426082thisisalsonotrelevant'),
    ((-1, -1, None), 'there_is_no_image_in_here'),
    ((13, -1, None), 'onlyTheHeaderffd8'),
    ((-1, -1, None), 'onlyTheFooterffd9'),
    ((0, 52, 'jpg'), 'ffd8ffe000104a4649460001MIXED89504e470JPGand0PNGffd9OHno44ae426082')
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

@pytest.mark.parametrize("expected, string", jpg_strings)
def test_find_file_markers(expected, string):

    assert expected == util.find_file_markers(string)


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