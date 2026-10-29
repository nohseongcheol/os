#!/usr/bin/env python3
"""기존 पथ 호환 प्रवेश_बिदुं. वास्तविक_डेटा 구현: ../उपकरण/बनाएँ_छवि.py"""
import importlib as 가져오기
import sys as ऑपरेटिंग_सिस्टम_मान
from pathlib import Path as पथ
ऑपरेटिंग_सिस्टम_मान.path.insert(0, str(पथ(__file__).resolve().parents[1] / 'उपकरण'))
if __name__ == '__main__':
    import runpy as ऐप_लॉन्चर
    ऐप_लॉन्चर.run_module('बनाएँ_छवि', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('बनाएँ_छवि')
    대응 = {'total': '총량', 'start': 'चलाएँ', 'firmware': 'फ़र्मवेयर_मान', 'files': 'फ़ाइल_सूची', 'archive_base': '압축기준', 'partition': 'विभाजन_फ़ाइल', 'archive': 'संग्रह', 'main': 'चलाएँ', 'block': 'डेटा_ब्_लॉक', 'ROOT': 'प्रोजेक्ट_करें_मूल', 'boot': '부팅경로', 'stage': 'स्टेज_मान', 'out': 'परिणाम_डेटा', 'expected': '예상결과', 'f': 'फ़ाइल_एन्ट्री', 'src': '원본주소', 'path': 'पथ', 'p': 'डेटा_पद', 'extracted': '추출자료', 'member': 'सदस्य', 'mbr': 'मास्टर_बूट_रेकॉर्ड', 'image': 'छवि', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'लाइसेंस', 'source': '원본자료', 'name': 'नाम', 'value': 'मान', 'manifest': 'बंडल_सूची', 'dest': 'गंतव्य_मान_पद', 'work': '작업경로'}
    for 이전, अद्यतित_आइटम in 대응.items():
        if hasattr(구현, अद्यतित_आइटम): globals()[이전] = getattr(구현, अद्यतित_आइटम)
