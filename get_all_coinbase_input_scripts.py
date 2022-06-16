import os
from chainexplorer import explorer as exp
from chainexplorer import util
from chainexplorer import apertus
import time


def get_all():
n = 0
part = 0
for block in range(741085):
    raw_block = exp.get_by_block(block)
    in_msg, _ = exp.collect_messages(raw_block)

    util.write_to_txt(f'{block},{in_msg[0]}', f'coinbase_input_scripts_part_{part}.txt')
    print(f'{block}    {in_msg[0]}')

    n += 1
    if n > 100000:
        part += 1

