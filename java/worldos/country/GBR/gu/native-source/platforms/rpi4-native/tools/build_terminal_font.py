#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/બિલ્ડ_ટર્મિનલ_ફૉન્ટ.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('બિલ્ડ_ટર્મિનલ_ફૉન્ટ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('બિલ્ડ_ટર્મિનલ_ફૉન્ટ')
    대응 = {'data': 'ડેટા', 'img': 'રેખાંકન_મૂલ્ય', 'bits': '비트들', 'x': 'x_યામ', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'પાથ_સૂચી', 'y': '세로좌표', 'main': 'ચલાવો_2', 'src': '원본주소', 'fonts': 'ફૉન્ટ_સૂચી', 'ROOT': 'પ્રોજેક્ટ_રૂટ', 'p': 'ડેટા_સ્થિતિ', 'cp': 'વર્ણ_એન્કોડિંગ', 'target': 'લક્ષ્ય'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
