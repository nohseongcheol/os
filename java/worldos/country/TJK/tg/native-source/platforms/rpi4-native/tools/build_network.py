#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/сохт_Шабака.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('сохт_Шабака', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('сохт_Шабака')
    대응 = {'obj': 'файли_ниҳоӣ', 'objects': 'ҷои_таъинот_Файлҳо', 'library': 'китобхона', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'файл_Рӯйхат', 'source': '원본자료', 'run': 'иҷро_кардан_фармон', 'flags': '설정비트', 'path': 'масир', 'build_network': 'эҷод_кардан_Шабака', 'cc': '시언어번역기', 'ar': 'Бойгонӣ_абзор'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
