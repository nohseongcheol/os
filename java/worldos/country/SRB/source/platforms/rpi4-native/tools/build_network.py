#!/usr/bin/env python3
"""기존 ПУТАЊА 호환 унос_поен. стваран_подаци 구현: ../Алатке/градити_Мрежа.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as ПУТАЊА
оперативни_систем_вриједност.path.insert(0, str(ПУТАЊА(__file__).resolve().parents[1] / 'Алатке'))
if __name__ == '__main__':
    import runpy as програм_покретач
    програм_покретач.run_module('градити_Мрежа', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('градити_Мрежа')
    대응 = {'obj': 'одредишни_фајл', 'objects': 'одредиште_Фајлови', 'library': 'библиотека', 'output': '출력결과', 'port': 'број_порта', 'root': 'корен_адреса', 'files': 'фајл_Листа', 'source': '원본자료', 'run': 'Изврши_команда', 'flags': 'конфигурација_Услуга_интелигентног_преноса_у_позадини', 'path': 'ПУТАЊА', 'build_network': 'Направи_Мрежа', 'cc': '시언어번역기', 'ar': 'Архива_алат'}
    for 이전, актуелно_ставка in 대응.items():
        if hasattr(구현, актуелно_ставка): globals()[이전] = getattr(구현, актуелно_ставка)
