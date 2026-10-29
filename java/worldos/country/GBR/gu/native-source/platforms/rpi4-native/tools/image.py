#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/બનાવો_છબી.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('બનાવો_છબી', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('બનાવો_છબી')
    대응 = {'total': '총량', 'start': 'ચલાવો_2', 'firmware': '기초제어프로그램', 'files': 'ફાઇલ_સૂચી', 'archive_base': '압축기준', 'partition': 'વિભાજન_ફાઇલ', 'archive': 'સંગ્રહ', 'main': 'ચલાવો_2', 'block': 'ડેટા_અવરોધિત_કરો', 'ROOT': 'પ્રોજેક્ટ_રૂટ', 'boot': '부팅경로', 'stage': 'સ્ટેજ_મૂલ્ય', 'out': 'પરિમાણ_ડેટા', 'expected': '예상결과', 'f': 'ફાઇલ_પ્રવેશ', 'src': '원본주소', 'path': 'પથ', 'p': 'ડેટા_સ્થિતિ', 'extracted': '추출자료', 'member': 'સદસ્ય', 'mbr': '주부트기록', 'image': 'છબી', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'લાઇસન્સ', 'source': '원본자료', 'name': 'નામ', 'value': 'મૂલ્ય', 'manifest': '꾸러미명세', 'dest': 'ગંતવ્ય_મૂલ્ય_સ્થિતિ', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
