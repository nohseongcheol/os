#!/usr/bin/env python3
"""Print a checked guest hex-upload script, without starting or contacting a VM."""
import argparse,shlex
from pathlib import Path
مەلۇمات_ئورۇنلاشتۇرۇش=argparse.ArgumentParser(description=__doc__);مەلۇمات_ئورۇنلاشتۇرۇش.add_argument('file',type=Path);مەلۇمات_ئورۇنلاشتۇرۇش.add_argument('--name',help='guest file name (e.g. package.Class.class)');دەلىل_رەت=مەلۇمات_ئورۇنلاشتۇرۇش.parse_args()
مەلۇمات=دەلىل_رەت.file.read_bytes();ئاتى=دەلىل_رەت.name or دەلىل_رەت.file.name
if len(مەلۇمات)>16384 or not 1<=len(ئاتى.encode('utf-8'))<=63 or any(ord(ھەرپ_كودى)<32 for ھەرپ_كودى in ئاتى):مەلۇمات_ئورۇنلاشتۇرۇش.error('RAM file <=16384 bytes and UTF-8 name <=63 bytes required')
print('load '+shlex.quote(ئاتى))
for 순번 in range(0,len(مەلۇمات),64):print(مەلۇمات[순번:순번+64].hex())
print('.')
