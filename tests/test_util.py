import pytest
import blockexplorer.util as util


jpg_strings = [
    ((20, 72, 'jpg'), 'sometextofnointerestffd8ffe000104a4649460001thisshouldnotbedetected0ffd9thisisalsonotrelevant'),
    ((11, 55, 'png'), 'howaboutpng89504e470dthisshould0notbedetected44ae426082thisisalsonotrelevant'),
    ((-1, -1, None), 'there_is_no_image_in_here'),
    ((-1, -1, None), 'onlyTheHeaderffd8ffe000104a4649460001'),
    ((-1, -1, None), 'onlyTheFooterffd9'),
    ((0, 52, 'jpg'), 'ffd8ffe000104a4649460001MIXED89504e470JPGand0PNGffd9OHno44ae426082')
]


@pytest.mark.parametrize("expected, string", jpg_strings)
def test_find_file_markers(expected, string):

    assert expected == util.find_file_markers(string)
