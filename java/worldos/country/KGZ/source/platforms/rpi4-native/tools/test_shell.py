#!/usr/bin/env python3
"""기존 ЖОЛ 호환 киргизме_жазуу_упай. актуалдуу_берилмелер 구현: ../Куралдар/셸시험.py"""
import importlib as 가져오기
import sys as оперативдик_система_маани
from pathlib import Path as ЖОЛ
оперативдик_система_маани.path.insert(0, str(ЖОЛ(__file__).resolve().parents[1] / 'Куралдар'))
if __name__ == '__main__':
    import runpy as програм_жаратма_тарткычы
    програм_жаратма_тарткычы.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'x_координата', 'msg': 'Желе_билдирүү', 'i': '순번', 'reply': 'жооп_берүү', 'call': '호출', 'args': 'аргумент_МАССИВ', 'chunk': '조각', 'data': 'берилмелер', 'proc': 'Процесси', 'long_text': '긴글', 'restored': '복원자료', 'send': 'жөнөтүү', 'file': 'Файл', 'main': 'Жүргүзүү', 'found': '찾은결과', 'ROOT': '기준', 'text': 'Текст', 'marker': '확인표시', 'command': 'Команда', 'expected': '예상결과', 'pixel': 'пиксел', 'shell': 'сырты', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'аяктоо_Жылбышуу', 'image': 'сүрөт', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'керектөөчү', 'line': 'сап', 'stream': 'агым_маани', 'name': 'Аты', 'value': 'маани', 'receive': '수신하기', 'report': 'ырастоо_отчет', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
