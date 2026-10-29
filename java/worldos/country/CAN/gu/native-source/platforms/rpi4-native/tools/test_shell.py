#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/셸시험.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_યામ', 'msg': 'નેટવર્ક_સંદેશ', 'i': '순번', 'reply': 'જવાબ', 'call': '호출', 'args': 'દલીલ_અરે', 'chunk': '조각', 'data': 'ડેટા', 'proc': 'પ્રક્રિયા', 'long_text': '긴글', 'restored': '복원자료', 'send': 'મોકલો', 'file': 'ફાઈલ', 'main': 'ચલાવો_2', 'found': 'શોધ_પરિમાણ', 'ROOT': 'પ્રોજેક્ટ_રૂટ', 'text': 'લખાણ', 'marker': '확인표시', 'command': 'આદેશ', 'expected': '예상결과', 'pixel': 'પેલ', 'shell': 'શેલ', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'અંત_કરો_ઑફસેટ', 'image': 'છબી', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': 'પરિમાણ', 'client': 'ક્લાયંટ', 'line': 'લાઇન', 'stream': 'સ્ટ્રીમ_મૂલ્ય', 'name': 'નામ', 'value': 'મૂલ્ય', 'receive': '수신하기', 'report': 'માન્યતા_અહેવાલ', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
