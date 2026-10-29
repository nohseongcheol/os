#!/usr/bin/env python3
"""기존 मार्ग 호환 प्रविष्टि_अंक. वास्तविक_लगत 구현: ../उपकरणहरू/सिर्जना_छवि.py"""
import importlib as 가져오기
import sys as सञ्चालनप्रणाली_मान
from pathlib import Path as मार्ग
सञ्चालनप्रणाली_मान.path.insert(0, str(मार्ग(__file__).resolve().parents[1] / 'उपकरणहरू'))
if __name__ == '__main__':
    import runpy as अनुप्रयोग_कर्मचारी_अगुवा
    अनुप्रयोग_कर्मचारी_अगुवा.run_module('सिर्जना_छवि', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('सिर्जना_छवि')
    대응 = {'total': '총량', 'start': 'चलाउनुहोस्', 'firmware': '기초제어프로그램', 'files': 'फाइल_सूची', 'archive_base': '압축기준', 'partition': 'विभाजन_फाइल', 'archive': 'सङ्ग्रह', 'main': 'चलाउनुहोस्', 'block': 'लगत_छेक्नुहोस्', 'ROOT': 'परियोजना_रूट', 'boot': '부팅경로', 'stage': 'चरण_मान', 'out': 'मापन_लगत', 'expected': '예상결과', 'f': 'फाइल_प्रविष्टि', 'src': '원본주소', 'path': 'मार्ग', 'p': 'लगत_राख्नुहोस्', 'extracted': '추출자료', 'member': 'सदस्य', 'mbr': '주부트기록', 'image': 'छवि', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'इजाजतपत्र', 'source': '원본자료', 'name': 'नाम', 'value': 'मान', 'manifest': '꾸러미명세', 'dest': 'गन्तव्य_मान_राख्नुहोस्', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
