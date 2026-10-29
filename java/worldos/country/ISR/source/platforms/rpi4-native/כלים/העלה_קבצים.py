#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
נתונים_עמדה=argparse.ArgumentParser(description=__doc__);נתונים_עמדה.add_argument('file',type=Path);נתונים_עמדה.add_argument('--name',help='guest file name (e.g. package.Class.class)');ארגומנט_מערך=נתונים_עמדה.parse_args()
נתונים=ארגומנט_מערך.file.read_bytes();שם=ארגומנט_מערך.name or ארגומנט_מערך.file.name
if len(נתונים)>16384 or not 1<=len(שם.encode('utf-8'))<=63 or any(ord(נקודת_קוד)<32 for נקודת_קוד in שם):נתונים_עמדה.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(שם))
for 순번 in range(0,len(נתונים),64):print(נתונים[순번:순번+64].hex())
print('.')
