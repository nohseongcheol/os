#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/원격한글시험.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('원격한글시험')
    대응 = {'wait': '기다리기', 'typing': '글자입력', 'start': 'ચલાવો_2', 'profile': 'પ્રોફાઇલ', 'focused': 'ફોકસ_કરાયેલ', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'સર્વર_મૂલ્ય', 'log': 'લૉગ_પંક્તિ', 'args': 'દલીલ_અરે', 'deadline': '마감시각', 'data': 'ડેટા', 'candidate': '후보', 'logs': '기록들', 'kw': '이름붙인인수', 'number': '수치', 'main': 'ચલાવો_2', 'ready': '준비완료', 'found': 'શોધ_પરિમાણ', 'guest': 'અતિથિ', 'ROOT': 'પ્રોજેક્ટ_રૂટ', 'marker': '확인표시', 'text': 'લખાણ', 'out': 'પરિમાણ_ડેટા', 'env': '환경', 'f': 'ફાઇલ_પ્રવેશ', 'port': 'પોર્ટ_નંબર', 'offset': 'ઑફસેટ_મૂલ્ય', 'version': '판번호', 'p': 'ડેટા_સ્થિતિ', 'selector': 'પસંદકર્તા', 'xvfb': 'વર્ચુઅલ_પ્રદર્શન', 'display': 'પ્રદર્શન', 'n': '개수', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': '가상입력도구', 'name': 'નામ', 'window': 'વિંડો', 'report': 'માન્યતા_અહેવાલ', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
