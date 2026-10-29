#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
डेटा_पद=argparse.ArgumentParser(description=__doc__);डेटा_पद.add_argument('file',type=Path);डेटा_पद.add_argument('--name',help='guest file name (e.g. package.Class.class)');तर्क_सरणी=डेटा_पद.parse_args()
आँकड़े=तर्क_सरणी.file.read_bytes();नाम=तर्क_सरणी.name or तर्क_सरणी.file.name
if len(आँकड़े)>16384 or not 1<=len(नाम.encode('utf-8'))<=63 or any(ord(वर्ण_कोड)<32 for वर्ण_कोड in नाम):डेटा_पद.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(नाम))
for 순번 in range(0,len(आँकड़े),64):print(आँकड़े[순번:순번+64].hex())
print('.')
