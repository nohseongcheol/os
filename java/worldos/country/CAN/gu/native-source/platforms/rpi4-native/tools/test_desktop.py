#!/usr/bin/env python3
"""기존 પથ 호환 પ્રવેશ_બિંદુ. વાસ્તવિક_ડેટા 구현: ../ઉપકરણો/바탕화면시험.py"""
import importlib as 가져오기
import sys as ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય
from pathlib import Path as પથ
ઑપરેટિંગ_સિસ્ટમ_મૂલ્ય.path.insert(0, str(પથ(__file__).resolve().parents[1] / 'ઉપકરણો'))
if __name__ == '__main__':
    import runpy as એપ્લિકેશન_લૉન્ચર
    એપ્લિકેશન_લૉન્ચર.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_યામ', 'typing': '글자입력', 'message': '알림문', 'start': 'ચલાવો_2', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'પ્રતીક', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'પ્રક્રિયા', 'data': 'ડેટા', 'main': 'ચલાવો_2', 'w': '너비값', 'init': '초기값', 'block': 'ડેટા_અવરોધિત_કરો', 'ROOT': 'પ્રોજેક્ટ_રૂટ', 'text': 'લખાણ', 'marker': '확인표시', 'report': 'માન્યતા_અહેવાલ', 'until': '까지', 'clipboard': 'ક્લિપબોર્ડ_મૂલ્ય', 'dst': 'ગંતવ્ય_સરનામું', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': 'પોર્ટ_નંબર', 'offset': 'ઑફસેટ_મૂલ્ય', 'h': '높이값', 'src': '원본주소', 'event': 'ઇવેંટ', 'encoding': 'વર્ણ_સેટ', 'size': 'માપ', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'પ્રતીક_મૂલ્ય', 'client': 'ક્લાયંટ', 'char': 'વર્ણ_ડેટા', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
