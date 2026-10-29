#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/예제빌드.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'ئۆلچەم_مەلۇمات', 'build_examples': '예제만들기', 'files': 'ھۆججەت_تىزىم', 'java': '자바실행', 'run': 'ئىجرا_قىلىش_بۇيرۇق', 'path': 'يول', 'p': 'مەلۇمات_ئورۇنلاشتۇرۇش', 'readme': 'چۈشەندۈرۈش_ھۆججىتى', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'ئىزدەش_ئىندېكس', 'classes': 'تۈركۈم_يول', 'repo': '저장소경로', 'root': 'يىلتىز_ئادرېس', 'content': 'مەزمۇن_قىممىتى', 'source': '원본자료', 'name': 'ئاتى', 'target': 'نىشان', 'manifest': '꾸러미명세', 'language': 'تىل'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
