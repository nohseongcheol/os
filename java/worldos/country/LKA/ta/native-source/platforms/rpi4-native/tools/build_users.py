#!/usr/bin/env python3
"""기존 பாதை_2 호환 நுழைவுப்_புள்ளி. அசல்_தரவு 구현: ../கருவிகள்/தொகு_பயனர்_தளம்.py"""
import importlib as 가져오기
import sys as இயக்க_முறைமை_மதிப்பு
from pathlib import Path as பாதை_2
இயக்க_முறைமை_மதிப்பு.path.insert(0, str(பாதை_2(__file__).resolve().parents[1] / 'கருவிகள்'))
if __name__ == '__main__':
    import runpy as நிரல்_துவக்குநர்
    நிரல்_துவக்குநர்.run_module('தொகு_பயனர்_தளம்', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('தொகு_பயனர்_தளம்')
    대응 = {'mode': 'முறை_பயன்முறை', 'header': 'மேற்குறிப்பு_மதிப்பு', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'காப்பகம்_கருவி', 'posix': '포직스경로', 'payload': 'பேலோட்_தரவு', 'flags': 'உள்ளமைவு_பின்புல_நுண்ணறிவு_டிரான்ஸ்ஃபர்_சேவை', 'cases': 'சோதனைப்_பெட்டி', 'cc': '시언어번역기', 'data': 'தரவு', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': 'தொகுபதிவகம்_பாதை', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'உரை', 'headers': 'மேற்குறிப்பு_பட்டியல்', 'cxx': '시플플번역기', 'valid': 'தகுதியான', 'build': 'தொகு', 'build_users': 'உருவாக்கு_பயனர்_தளம்', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'நிரல்_மேற்குறிப்பு_ஆஃப்செட்', 'offset': 'ஆஃப்செட்_மதிப்பு', 'text_address': 'கட்டளை_முகவரி', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'இயக்கு_கட்டளை', 'path': 'பாதை_2', 'p': 'தரவு_நிலை', 'changed': '바뀐자료', 'n': '개수', 'flag': 'அமைப்புகள்_மதிப்பு', 'index': 'தேடுதல்_அடைவு', 'classes': 'பிரிவு_பாதை', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'தரவு_முகவரி', 'symbol': 'சின்னம்_மதிப்பு', 'root': 'மூலம்_முகவரி', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'பெயர்', 'value': 'மதிப்பு', 'fmt': 'வடிவம்', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
