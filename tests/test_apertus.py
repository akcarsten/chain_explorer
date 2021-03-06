import pytest
import os
import hashlib
from chainexplorer import apertus


tx_tests = [
    ('78f0e6de0ce007f4dd4a09085e649d7e354f70bc7da06d697b167f353f115b8e',
     b'\xa4r\x99\xedmCz\xd2@d+\x85\xae\xcd\xfdt\x02I\x9ef2\xa8f\xb3!\xdf\xf0\x1f\x1e\xde\x157',
     b"X\x88\x1bH\x1bS\xf2\xcf\xbf\x9b\xf4n\xc0 6\xaf\xf5%\xe0\x96*\xd4s'\xab\x93\xbe#X\xfe\xccZ")
]


def test_extract_transactions():

    out_scripts = \
        '3838383161393337613433376666366365383362653361383964373765613838656531323331356633376637656630646433373' \
        '43263333065656639326462617c3339362a38383831613933376134333766663663653833626533613839643737656138386565' \
        '3132333135663337663765663064643337343263333065656639326462610d0a353735303631313436333335626435376632646' \
        '331333231313231353264306565656134346366313837656136613532616330323433356137653562656134340d0a3637346337' \
        '6363333465613434626232373663366361663736663262323866613135393733383061623665366136393036303736643866373' \
        '2323963613562330d0a386532363432343136616432303932346234336635316136333366613163306135626138653461376236' \
        '333138373764623163363435343061343230383163390d0a6133303834303138303936623932616630346466353762363131366' \
        '53031666634623763376538626432323832333565643439653233663461323831373032390d0a33393334383732326238343161' \
        '6661306335623637653561663130383339616665393635656431623234383734653839333336626561396661346566333039310' \
        'd0a746f6d536561202620454d42494900'

    expected = ['8881a937a437ff6ce83be3a89d77ea88ee12315f37f7ef0dd3742c30eef92dba',
                '575061146335bd57f2dc132112152d0eeea44cf187ea6a52ac02435a7e5bea44',
                '674c7cc34ea44bb276c6caf76f2b28fa1597380ab6e6a6906076d8f7229ca5b3',
                '8e2642416ad20924b43f51a633fa1c0a5ba8e4a7b631877db1c64540a42081c9',
                'a3084018096b92af04df57b6116e01ff4b7c7e8bd228235ed49e23f4a2817029',
                '39348722b841afa0c5b67e5af10839afe965ed1b24874e89336bea9fa4ef3091']

    actual = apertus.__extract_transactions(out_scripts)

    assert actual == expected


def test_extract_data():

    scripts = '7719c16e0d44772edf98b73d0d004bf32800d479ecabc648f5a'
    header_index = 5
    footer_index = 15

    expected = b'\x16\xe0\xd4Gr'
    actual = apertus.__extract_data(scripts, header_index, footer_index)

    assert actual == expected


@pytest.mark.parametrize("tx_hash, expected_jpg, expected_txt", tx_tests)
@pytest.mark.skipif(os.name != 'nt', reason="only run on Windows")
def test_download_file(tmp_path, tx_hash, expected_jpg, expected_txt):

    file_name = str(tmp_path) + '/test_download'

    expected_results = [
        (f'{file_name}_0.jpg', expected_jpg),
        (f'{file_name}.txt', expected_txt)
         ]

    apertus.download_file(tx_hash, file_name=file_name, max_value=5500)

    for test_type in expected_results:

        with open(test_type[0], 'rb') as file:
            data = file.read()

        actual = hashlib.sha256(data).digest()

        assert actual == test_type[1]
