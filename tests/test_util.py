import pytest
import blockexplorer.util as util


jpg_strings = [
    ((20, 47), 'sometextofnointerestffd8thisshouldnotbedetectedffd9thisisalsonotrelevant'),
    ((-1, -1), 'there_is_no_image_in_here'),
    ((13, -1), 'onlyTheHeaderffd8'),
    ((-1, -1), 'onlyTheFooterffd9')
]


@pytest.mark.parametrize("actual, string", jpg_strings)
def test_find_jpg_markers(actual, string):

    assert actual == util.find_jpg_markers(string)
