#!/usr/bin/env python3
"""기존 масир 호환 ворида_нуқта. воқеӣ_иттилоот 구현: ../Абзорҳо/예제빌드.py"""
import importlib as 가져오기
import sys as системаи_омил_қимат
from pathlib import Path as масир
системаи_омил_қимат.path.insert(0, str(масир(__file__).resolve().parents[1] / 'Абзорҳо'))
if __name__ == '__main__':
    import runpy as барнома_панели_барномаҳо
    барнома_панели_барномаҳо.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'файл_Рӯйхат', 'java': '자바실행', 'run': 'иҷро_кардан_фармон', 'path': 'масир', 'p': '자료위치', 'readme': 'файли_тафсилот', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': '색인', 'classes': 'синф_масир', 'repo': '저장소경로', 'root': '뿌리주소', 'content': 'Мӯҳтаво_қимат', 'source': '원본자료', 'name': 'Ном', 'target': 'ҳадаф', 'manifest': '꾸러미명세', 'language': 'Забон'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
