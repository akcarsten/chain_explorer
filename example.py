import blockexplorer.explorer as exp

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

# Now let's dig a little deeper.
# The input to the above transaction was an output of an previous transaction ID: 6550612141802894
# We can see that as follows:

prev_out_tx_id = raw_tx['inputs'][0]['prev_out']['spending_outpoints'][0]['tx_index']

# So let's load this transaction

raw_block = exp.get_by_block(raw_tx['block_index'])

for tx in raw_block['tx']:
    if tx['inputs'][0]['prev_out'] is not None:
        if tx['inputs'][0]['prev_out']['tx_index'] == prev_out_tx_id:
            print('found it')
            print(tx['hash'])


raw_tx = exp.get_transaction('78f0e6de0ce007f4dd4a09085e649d7e354f70bc7da06d697b167f353f115b8e')

for o in raw_tx['out']:
   print(o)

test = exp.get_by_block(273536)

for t in test['tx']:

    if t['hash'] == '8881a937a437ff6ce83be3a89d77ea88ee12315f37f7ef0dd3742c30eef92dba':
        print(t['hash'])
        print(t['tx_index'])

    if t['inputs'][0]['prev_out'] is not None:
        if t['inputs'][0]['prev_out']['tx_index'] == 6550612141802894:
             print(t['hash'])
             print(t['tx_index'])


test['tx'][0]['hash']