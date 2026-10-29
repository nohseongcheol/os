#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
ውሂብ_በቦታ_አስቀመጠ=argparse.ArgumentParser(description=__doc__);ውሂብ_በቦታ_አስቀመጠ.add_argument('file',type=Path);ውሂብ_በቦታ_አስቀመጠ.add_argument('--name',help='guest file name (e.g. package.Class.class)');ነጋሪ_እሴት_ድርድር=ውሂብ_በቦታ_አስቀመጠ.parse_args()
ውሂብ=ነጋሪ_እሴት_ድርድር.file.read_bytes();ስም=ነጋሪ_እሴት_ድርድር.name or ነጋሪ_እሴት_ድርድር.file.name
if len(ውሂብ)>16384 or not 1<=len(ስም.encode('utf-8'))<=63 or any(ord(የቁምፊ_ኮድ)<32 for የቁምፊ_ኮድ in ስም):ውሂብ_በቦታ_አስቀመጠ.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(ስም))
for 순번 in range(0,len(ውሂብ),64):print(ውሂብ[순번:순번+64].hex())
print('.')
