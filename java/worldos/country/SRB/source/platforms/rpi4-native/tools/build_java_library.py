#!/usr/bin/env python3
"""기존 ПУТАЊА 호환 унос_поен. стваран_подаци 구현: ../Алатке/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as оперативни_систем_вриједност
from pathlib import Path as ПУТАЊА
оперативни_систем_вриједност.path.insert(0, str(ПУТАЊА(__file__).resolve().parents[1] / 'Алатке'))
if __name__ == '__main__':
    import runpy as програм_покретач
    програм_покретач.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'Заглавље_вриједност', 'sources': '원문목록', 'i': '순번', 'info': 'Информације_о_систему', 'payload': 'корисни_подаци_подаци', 'src': '원본주소', 'run': 'Изврши_команда', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'класа_пут', 'dist': '배포경로', 'archive': 'Архива', 'output': '출력결과', 'root': 'корен_адреса', 'name': 'Назив', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, актуелно_ставка in 대응.items():
        if hasattr(구현, актуелно_ставка): globals()[이전] = getattr(구현, актуелно_ставка)
