#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
डेटा_स्थान=argparse.ArgumentParser(description=__doc__);डेटा_स्थान.add_argument('file',type=Path);डेटा_स्थान.add_argument('--name',help='guest file name (e.g. package.Class.class)');वितर्क_ऍरे=डेटा_स्थान.parse_args()
डेटा=वितर्क_ऍरे.file.read_bytes();नाव=वितर्क_ऍरे.name or वितर्क_ऍरे.file.name
if len(डेटा)>16384 or not 1<=len(नाव.encode('utf-8'))<=63 or any(ord(वर्ण_कोड)<32 for वर्ण_कोड in नाव):डेटा_स्थान.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(नाव))
for क्रमांक_अनुक्रमणिका in range(0,len(डेटा),64):print(डेटा[क्रमांक_अनुक्रमणिका:क्रमांक_अनुक्रमणिका+64].hex())
print('.')
