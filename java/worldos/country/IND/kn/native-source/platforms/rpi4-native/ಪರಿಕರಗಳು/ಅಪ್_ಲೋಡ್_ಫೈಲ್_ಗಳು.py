#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
ಡೇಟಾ_ಹುದ್ದೆ=argparse.ArgumentParser(description=__doc__);ಡೇಟಾ_ಹುದ್ದೆ.add_argument('file',type=Path);ಡೇಟಾ_ಹುದ್ದೆ.add_argument('--name',help='guest file name (e.g. package.Class.class)');ವಾದ_ಅರೇ=ಡೇಟಾ_ಹುದ್ದೆ.parse_args()
ಡೇಟಾ=ವಾದ_ಅರೇ.file.read_bytes();ಹೆಸರು=ವಾದ_ಅರೇ.name or ವಾದ_ಅರೇ.file.name
if len(ಡೇಟಾ)>16384 or not 1<=len(ಹೆಸರು.encode('utf-8'))<=63 or any(ord(ಅಕ್ಷರ_ಕೋಡ್)<32 for ಅಕ್ಷರ_ಕೋಡ್ in ಹೆಸರು):ಡೇಟಾ_ಹುದ್ದೆ.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(ಹೆಸರು))
for 순번 in range(0,len(ಡೇಟಾ),64):print(ಡೇಟಾ[순번:순번+64].hex())
print('.')
