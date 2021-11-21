import blockexplorer.explorer as exp
import time

# Example 1: Genesis block
# Encoded in the input message

# Download the Genesis block
raw_block = exp.get_by_block(0)

# Have a look at the Genesis information
exp.show_block_info(raw_block)

# The hidden information is in the input message
in_msg, out_msg = exp.collect_messages(raw_block)

# The input message needs to be decoded from hexadecimal to ASCII to be readable
decoded_msg = exp.decode_hex_message(in_msg)

print(decoded_msg)

# Example 2: Block 666666
# Encoded in the output message

raw_block = exp.get_by_block(666666)
in_msg, out_msg = exp.collect_messages(raw_block)
msg = exp.decode_hex_message(out_msg)
print([s for s in msg if 'not' in str(s)])

# Example 3: The Bitcoin white paper
exp.download_data('54e48e5f5c656b26c3bca14a8c95aa583d07ebe84dde3b7dd4a78f4e4186e713', 'bitcoin.pdf')

# Example 4: Satoshis Upload/Download Tool
# `In a cute touch, these transactions both donate 0.00000001 bitcoins to address 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa,
# which is Satoshi Nakamoto's address from the Genesis Block.`
# -- http://www.righto.com/2014/02/ascii-bernanke-wikileaks-photographs.html#ref13

# The Downloader
exp.download_data('6c53cd987119ef797d5adccd76241247988a0a5ef783572a9972e7371c5fb0cc', 'downloader.py')

# The Uploader
exp.download_data('4b72a223007eab8a951d43edc171befeabc7b5dca4213770c88e09ba5b936e17', 'uploader.py')

# Example 5: Nelson Mandela

# Part 1: The Wikipedia text
raw_tx = exp.get_transaction('8881a937a437ff6ce83be3a89d77ea88ee12315f37f7ef0dd3742c30eef92dba')

data = ''
for output in raw_tx['out']:
    if output['value'] == 5500:
        data = data + output['script'][6:46]

print('\nThis is text from the Wikipedia page about Nelson Mandela, encoded on the Bitcoin blockchain:\n')
print(exp.decode_hex_message(data)[0][8:-114].
      decode('utf8', errors="ignore"))


# Part 2: The image of Nelson Mandela

exp.show_transaction_info(raw_tx)
# The transaction was recorded in block #273536

raw_block = exp.get_by_block(273536) #318595

data = []
for tx in raw_block['tx']:
    for single_tx in tx['out']:
        if single_tx['value'] <= 5500:
            print(tx['hash'])
            data.append(single_tx['script'][6:-4])

jpg = ''.join(data)

header_index = jpg.find('ffd8')
footer_index = jpg.find('ffd9')

jpg = exp.decode_hex_message(jpg[header_index:footer_index + 4])[0] # add 4 bytes to include the complete footer (ffd9)

f = open('test1.jpg', "wb")
f.write(jpg)
f.close()



# Part 3: The Mandela speech
raw_block = exp.get_by_block(273522)

data = []
tx_index = []
for tx in raw_block['tx']:
    for single_tx in tx['out']:
        if single_tx['value'] == 5500:
            print(single_tx['script'])
            data.append(single_tx['script'][6:-4])
            tx_index.append(tx['hash'])
            
            
            
##### ALTERNATIVE

def collect_out_sripts(raw_tx):

    scripts = []
    for single_tx in raw_tx['out']:
        if single_tx['value'] <= 5500:
            scripts.append(single_tx['script'][6:-4])

    return scripts


def get_input_address(raw_tx):
    return raw_tx['inputs'][0]['prev_out']['addr']


def get_transactions(tx_hash):

    txs = []

    while tx_hash is not None:

        print(tx_hash)

        txs.append(tx_hash)

        raw_tx = exp.get_transaction(tx_hash)
        input_address = get_input_address(raw_tx)
        multi_address = exp.get_multi_address(input_address)

        if len(multi_address['txs']) == 2:
            for tx in multi_address['txs']:
                if tx['hash'] != raw_tx['hash']:
                    tx_hash = (tx['hash'])
                else:
                    tx_hash = None
        else:
            tx_hash = None

        time.sleep(2)

    return txs

#tx_hash = '78f0e6de0ce007f4dd4a09085e649d7e354f70bc7da06d697b167f353f115b8e'
tx_hash = '542de4ab1ac6917030e0dd5b3be584460a77ae6ed53ea3634b084c3750b4d05e'

txs = get_transactions(tx_hash)

data = []
for tx in txs[::-1]:
    print(tx)

    raw_tx = exp.get_transaction(tx)
    data = data + collect_out_sripts(raw_tx)

jpg = ''.join(data)

header_index = jpg.find('ffd8')
footer_index = jpg.find('ffd9', header_index)

jpg = exp.decode_hex_message(jpg[header_index:footer_index + 4])[0] # add 4 bytes to include the complete footer (ffd9)

f = open('test2.jpg', "wb")
f.write(jpg)
f.close()
