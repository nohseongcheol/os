#!/usr/bin/env python3
"""기존 пут 호환 унос_тачка. стваран_подаци 구현: ../도구/направити_Мрежа.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as пут
оперативни_систем_вриједност.path.insert(0, str(пут(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('направити_Мрежа', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('направити_Мрежа')
    대응 = {'obj': 'одредишни_фајл', 'objects': '목적파일들', 'library': 'библиотека', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'фајл_списак', 'source': '원본자료', 'run': '실행', 'flags': '설정비트', 'path': 'пут', 'build_network': '통신망만들기', 'cc': '시언어번역기', 'ar': 'архива_алатка'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
