#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/தொகு_முறைமை.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('தொகு_முறைமை', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('தொகு_முறைமை')
    대응 = {'network': 'பிணையம்', 'BUILD': 'தொகு_பாதை', 'ar': 'காப்பகம்_கருவி', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'எழுத்துரு_தரவு', 'flags': 'உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'மதிப்புரு_கோவை', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'முறை_உள்ளீடு', 'main': 'செயல்படுத்துக', 'objcopy': 'பொருள்_கோப்பு_மாற்றி', 'ROOT': 'திட்டப்பணி_மூலம்', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'உருவாக்கு_பயனர்_தளம்', 'f': 'கோப்பு_உள்ளீடு', 'extra': '추가영역', 'exports': 'ஏற்றுமதிசெய்_அட்டவணை', 'jobs': '빌드작업', 'run': 'இயக்கு_கட்டளை', 'path': 'பாதை_2', 'REPO': 'தொகுபதிவகம்_மூலம்', 'tool': 'கருவிகள்', 'classes': 'பிரிவு_பாதை', 'output': '출력결과', 'samples': '예제들', 'symbol': 'சின்னம்_மதிப்பு', 'source': '원본자료', 'name': 'பெயர்', 'build_network': 'உருவாக்கு_பிணையம்', 'font_info': 'எழுத்துரு_தகவல்', 'manifest': 'மூட்டை_தொற்றம்', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
