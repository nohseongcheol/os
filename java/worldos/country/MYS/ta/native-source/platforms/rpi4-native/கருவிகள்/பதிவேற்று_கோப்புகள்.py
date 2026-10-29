#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
தரவு_நிலை=argparse.ArgumentParser(description=__doc__);தரவு_நிலை.add_argument('file',type=Path);தரவு_நிலை.add_argument('--name',help='guest file name (e.g. package.Class.class)');மதிப்புரு_கோவை=தரவு_நிலை.parse_args()
தரவு=மதிப்புரு_கோவை.file.read_bytes();பெயர்=மதிப்புரு_கோவை.name or மதிப்புரு_கோவை.file.name
if len(தரவு)>16384 or not 1<=len(பெயர்.encode('utf-8'))<=63 or any(ord(எழுத்துக்குறி_குறியீடு)<32 for எழுத்துக்குறி_குறியீடு in பெயர்):தரவு_நிலை.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(பெயர்))
for 순번 in range(0,len(தரவு),64):print(தரவு[순번:순번+64].hex())
print('.')
