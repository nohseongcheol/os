#!/usr/bin/env python3
"""Exercise RFB key events against an edition's real input bridge, without QEMU."""
import importlib.util
import json
from pathlib import Path
import sys

folder=Path(sys.argv[1]).resolve()
config=json.loads((folder/'native.json').read_text())
native=folder/config['source']/config['native']
mapping=config['identifiers']
tools=native/Path(config['runner']).parent
sys.path.insert(0,str(tools))
path=tools/(mapping.get('바탕화면','바탕화면')+'.py')
spec=importlib.util.spec_from_file_location('edition_bridge',str(path))
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
buffer=[''];modes=[]
def send(data):
    for char in data.decode('utf-8'):
        buffer[0]=buffer[0][:-1] if char=='\x7f' else buffer[0]+char
bridge=getattr(module,mapping.get('글쇠판','글쇠판'))(send,modes.append)
event=getattr(bridge,mapping.get('누름값','누름값'))
def tap(key):event(True,key);event(False,key)
def type_keys(text):
    for key in text:tap(ord(key))
profile=json.loads((native/'input.json').read_text())
for shift in (False,True):
    buffer[0]=''
    if shift:event(True,0xffe1);tap(32);event(False,0xffe1)
    else:
        # Auto-repeat keydown must not toggle the mode repeatedly.
        event(True,0xffc6);event(True,0xffc6);event(False,0xffc6)
    assert modes[-1] is True
    type_keys(profile['sample_keys']);tap(0xffc6)
    assert buffer[0]==profile['sample'],(config['country'],buffer,profile['sample'])
    assert modes[-1] is False
checks=['F9 repeat guard','Shift+Space','locale sample','ASCII return']
if profile['kind']=='candidates':
    buffer[0]='';tap(0xffc6);type_keys(profile['sample_keys']);tap(32)
    expected=profile['map'][profile['sample_keys']][1]
    assert buffer[0]==expected,(buffer,expected)
    tap(0xffc6);checks.append('candidate cycling')
if profile['kind']=='keyboard':
    import unicodedata
    candidates=[(k,v) for k,v in profile.get('altgr',{}).items() if not v.startswith('dead:') and v!=profile['map'].get(k,k)]
    if candidates:
        key,value=candidates[0];buffer[0]='';tap(0xffc6)
        event(True,0xfe03);tap(ord(key));event(False,0xfe03);tap(0xffc6)
        assert buffer[0]==value,(buffer,value);checks.append('AltGr')
    accents=[(k,v) for k,v in profile.get('altgr',{}).items() if v.startswith('dead:')]
    if accents:
        key,value=accents[0];buffer[0]='';tap(0xffc6)
        event(True,0xfe03);tap(ord(key));event(False,0xfe03)
        tap(0xff08);tap(ord('a'));tap(0xffc6)
        assert buffer[0]==profile['map'].get('a','a'),buffer
        checks.append('dead accent backspace')
buffer[0]=''
event(True,0xffe3);event(True,0xffe1);tap(ord('u'));event(False,0xffe1);event(False,0xffe3)
type_keys('1f600');tap(0xff0d)
assert buffer[0]=='😀',buffer
checks.append('Unicode scalar entry')
print(json.dumps({'country':config['country'],'passed':True,'checks':checks},ensure_ascii=False))
