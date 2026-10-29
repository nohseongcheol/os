#!/usr/bin/env python3
"""기존 ПАТЕКА 호환 внес_поен. реален_податоци 구현: ../Алатки/верзија_систем.py"""
import importlib as TAKE_VALUE
import sys as оперативен_систем_VALUE
from pathlib import Path as ПАТЕКА
оперативен_систем_VALUE.path.insert(0, str(ПАТЕКА(__file__).resolve().parents[1] / 'Алатки'))
if __name__ == '__main__':
    import runpy as програма_стартувач
    програма_стартувач.run_module('верзија_систем', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('верзија_систем')
    대응 = {'network': 'Мрежа', 'BUILD': 'верзија_патека', 'ar': 'Архива_алатка', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'фонт_податоци', 'flags': 'конфигурација_Услуга_за_интелигентен_пренос_во_заднина', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'аргумент_низа', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'метод_внес', 'main': 'Изврши_2', 'objcopy': 'објект_датотека_конвертор', 'ROOT': 'Project_корен', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'Create_корисник_простор', 'f': 'датотека_внес', 'extra': '추가영역', 'exports': 'извези_табела', 'jobs': '빌드작업', 'run': 'Изврши_наредба', 'path': 'ПАТЕКА', 'REPO': 'склад_корен', 'tool': 'Алатки', 'classes': 'класа_патека', 'output': '출력결과', 'samples': '예제들', 'symbol': 'симбол_VALUE', 'source': '원본자료', 'name': 'Име', 'build_network': 'Create_Мрежа', 'font_info': 'фонт_информации', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
