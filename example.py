import os
from chainexplorer import explorer as exp
from chainexplorer import util
from chainexplorer import apertus
import time


'''
It took around six months until version 2 blocks were the standard, with the last version 1 block at height 227,835 timestamped at 2013–03–24 15:49:13 GMT.
https://medium.com/fcats-blockchain-incubator/understanding-the-bitcoin-blockchain-header-a2b0db06b515


Provide an example of timestamp to determine the block time
'''

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

'''
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

raw_block = exp.get_by_block(273536)

data = []
for tx in raw_block['tx']:
    for single_tx in tx['out']:
        if single_tx['value'] <= 5500:
            print(tx['hash'])
            data.append(single_tx['script'][6:-4])

jpg = ''.join(data)

header_index = jpg.find('ffd8')
footer_index = jpg.find('ffd9')

jpg = exp.decode_hex_message(jpg[header_index:footer_index + 4])[0]  # add 4 bytes to include the complete footer (ffd9)
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
'''

# Working
# tx_hash = '78f0e6de0ce007f4dd4a09085e649d7e354f70bc7da06d697b167f353f115b8e'  # Mandela
# tx_hash = '542de4ab1ac6917030e0dd5b3be584460a77ae6ed53ea3634b084c3750b4d05e'  # Mother Teresa
# tx_hash = 'd1bbc2f586d1de38edefe10337e2e99d1e8580d0be1a34f0f74315b12c131425'  # John Lennon
# tx_hash = 'eec9d22292be2740050993d53673e1f969ebd8001669bb5498a59bef6a0a98cb'  # PNG picture
# tx_hash = 'f3b185bd932ef28cfd8e0d6891fa5af059a0446a1512e24461ddade4f1df0b53'  # Michael Jackson
# tx_hash = '151c05d420a3caa41ccc32bceeb75a2a3ab2b443cf55380fe17d442d024000b1'  # Random mother and son
# tx_hash = '73e5e9a23b7870c3942abf640655191c38e817793e8373d074dec62609ce843b'  # Picture gallery
# tx_hash = '366bfe5b135ffc52894f67f53936ec2ec693cad61c64e52f1624ef22815d4de7'  # Gallery this time signed
# tx_hash = 'abf602893f5329ae27481b6966c636979f5714a1d63368747bb374f59f4e4b68'  # Marylin Monroe ---
# tx_hash = '3c667e40667c496ff7c220b3abc3db391e8a3ebc158ead91f6b2d9a2b486c6b7'  # Isac Asimov
# tx_hash = '3e4d412944604e7b28f1bb521040968858aecc4518aef8359788205ef14e7d28'  # random image
# tx_hash = 'c53719cd196ea0f6c6bc77f828954d485854854a4b22ccb3d63692dacfa17b36'  # random image
# tx_hash = '460ed23bea89176cdfe18e13fce51ad5386ad8e3e1f7d6f5b4711b3be97b0502'  # Homeless person
# tx_hash = '50d12347e7c33949b93ed7ad0e703f1adb45923352e8ef8e317f33a59b062227'  # Wedding picture
# tx_hash = 'fde8a8309c993a54a6bf83a3492f028f75013aacc37c0d35e647354f152c3786'  # Ownership transfer across chains
# tx_hash = '2c4b9497af8c0c0eb9383357b40c3de33dba0b4f481099a32719f2b9036da8e7'  # Bike Lady
# tx_hash = '6d606e3cf568c98d603a5d8a4664eb777318522575caf8af489171f88167d202'  # Johnny Cash
# tx_hash = '1bc87dbff1ff5831287f62ac7cf95579794e4386688479bab66174963f9a4a0c'  # Spok text + audio + picture works but file detection should be improved
# tx_hash = 'a1a859baf7682453409188ffd4f9b5956b39703eb94942afde02a3f4ab0b305b'  # Margaret Hamilton
# tx_hash = '54d73e61c13b9b2cad3cb65fd92e1b6e047380c2df1874d42d067a58c296ab3d'  # Pope, lots of data HTML
# tx_hash = 'd305192d5c4312fb3e6434bf08fb598749abee14281c859af7019aa43bb91e48' #
# tx_hash = 'bcc522a4ef06fc713c7a78bf90fe7d941433364b1b4efb15d1b7128fdd1f5c38'  # Random person
# tx_hash = 'c0fc3eb9e7b6c4f969e946a4b488fc8fea77d8bc8c61996fcccd48cd7e8de36a'  # Picture gallery
# tx_hash = '4cbb32cd27b5b5edc12d3559bdffc1355ac2a210463d5cfaadc7ce9b06675b2b' #
# tx_hash = '474b81dcdf6c85e762092799e2a96886f2165e825d17e7eca58f210c2a572ce2'  # Picture gallery

# Not working
# tx_hash = '88144af29540aa788a9cb156ed461d57be82d97540d3255433a9defb4c26eb1e'  # CO2 paper and figure PICTURE OK BUT TEXT MISSING
# tx_hash = '56a8434f73486bc973673ec01502fa1ebdcaa0248ec3a572643520e63c0bdc57'  # CO2 paper and figure
# tx_hash = '118afd4a84d3f8588d5333fbe78d4e2b986c93453c0a4bcf1bca01e9e45eed66'
# tx_hash = '4c7d8f6e7082a30d2d2d07c47ab462ea389415f4b95559106ff5f83f2bca8c82'
# tx_hash = '5273f09867c347c798db7f9df9fbcc724520288662e9efe54db47cdd12eb908e'  # lots of data
# tx_hash = '8f76545181e2e9c29b6e810a46d607bcf4cec9cb0452fb912887f9abc2f0b5df'  # lots of data
# tx_hash = 'c29ad9a43149d29ce8a8f92b68ce38d01cb556acd812ed4f427c52693b617c34'
# tx_hash = '0601220d73a077587a60ddca7cbd4a77166a47a7e2191a437d442872cc354dad'  # lots of data
# tx_hash = 'a467eb78c5d5c5d3ce0e6dc5ad3b2532dd8b4e916ad762897d43c71ba868308c'  # lots of data
# tx_hash = 'a467eb78c5d5c5d3ce0e6dc5ad3b2532dd8b4e916ad762897d43c71ba868308c'  # lots of data


# apertus.download_file(tx_hash, 'test',  max_value=5500)
