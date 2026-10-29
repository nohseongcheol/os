#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
డేటా_స్థాయి=argparse.ArgumentParser(description=__doc__);డేటా_స్థాయి.add_argument('file',type=Path);డేటా_స్థాయి.add_argument('--name',help='guest file name (e.g. package.Class.class)');కారకం_శ్రేణి=డేటా_స్థాయి.parse_args()
డేటా=కారకం_శ్రేణి.file.read_bytes();పేరు=కారకం_శ్రేణి.name or కారకం_శ్రేణి.file.name
if len(డేటా)>16384 or not 1<=len(పేరు.encode('utf-8'))<=63 or any(ord(అక్షర_కోడ్)<32 for అక్షర_కోడ్ in పేరు):డేటా_స్థాయి.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(పేరు))
for 순번 in range(0,len(డేటా),64):print(డేటా[순번:순번+64].hex())
print('.')
