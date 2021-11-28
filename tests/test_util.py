import pytest
import blockexplorer.util as util


jpg_strings = [
    ((20, 51, 'jpg'), 'sometextofnointerestffd8thisshouldnotbedetectedffd9thisisalsonotrelevant'),
    ((11, 54, 'png'), 'howaboutpng89504e470dthisshouldnotbedetected44ae426082thisisalsonotrelevant'),
    ((-1, -1, None), 'there_is_no_image_in_here'),
    ((-1, -1, None), 'onlyTheHeaderffd8'),
    ((-1, -1, None), 'onlyTheFooterffd9')
]


@pytest.mark.parametrize("actual, string", jpg_strings)
def test_find_file_markers(actual, string):

    assert actual == util.find_file_markers(string)
