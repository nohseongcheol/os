#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/셸시험.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'координатаи_х', 'msg': 'Шабака_паём', 'i': '순번', 'reply': 'ҷавоб_додан', 'call': '호출', 'args': 'аргумент_қатор', 'chunk': '조각', 'data': 'иттилоот', 'proc': 'Раванд', 'long_text': '긴글', 'restored': '복원자료', 'send': 'фиристодан', 'file': 'Файл', 'main': 'порча', 'found': '찾은결과', 'ROOT': '기준', 'text': 'Матн', 'marker': '확인표시', 'command': 'фармон', 'expected': '예상결과', 'pixel': 'пиксел', 'shell': 'восит', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'анҷом_додан_Интиқолшавӣ', 'image': 'расм', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'муштарӣ', 'line': 'хат', 'stream': 'ҷараён_қимат', 'name': 'Ном', 'value': 'қимат', 'receive': '수신하기', 'report': 'санҷиши_эътибор_гузориш', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
