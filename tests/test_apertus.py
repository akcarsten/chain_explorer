import pytest
import blockexplorer.apertus as ap


def test_collect_transactions():
    # USE MOCK HERE TO AVOID REQUESTING DATA FROM THE API
    ap.collect_transactions(raw_tx)