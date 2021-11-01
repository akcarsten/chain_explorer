import blockexplorer.explorer as exp

# Download the Genesis block
block = exp.get_by_block(0)

# Have a look at the Genesis information
exp.show_block_info(block)

# The hidden information is in the input message
in_msg, out_msg = exp.collect_messages(block)

# The input message needs to be decoded from hexadecimal to ASCII to be readable
decoded_msg = exp.decode_hex_message(in_msg)

print(decoded_msg)