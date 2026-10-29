#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
positionDonnées=argparse.ArgumentParser(description=__doc__);positionDonnées.add_argument('file',type=Path);positionDonnées.add_argument('--name',help='guest file name (e.g. package.Class.class)');tableauArgument=positionDonnées.parse_args()
Données=tableauArgument.file.read_bytes();nom=tableauArgument.name or tableauArgument.file.name
if len(Données)>16384 or not 1<=len(nom.encode('utf-8'))<=63 or any(ord(codeCaractère)<32 for codeCaractère in nom):positionDonnées.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(nom))
for indiceOrdinal in range(0,len(Données),64):print(Données[indiceOrdinal:indiceOrdinal+64].hex())
print('.')
