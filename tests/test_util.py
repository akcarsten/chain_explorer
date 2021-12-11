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

'''
@pytest.fixture(scope="function")
def delete_folders():
    os.system('rmdir /S /Q "test_folder"')
'''

@pytest.mark.parametrize("expected, string", jpg_strings)
def test_find_file_markers(expected, string):

    assert expected == util.find_file_markers(string)


@pytest.mark.parametrize("test_structure", test_folders)
def test_create_folders(test_structure, tmp_path):

    directory = f'{tmp_path}/{test_structure}'
    util.create_folder(directory)

    assert os.path.isdir(directory)
