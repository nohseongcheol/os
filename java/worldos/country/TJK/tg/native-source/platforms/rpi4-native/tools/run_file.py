#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/иҷро_кардан_файл.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('иҷро_кардан_файл', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('иҷро_кардан_файл')
    대응 = {'timeout': '시간제한', 's': 'сатр_иттилоот', 'i': '순번', 'match': '일치', 'files': 'файл_Рӯйхат', 'program': 'барнома', 'executable': '실행가능파일', 'args': 'аргумент_қатор', 'chunk': '조각', 'data': 'иттилоот', 'proc': 'Раванд', 'send': 'фиристодан', 'main': 'порча', 'marker': '확인표시', 'command': 'фармон', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'иҷро_кардан_фармон', 'p': '자료위치', 'parser': '인수해석기', 'options': 'Имконот', 'kind': 'категория_қимат', 'selector': 'интихобкунанда', 'upload_data': 'бор_кардан_иттилоот', 'end': 'анҷом_додан_Интиқолшавӣ', 'n': '개수', 'd': 'ҷои_таъинот_иттилоот', 'key': '누름값', 'output': '출력결과', 'line': 'хат', 'name': 'Ном', 'upload_name': 'бор_кардан_ном', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
