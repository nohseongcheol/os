#!/usr/bin/env python3
"""기존 ПУТАЊА 호환 унос_поен. стваран_подаци 구현: ../Алатке/자바가상기계시험.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as ПУТАЊА
оперативни_систем_вриједност.path.insert(0, str(ПУТАЊА(__file__).resolve().parents[1] / 'Алатке'))
if __name__ == '__main__':
    import runpy as програм_покретач
    програм_покретач.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'ниска_подаци', 'actual': 'стваран_мера', 'match': '일치', 'payload': 'корисни_подаци_подаци', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Покрени', 'ROOT': 'пројектовати_корен', 'text': 'Текст', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'Довршено_износ', 'classes': 'класа_пут', 'output': '출력결과', 'result': 'ИСХОД', 'cmd': '명령인수', 'name': 'Назив', 'jar': '자바꾸러미', 'report': 'провјера_извештај', 'tests': '시험목록'}
    for 이전, актуелно_ставка in 대응.items():
        if hasattr(구현, актуелно_ставка): globals()[이전] = getattr(구현, актуелно_ставка)
