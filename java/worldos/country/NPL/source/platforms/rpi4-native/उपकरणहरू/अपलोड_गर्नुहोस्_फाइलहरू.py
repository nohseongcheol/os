#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
लगत_राख्नुहोस्=argparse.ArgumentParser(description=__doc__);लगत_राख्नुहोस्.add_argument('file',type=Path);लगत_राख्नुहोस्.add_argument('--name',help='guest file name (e.g. package.Class.class)');तर्क_विन्यास=लगत_राख्नुहोस्.parse_args()
लगत=तर्क_विन्यास.file.read_bytes();नाम=तर्क_विन्यास.name or तर्क_विन्यास.file.name
if len(लगत)>16384 or not 1<=len(नाम.encode('utf-8'))<=63 or any(ord(वर्ण_सङ्केत)<32 for वर्ण_सङ्केत in नाम):लगत_राख्नुहोस्.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(नाम))
for 순번 in range(0,len(लगत),64):print(लगत[순번:순번+64].hex())
print('.')
