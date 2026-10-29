#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/바탕화면시험.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'координатаи_х', 'typing': '글자입력', 'message': '알림문', 'start': 'порча', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'аломат', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Раванд', 'data': 'иттилоот', 'main': 'порча', 'w': '너비값', 'init': '초기값', 'block': 'иттилоот_манъ_кардан', 'ROOT': '기준', 'text': 'Матн', 'marker': '확인표시', 'report': 'санҷиши_эътибор_гузориш', 'until': '까지', 'clipboard': 'ҳофизаи_муваққатӣ_қимат', 'dst': 'ҷои_таъинот_суроға', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'Интиқолшавӣ_қимат', 'h': '높이값', 'src': '원본주소', 'event': 'рӯйдод', 'encoding': 'маҷмӯи_аломатҳо', 'size': 'андоза_кардан', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'аломат_қимат', 'client': 'муштарӣ', 'char': 'аломат_иттилоот_4d9f8719', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
