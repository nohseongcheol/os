#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/창시험.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('창시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('창시험')
    대응 = {'wait': '기다리기', 'x': 'x_યામ', 's': 'સ્ટ્રિંગ_ડેટા', 'xy': 'યામ_જોડ', 'sel': 'પસંદકર્તા_a916db4e', 'seconds': '초단위', 'log': 'લૉગ_પંક્તિ', 'at': '현재위치', 'send': 'મોકલો', 'main': 'ચલાવો_2', 'req': '요청값', 'hot': 'શૉર્ટકટ_મૂલ્ય', 'pump': 'હેન્ડલ_ઇવેંટ', 'ROOT': 'પ્રોજેક્ટ_રૂટ', 'marker': '확인표시', 'b': '둘째값', 'command': 'આદેશ', 'shell': 'શેલ', 'f': 'ફાઇલ_પ્રવેશ', 'color': '색상', 'click': 'ક્લિક_કરો_બટન', 'k': '셋째순번', 'c': 'વર્ણ_કોડ', 'r': '반환값', 'p': 'ડેટા_સ્થિતિ', 'done': '완료량', 'end': 'અંત_કરો_ઑફસેટ', 'command_mode': 'આદેશ_મોડ', 'key': '누름값', 'y': '세로좌표', 'pixels': '화소들', 'result': 'પરિમાણ', 'report': 'માન્યતા_અહેવાલ', 'dest': 'ગંતવ્ય_મૂલ્ય_સ્થિતિ', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
