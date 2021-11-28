import blockexplorer.explorer as exp
import blockexplorer.util as util
import blockexplorer.apertus as apertus
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
util.write_binary_to_file(jpg, 'test1.jpg')


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
            

#tx_hash = '78f0e6de0ce007f4dd4a09085e649d7e354f70bc7da06d697b167f353f115b8e'  # Mandela
#tx_hash = '542de4ab1ac6917030e0dd5b3be584460a77ae6ed53ea3634b084c3750b4d05e'  # Mother Teresa
#tx_hash = 'd1bbc2f586d1de38edefe10337e2e99d1e8580d0be1a34f0f74315b12c131425'  # John Lennon NOT WORKING YET
#tx_hash = 'eec9d22292be2740050993d53673e1f969ebd8001669bb5498a59bef6a0a98cb' # PNG picture implement decoder
#tx_hash = 'f3b185bd932ef28cfd8e0d6891fa5af059a0446a1512e24461ddade4f1df0b53'  # Michael Jackson
#tx_hash = '151c05d420a3caa41ccc32bceeb75a2a3ab2b443cf55380fe17d442d024000b1'  # Random mother and son
#tx_hash = '73e5e9a23b7870c3942abf640655191c38e817793e8373d074dec62609ce843b'  # This is a gallery. Currently only the first image is decoded -> fix
#tx_hash = 'abf602893f5329ae27481b6966c636979f5714a1d63368747bb374f59f4e4b68' # Marylin Monroe
#tx_hash = '3c667e40667c496ff7c220b3abc3db391e8a3ebc158ead91f6b2d9a2b486c6b7'  # Isac Asimov
#tx_hash = '3e4d412944604e7b28f1bb521040968858aecc4518aef8359788205ef14e7d28'
#tx_hash = 'a1a859baf7682453409188ffd4f9b5956b39703eb94942afde02a3f4ab0b305b'  # Odd length error
#tx_hash = 'c53719cd196ea0f6c6bc77f828954d485854854a4b22ccb3d63692dacfa17b36' #
#tx_hash = '1bc87dbff1ff5831287f62ac7cf95579794e4386688479bab66174963f9a4a0c' # Spok text + audio + picture NOT WORKING
tx_hash = '56a8434f73486bc973673ec01502fa1ebdcaa0248ec3a572643520e63c0bdc57' # CO2 paper abstract and figure NOT WORKING

apertus.download_image(tx_hash, 'test', max_value=5500)
