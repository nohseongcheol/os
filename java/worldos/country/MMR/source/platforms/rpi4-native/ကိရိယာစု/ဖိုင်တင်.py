#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
ဒေတာနေရာ=argparse.ArgumentParser(description=__doc__);ဒေတာနေရာ.add_argument('file',type=Path);ဒေတာနေရာ.add_argument('--name',help='guest file name (e.g. package.Class.class)');ပေးအချက်အခင်းအကျင်း=ဒေတာနေရာ.parse_args()
ဒေတာ=ပေးအချက်အခင်းအကျင်း.file.read_bytes();အမည်=ပေးအချက်အခင်းအကျင်း.name or ပေးအချက်အခင်းအကျင်း.file.name
if len(ဒေတာ)>16384 or not 1<=len(အမည်.encode('utf-8'))<=63 or any(ord(အက္ခရာကုဒ်)<32 for အက္ခရာကုဒ် in အမည်):ဒေတာနေရာ.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(အမည်))
for အစဉ်အမှတ် in range(0,len(ဒေတာ),64):print(ဒေတာ[အစဉ်အမှတ်:အစဉ်အမှတ်+64].hex())
print('.')
