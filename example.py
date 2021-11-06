import blockexplorer.explorer as exp
import codecs

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
raw_tx = exp.get_transaction('54e48e5f5c656b26c3bca14a8c95aa583d07ebe84dde3b7dd4a78f4e4186e713')

pdf = ''
n = 0
for output in raw_tx['out']:
    if n < 948:
        cur = 4
        pdf = pdf + output['script'][cur:cur + 130]
        cur += 132
        pdf = pdf + output['script'][cur:cur + 130]
        cur += 132
        pdf = pdf + output['script'][cur:cur + 130]
    n +=1

f = open("bitcoin.pdf", "wb")
f.write(codecs.decode(pdf[16:-112], 'hex'))
f.close()
