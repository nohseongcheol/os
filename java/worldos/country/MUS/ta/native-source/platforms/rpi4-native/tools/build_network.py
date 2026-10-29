#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/தொகு_பிணையம்.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('தொகு_பிணையம்', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('தொகு_பிணையம்')
    대응 = {'obj': 'இலக்குக்_கோப்பு', 'objects': 'இலக்கு_கோப்புகள்', 'library': 'நூலகம்', 'output': '출력결과', 'port': 'முனைய_எண்', 'root': 'மூலம்_முகவரி', 'files': 'கோப்பு_பட்டியல்', 'source': '원본자료', 'run': 'இயக்கு_கட்டளை', 'flags': 'உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை', 'path': 'பாதை_2', 'build_network': 'உருவாக்கு_பிணையம்', 'cc': '시언어번역기', 'ar': 'காப்பகம்_கருவி'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
