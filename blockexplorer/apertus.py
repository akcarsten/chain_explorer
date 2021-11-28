import blockexplorer.explorer as exp
import blockexplorer.util as util

# TEXT DECODING NEEDS TO BE IMPLEMENTED


def __extract_transactions(out_scripts: str) -> list:

    binary_scripts = exp.decode_hex_message(out_scripts)[0]
    utf8_scripts = binary_scripts.decode('utf-8', errors='ignore')
    formatted_scripts = utf8_scripts.split('\r\n')
    formatted_scripts[0] = formatted_scripts[0][:64]

    return formatted_scripts[:-1]


def __extract_jpg(scripts: str, header_index: int, footer_index: int) -> bytes:
    image = scripts[header_index:footer_index + 4]  # add 4 bytes to include the complete footer (ffd9)

    return exp.decode_hex_message(image)[0]


def download_image(tx_hash: str, file_name, max_value=float('inf')) -> None:

    raw_tx = exp.get_transaction(tx_hash)

    out_scripts = exp.collect_out_scripts(raw_tx, max_value=max_value)
    out_scripts = ''.join(out_scripts)

    txs = __extract_transactions(out_scripts)

    scripts = exp.collect_multi_out_scripts(txs, max_value=max_value)
    scripts = ''.join(scripts)

    header_index, footer_index = util.find_jpg_markers(scripts)

    image = []
    if (header_index, footer_index) != []:
        image = __extract_jpg(scripts, header_index, footer_index)

        file_name = file_name + '.jpg'

    util.write_binary_to_file(image, file_name)
