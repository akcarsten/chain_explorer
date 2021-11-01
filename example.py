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
