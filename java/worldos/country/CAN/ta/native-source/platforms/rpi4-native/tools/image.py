#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/உருவாக்கு_படம்.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('உருவாக்கு_படம்', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('உருவாக்கு_படம்')
    대응 = {'total': '총량', 'start': 'செயல்படுத்துக', 'firmware': '기초제어프로그램', 'files': 'கோப்பு_பட்டியல்', 'archive_base': '압축기준', 'partition': 'பகுதிப்பிரிப்பு_கோப்பு', 'archive': 'காப்பகம்', 'main': 'செயல்படுத்துக', 'block': 'தரவு_தடு', 'ROOT': 'திட்டப்பணி_மூலம்', 'boot': '부팅경로', 'stage': 'நிலை_மதிப்பு_29ee1bb7', 'out': 'அளவிடக்கூடியது_தரவு', 'expected': '예상결과', 'f': 'கோப்பு_உள்ளீடு', 'src': '원본주소', 'path': 'பாதை_2', 'p': 'தரவு_நிலை', 'extracted': '추출자료', 'member': 'உறுப்பினர்', 'mbr': '주부트기록', 'image': 'படம்', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'உரிமம்', 'source': '원본자료', 'name': 'பெயர்', 'value': 'மதிப்பு', 'manifest': 'மூட்டை_தொற்றம்', 'dest': 'இலக்கு_மதிப்பு_நிலை', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
