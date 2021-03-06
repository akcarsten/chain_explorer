# What is Chain Explore?

Chain explorer is an easy to use Python package that allows the exploration of the Bitcoin Blockchain. 
It retrieves data through the https://www.blockchain.com/explorer API. 
The focus of the functions is to decode data that was embedded in the blockchain.
Examples of such data are the famous message from Satoshi Nakamoto in the Bitcoin Genesis block.
The Bitcoin white paper. The Satoshi upload and download tool as code on the blockchain.
Or image data stored on the blockchain via the Apertus tool.

# How to install?

Install with pip:

```
pip install chainexplorer
```

Alternatively the package can be installed by cloning the repository as follows.

Clone the Git repository:

```
git clone https://github.com/akcarsten/chain_explorer
```

Then go to the folder to which you cloned the repository and run:

```
python setup.py install
```

# Some Examples

Below some examples are listed that show how the Chain Explorer package can be used to explore the secrets 
of the Bitcoin blockchain.

## Example 1: The secret message in the Genesis block

```Python
from chainexplorer import explorer as exp


# Download the Genesis block
raw_block = exp.get_by_block(0)

# Have a look at the Genesis information
exp.show_block_info(raw_block)

# The hidden information is in the input message
in_msg, out_msg = exp.collect_messages(raw_block)

# The input message needs to be decoded from hexadecimal to ASCII to be readable
decoded_msg = exp.decode_hex_message(in_msg)

print(decoded_msg)

b'\x04\xff\xff\x00\x1d\x01\x04EThe Times 03/Jan/2009 Chancellor on brink of second bailout for banks'

```

## Example 2: Download the Bitcoin white paper 

```Python
from chainexplorer import explorer as exp


# Get the Bitcoin white paper from the blockchain
exp.download_data('54e48e5f5c656b26c3bca14a8c95aa583d07ebe84dde3b7dd4a78f4e4186e713', 'bitcoin.pdf')
```