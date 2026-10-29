#!/usr/bin/env python3
"""기존 пут 호환 унос_тачка. стваран_подаци 구현: ../도구/화면요소시험.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as пут
оперативни_систем_вриједност.path.insert(0, str(пут(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': '가로좌표', 's': 'стринг_подаци', 'i': '순번', 'sel': '선택기', 'seconds': '초단위', 'log': 'дневник_рада_ред', 'data': 'подаци', 'at': '현재위치', 'send': 'послати', 'main': '시작', 'req': '요청값', 'hot': 'пречица_вриједност', 'pump': 'хватиште_догађај', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'команда', 'shell': 'љуска', 'f': 'фајл_унос', 'click': 'кликнути_дугме', 'k': '셋째순번', 'c': 'кôд_знака', 'r': '반환값', 'p': '자료위치', 'command_mode': 'команда_мод', 'end': '끝위치', 'classes': 'класа_пут', 'key': '누름값', 'y': '세로좌표', 'result': '결과', 'report': 'провјера_извјештај', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
