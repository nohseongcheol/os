#!/usr/bin/env python3
"""기존 ПУТАЊА 호환 унос_поен. стваран_подаци 구현: ../Алатке/градити_систем.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as ПУТАЊА
оперативни_систем_вриједност.path.insert(0, str(ПУТАЊА(__file__).resolve().parents[1] / 'Алатке'))
if __name__ == '__main__':
    import runpy as програм_покретач
    програм_покретач.run_module('градити_систем', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('градити_систем')
    대응 = {'network': 'Мрежа', 'BUILD': 'градити_пут', 'ar': 'Архива_алат', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'фонт_подаци', 'flags': 'конфигурација_Услуга_интелигентног_преноса_у_позадини', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'аргумент_низ', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'метода_унос', 'main': 'Покрени', 'objcopy': 'објекат_фајл_претварач', 'ROOT': 'пројектовати_корен', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'Направи_корисник_простор', 'f': 'фајл_унос', 'extra': '추가영역', 'exports': 'Извоз_табела', 'jobs': '빌드작업', 'run': 'Изврши_команда', 'path': 'ПУТАЊА', 'REPO': 'депо_корен', 'tool': 'Алатке', 'classes': 'класа_пут', 'output': '출력결과', 'samples': '예제들', 'symbol': 'симбол_вриједност', 'source': '원본자료', 'name': 'Назив', 'build_network': 'Направи_Мрежа', 'font_info': 'фонт_информација', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, актуелно_ставка in 대응.items():
        if hasattr(구현, актуелно_ставка): globals()[이전] = getattr(구현, актуелно_ставка)
