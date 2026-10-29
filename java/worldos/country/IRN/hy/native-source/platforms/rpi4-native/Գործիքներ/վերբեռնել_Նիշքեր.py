#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
տվյալ_դիրք=argparse.ArgumentParser(description=__doc__);տվյալ_դիրք.add_argument('file',type=Path);տվյալ_դիրք.add_argument('--name',help='guest file name (e.g. package.Class.class)');արգումենտ_ԶԱՆԳՎԱԾ=տվյալ_դիրք.parse_args()
տվյալ=արգումենտ_ԶԱՆԳՎԱԾ.file.read_bytes();Անուն=արգումենտ_ԶԱՆԳՎԱԾ.name or արգումենտ_ԶԱՆԳՎԱԾ.file.name
if len(տվյալ)>16384 or not 1<=len(Անուն.encode('utf-8'))<=63 or any(ord(գրանշանի_կոդ)<32 for գրանշանի_կոդ in Անուն):տվյալ_դիրք.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(Անուն))
for 순번 in range(0,len(տվյալ),64):print(տվյալ[순번:순번+64].hex())
print('.')
