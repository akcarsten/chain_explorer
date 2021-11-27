import pytest
from unittest.mock import patch
import blockexplorer.util as util


def test_find_jpg_markers():

    test_string = 'sometextofnointerestffd8thisshouldnotbedetectedffd9thisisalsonotrelevant'

    assert (20, 47) == util.find_jpg_markers(test_string)
