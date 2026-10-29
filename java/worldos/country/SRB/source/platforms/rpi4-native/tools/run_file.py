#!/usr/bin/env python3
"""기존 ПУТАЊА 호환 унос_поен. стваран_подаци 구현: ../Алатке/Изврши_фајл.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as ПУТАЊА
оперативни_систем_вриједност.path.insert(0, str(ПУТАЊА(__file__).resolve().parents[1] / 'Алатке'))
if __name__ == '__main__':
    import runpy as програм_покретач
    програм_покретач.run_module('Изврши_фајл', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Изврши_фајл')
    대응 = {'timeout': '시간제한', 's': 'ниска_подаци', 'i': '순번', 'match': '일치', 'files': 'фајл_Листа', 'program': 'програм', 'executable': '실행가능파일', 'args': 'аргумент_низ', 'chunk': '조각', 'data': 'подаци', 'proc': 'Процес', 'send': 'послати', 'main': 'Покрени', 'marker': '확인표시', 'command': 'Наредба', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'Изврши_команда', 'p': 'подаци_позиција', 'parser': 'анализатор', 'options': 'Опције', 'kind': 'област_вриједност', 'selector': 'бирач', 'upload_data': 'Отпрема_подаци', 'end': 'завршити_Помак', 'n': '개수', 'd': 'одредиште_подаци', 'key': '누름값', 'output': '출력결과', 'line': 'Ред', 'name': 'Назив', 'upload_name': 'Отпрема_име', 'receive': '수신하기'}
    for 이전, актуелно_ставка in 대응.items():
        if hasattr(구현, актуелно_ставка): globals()[이전] = getattr(구현, актуелно_ставка)
