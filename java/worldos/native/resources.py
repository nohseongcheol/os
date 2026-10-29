#!/usr/bin/env python3
"""Freeze fonts, real keyboard layouts, and a relocatable host QEMU bundle."""
import ctypes as C
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
from PIL import Image, ImageDraw, ImageFont
from archives import archive_writer
from paths import jkoros_root

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'native/resources'
ALPINE = ROOT / 'build/rootfs'
HOST = jkoros_root() / 'platforms/rpi4/build/host'


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def bundle_qemu():
    loader = HOST / 'lib/ld-musl-x86_64.so.1'
    binary = HOST / 'usr/bin/qemu-system-aarch64'
    listing = subprocess.check_output([str(loader), '--library-path', str(HOST/'usr/lib')+':'+str(HOST/'lib'), '--list', str(binary)], universal_newlines=True)
    files = {'lib/ld-musl-x86_64.so.1': loader, 'qemu-system-aarch64': binary}
    for path in re.findall(r'=> (\S+)', listing):
        if path.startswith(str(HOST)):
            files['lib/' + Path(path).name] = Path(path)
    for path in (HOST/'usr/share/qemu/keymaps').rglob('*'):
        if path.is_file():files['share/qemu/keymaps/'+path.name]=path
    wrapper = b'#!/bin/sh\nbase=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)\nexec "$base/lib/ld-musl-x86_64.so.1" --library-path "$base/lib" "$base/qemu-system-aarch64" -L "$base/share/qemu" "$@"\n'
    with archive_writer(OUTPUT/'qemu-host.tar.gz') as temporary, tarfile.open(str(temporary), 'w:gz') as archive:
        for name, path in sorted(files.items()):
            data = path.read_bytes(); info = tarfile.TarInfo(name); info.size = len(data); info.mode = 0o755
            archive.addfile(info, io.BytesIO(data))
        info = tarfile.TarInfo('qemu'); info.size = len(wrapper); info.mode = 0o755
        archive.addfile(info, io.BytesIO(wrapper))
        for name in ('GPL-2', 'LGPL-2.1', 'LGPL-3'):
            data = (Path('/usr/share/common-licenses')/name).read_bytes()
            info = tarfile.TarInfo('licenses/'+name); info.size = len(data)
            archive.addfile(info, io.BytesIO(data))
    write_json(OUTPUT/'qemu-host.json', {'version': subprocess.check_output([str(loader), '--library-path', str(HOST/'usr/lib')+':'+str(HOST/'lib'), str(binary), '--version'], universal_newlines=True).splitlines()[0], 'upstream': 'https://www.qemu.org/download/', 'files': {name:hashlib.sha256(path.read_bytes()).hexdigest() for name,path in files.items()}, 'host': 'x86_64 Linux; override QEMU_AARCH64 on other hosts'})


def font():
    # FreeType's cmap selects actual glyphs, never a font's missing-glyph box.
    ft = C.CDLL('libfreetype.so.6'); library = C.c_void_p()
    ft.FT_Init_FreeType(C.byref(library))
    ft.FT_New_Face.argtypes = [C.c_void_p,C.c_char_p,C.c_long,C.POINTER(C.c_void_p)]
    ft.FT_Get_First_Char.argtypes = [C.c_void_p,C.POINTER(C.c_uint)]; ft.FT_Get_First_Char.restype = C.c_ulong
    ft.FT_Get_Next_Char.argtypes = [C.c_void_p,C.c_ulong,C.POINTER(C.c_uint)]; ft.FT_Get_Next_Char.restype = C.c_ulong
    paths = [Path('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')]
    paths += [ALPINE/'usr/share/fonts/noto'/name for name in ['NotoSans-Regular.ttf','NotoSansArabic-Regular.ttf','NotoSansHebrew-Regular.ttf']]
    paths += sorted((ALPINE/'usr/share/fonts/noto').glob('NotoSans*Regular.ttf'))
    paths += sorted((ALPINE/'usr/share/fonts/noto').glob('NotoSerif*Regular.ttf'))
    paths += [Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')]
    faces = []; coverage = {}; seen = set()
    for path in paths:
        if not path.is_file() or path in seen: continue
        seen.add(path); face = C.c_void_p()
        if ft.FT_New_Face(library, str(path).encode(), 0, C.byref(face)): continue
        slot = len(faces); faces.append((path, ImageFont.truetype(str(path), 13 if slot == 0 else 16)))
        glyph = C.c_uint(); char = ft.FT_Get_First_Char(face, C.byref(glyph))
        while glyph.value:
            if char < 65536 or 0x1f600 <= char < 0x1f650:
                coverage.setdefault(char, slot)
            char = ft.FT_Get_Next_Char(face, char, C.byref(glyph))
        ft.FT_Done_Face(face)
    data = bytearray()
    for char in list(range(65536)) + list(range(0x1f600,0x1f650)):
        image = Image.new('L', (16,16))
        if char >= 32 and char in coverage:
            path, face = faces[coverage[char]]
            canvas = Image.new('L',(48,48)); ImageDraw.Draw(canvas).text((0,0),chr(char),font=face,fill=255)
            box = canvas.getbbox()
            if box:
                if char < 256:
                    ImageDraw.Draw(image).text((0,-1),chr(char),font=face,fill=255)
                else:
                    glyph = canvas.crop(box)
                    if glyph.width > 16 or glyph.height > 16:
                        glyph.thumbnail((16,16), Image.LANCZOS)
                    image.paste(glyph, ((16-glyph.width)//2, (16-glyph.height)//2))
        for y in range(16):
            bits = 0
            for x in range(16): bits = (bits << 1) | (image.getpixel((x,y)) >= 96)
            data += bits.to_bytes(2,'big')
    (OUTPUT/'terminal-font.bin').write_bytes(data)
    write_json(OUTPUT/'terminal-font.json', {'name':'WorldOS multi-script bitmap', 'glyphs':65616, 'sha256':hashlib.sha256(data).hexdigest(), 'coverage':sorted(coverage), 'sources':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p,_ in faces}, 'shaping':'individual Unicode glyphs; full Indic shaping and bidi are not implemented'})


class Names(C.Structure):
    _fields_ = [(name,C.c_char_p) for name in ('rules','model','layout','variant','options')]


def keyboard(layout, variant=''):
    lib = C.CDLL('libxkbcommon.so.0')
    lib.xkb_context_new.argtypes=[C.c_int]; lib.xkb_context_new.restype=C.c_void_p
    lib.xkb_keymap_new_from_names.argtypes=[C.c_void_p,C.POINTER(Names),C.c_int]; lib.xkb_keymap_new_from_names.restype=C.c_void_p
    lib.xkb_keymap_key_get_syms_by_level.argtypes=[C.c_void_p,C.c_uint,C.c_uint,C.c_uint,C.POINTER(C.POINTER(C.c_uint))]
    lib.xkb_keysym_to_utf32.argtypes=[C.c_uint];lib.xkb_keysym_to_utf32.restype=C.c_uint
    lib.xkb_keymap_unref.argtypes=[C.c_void_p];lib.xkb_context_unref.argtypes=[C.c_void_p]
    context=lib.xkb_context_new(0)
    names=Names(b'evdev',b'pc105',layout.encode(),variant.encode(),b'')
    keymap=lib.xkb_keymap_new_from_names(context,C.byref(names),0)
    if not keymap: lib.xkb_context_unref(context); raise ValueError('XKB layout unavailable: '+layout+'/'+variant)
    usnames=Names(b'evdev',b'pc105',b'us',b'',b'')
    us=lib.xkb_keymap_new_from_names(context,C.byref(usnames),0)
    dead={0xfe50:0x300,0xfe51:0x301,0xfe52:0x302,0xfe53:0x303,0xfe54:0x304,0xfe55:0x306,0xfe56:0x307,0xfe57:0x308,0xfe58:0x30a,0xfe59:0x30b,0xfe5a:0x30c,0xfe5b:0x327,0xfe5c:0x328}
    def symbol(km,code,level):
        ptr=C.POINTER(C.c_uint)()
        n=lib.xkb_keymap_key_get_syms_by_level(km,code,0,level,C.byref(ptr))
        return ptr[0] if n else 0
    result={'kind':'keyboard','layout':layout,'variant':variant,'map':{},'altgr':{},'source':'XKeyboardConfig (frozen keysym levels; US host key positions)'}
    for code in range(9,256):
        for level in (0,1):
            source=lib.xkb_keysym_to_utf32(symbol(us,code,level))
            if not 32<=source<127:continue
            for extra, field in ((0,'map'),(2,'altgr')):
                sym=symbol(keymap,code,level+extra); cp=lib.xkb_keysym_to_utf32(sym)
                if sym in dead:result[field][chr(source)]='dead:'+format(dead[sym],'x')
                elif cp>=32:result[field][chr(source)]=chr(cp)
    lib.xkb_keymap_unref(us);lib.xkb_keymap_unref(keymap);lib.xkb_context_unref(context)
    return result


def phonetic(filename, kind):
    path=ALPINE/'usr/share/m17n'/filename
    text=path.read_text(); table={}
    # Only literal mappings are imported. We do not pretend to interpret m17n's
    # state language. Japanese kana and Ethiopic SERA use these literal rules.
    quoted=r'"((?:[^"\\]|\\.)*)"'
    def unquote(value):return re.sub(r'\\(.)',r'\1',value)
    for match in re.finditer(r'\(\s*'+quoted+r'\s+(?:'+quoted+r'|\?(\S))\s*\)',text):
        key=unquote(match.group(1)); value=unquote(match.group(2)) if match.group(2) is not None else match.group(3)
        if key and value and all(32<=ord(c)<127 for c in key):table[key]=value
    if kind=='candidates':
        for match in re.finditer(r'\(\s*"([a-z]+)"\s*\(((?:\s*"[^"\n]*")+)\s*\)\)',text):
            table[match.group(1)]=[c for c in ''.join(re.findall(r'"([^"]*)"',match.group(2))) if ord(c)<65536]
    if kind=='kana': table.update({'n':'ん',"n'":'ん','nn':'ん'})
    if not table:raise ValueError('No input rules: '+filename)
    return {'kind':kind,'map':table,'source':'m17n-db '+filename, 'upstream_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('action',choices=['font','qemu']);args=p.parse_args()
    OUTPUT.mkdir(parents=True,exist_ok=True)
    {'font':font,'qemu':bundle_qemu}[args.action]()
