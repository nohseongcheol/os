#!/usr/bin/env python3
"""기존 Yul 호환 кертү_балл. фактик_мәгълүмат 구현: ../Кораллар/바탕화면시험.py"""
import importlib as TAKE_VALUE
import sys as операцион_система_VALUE
from pathlib import Path as Yul
операцион_система_VALUE.path.insert(0, str(Yul(__file__).resolve().parents[1] / 'Кораллар'))
if __name__ == '__main__':
    import runpy as кушымта_хезмәткәр
    кушымта_хезмәткәр.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('바탕화면시험')
    대응 = {'x': 'X_координатасы', 'typing': '글자입력', 'message': '알림문', 'start': 'эшләтү', 'down': '누르는중', 'exact': 'EXACT_VALUE', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'символ', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Процесс', 'data': 'мәгълүмат', 'main': 'эшләтү', 'w': '너비값', 'init': '초기값', 'block': 'мәгълүмат_тыю', 'ROOT': 'экранга_җибәрү_тамыр', 'text': 'Mäten', 'marker': '확인표시', 'report': 'раслау_отчет', 'until': '까지', 'clipboard': 'алмашу_буферы_VALUE', 'dst': 'күчерү_урыны_адрес', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'OFFSET_VALUE', 'h': '높이값', 'src': '원본주소', 'event': 'вакыйга', 'encoding': 'символлар_җыелмасы', 'size': 'үлчәмен_үзгәртү', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'символ_VALUE', 'client': 'клиент', 'char': 'символ_мәгълүмат_4d9f8719', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
