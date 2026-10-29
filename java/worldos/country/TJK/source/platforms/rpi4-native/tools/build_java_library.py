#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'Сарнавор_қимат', 'sources': '원문목록', 'i': '순번', 'info': 'Маълумоти_система', 'payload': 'қобилият_иттилоот', 'src': '원본주소', 'run': 'иҷро_кардан_фармон', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'синф_масир', 'dist': '배포경로', 'archive': 'Бойгонӣ', 'output': '출력결과', 'root': '뿌리주소', 'name': 'Ном', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
