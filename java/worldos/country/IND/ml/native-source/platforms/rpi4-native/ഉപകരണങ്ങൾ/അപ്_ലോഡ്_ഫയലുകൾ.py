#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
ഡാറ്റാ_പദവി=argparse.ArgumentParser(description=__doc__);ഡാറ്റാ_പദവി.add_argument('file',type=Path);ഡാറ്റാ_പദവി.add_argument('--name',help='guest file name (e.g. package.Class.class)');ആര്_ഗ്യുമെന്_റ്_അരേ=ഡാറ്റാ_പദവി.parse_args()
ഡാറ്റാ=ആര്_ഗ്യുമെന്_റ്_അരേ.file.read_bytes();പേരു്=ആര്_ഗ്യുമെന്_റ്_അരേ.name or ആര്_ഗ്യുമെന്_റ്_അരേ.file.name
if len(ഡാറ്റാ)>16384 or not 1<=len(പേരു്.encode('utf-8'))<=63 or any(ord(പ്രതീകകോഡ്)<32 for പ്രതീകകോഡ് in പേരു്):ഡാറ്റാ_പദവി.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(പേരു്))
for 순번 in range(0,len(ഡാറ്റാ),64):print(ഡാറ്റാ[순번:순번+64].hex())
print('.')
