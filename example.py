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

# The Downloader
exp.download_data('6c53cd987119ef797d5adccd76241247988a0a5ef783572a9972e7371c5fb0cc', 'downloader.py')

# The Uploader
exp.download_data('4b72a223007eab8a951d43edc171befeabc7b5dca4213770c88e09ba5b936e17', 'uploader.py')
