#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ=argparse.ArgumentParser(description=__doc__);ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.add_argument('file',type=Path);ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.add_argument('--name',help='guest file name (e.g. package.Class.class)');ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ=ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.parse_args()
ਸਮੱਗਰੀ=ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.file.read_bytes();ਨਾਂ=ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.name or ਦਲੀਲ_ਤਰਤੀਬ_ਦੇਣਾ.file.name
if len(ਸਮੱਗਰੀ)>16384 or not 1<=len(ਨਾਂ.encode('utf-8'))<=63 or any(ord(ਵਰਣ_ਕੋਡ)<32 for ਵਰਣ_ਕੋਡ in ਨਾਂ):ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(ਨਾਂ))
for 순번 in range(0,len(ਸਮੱਗਰੀ),64):print(ਸਮੱਗਰੀ[순번:순번+64].hex())
print('.')
