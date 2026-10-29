#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
자료위치=argparse.ArgumentParser(description=__doc__);자료위치.add_argument('file',type=Path);자료위치.add_argument('--name',help='guest file name (e.g. package.Class.class)');ሓባሪ_ቁጽሪ_ተርታ=자료위치.parse_args()
ሓበሬታ=ሓባሪ_ቁጽሪ_ተርታ.file.read_bytes();ሽም=ሓባሪ_ቁጽሪ_ተርታ.name or ሓባሪ_ቁጽሪ_ተርታ.file.name
if len(ሓበሬታ)>16384 or not 1<=len(ሽም.encode('utf-8'))<=63 or any(ord(ኮድ_ፊደል)<32 for ኮድ_ፊደል in ሽም):자료위치.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(ሽም))
for 순번 in range(0,len(ሓበሬታ),64):print(ሓበሬታ[순번:순번+64].hex())
print('.')
