#!/usr/bin/env python3
"""기존 ЖОЛ 호환 киргизме_жазуу_упай. актуалдуу_берилмелер 구현: ../Куралдар/바탕화면시험.py"""
import importlib as 가져오기
import sys as оперативдик_система_маани
from pathlib import Path as ЖОЛ
оперативдик_система_маани.path.insert(0, str(ЖОЛ(__file__).resolve().parents[1] / 'Куралдар'))
if __name__ == '__main__':
    import runpy as програм_жаратма_тарткычы
    програм_жаратма_тарткычы.run_module('바탕화면시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('바탕화면시험')
    대응 = {'x': 'x_координата', 'typing': '글자입력', 'message': '알림문', 'start': 'Жүргүзүү', 'down': '누르는중', 'exact': '정확한값', 'i': '순번', 'press': '글쇠누르기', 'rectangles': '사각형들', 'sym': 'символ', 'j': '안쪽순번', 'deadline': '마감시각', 'proc': 'Процесси', 'data': 'берилмелер', 'main': 'Жүргүзүү', 'w': '너비값', 'init': '초기값', 'block': 'берилмелер_тосмолоо', 'ROOT': '기준', 'text': 'Текст', 'marker': '확인표시', 'report': 'ырастоо_отчет', 'until': '까지', 'clipboard': 'алмашуу_буфери_маани', 'dst': 'көздөө_жайы_дарек', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': '대화기록', 'port': '접속번호', 'offset': 'Жылбышуу_маани', 'h': '높이값', 'src': '원본주소', 'event': 'окуя', 'encoding': 'символдор_тобу', 'size': 'Өлчөмү', 'key': '누름값', 'pixels': '화소들', 'y': '세로좌표', 'output': '출력결과', 'symbol': 'символ_маани', 'client': 'керектөөчү', 'char': 'символ_берилмелер_4d9f8719', 'rgb': '빛삼원색'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
