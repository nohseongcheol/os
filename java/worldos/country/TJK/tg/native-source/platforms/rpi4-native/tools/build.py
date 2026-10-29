#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/сохт_система.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('сохт_система', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('сохт_система')
    대응 = {'network': 'Шабака', 'BUILD': 'сохт_масир', 'ar': 'Бойгонӣ_абзор', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'шрифт_иттилоот', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'аргумент_қатор', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'сабк_ворида', 'main': 'порча', 'objcopy': 'объект_файл_конвертер', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'эҷод_кардан_корбар_фазо', 'f': 'файл_ворида', 'extra': '추가영역', 'exports': 'содир_кардан_ҷадвал', 'jobs': '빌드작업', 'run': 'иҷро_кардан_фармон', 'path': 'масир', 'REPO': '저장소', 'tool': 'Абзорҳо', 'classes': 'синф_масир', 'output': '출력결과', 'samples': '예제들', 'symbol': 'аломат_қимат', 'source': '원본자료', 'name': 'Ном', 'build_network': 'эҷод_кардан_Шабака', 'font_info': 'шрифт_маълумот', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
