#!/usr/bin/env python3
"""기존 يول 호환 كىرگۈزۈش_نوقتا. ھەقىقىي_مەلۇمات 구현: ../قوراللار/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as مەشغۇلات_سىستېمىسى_قىممىتى
from pathlib import Path as يول
مەشغۇلات_سىستېمىسى_قىممىتى.path.insert(0, str(يول(__file__).resolve().parents[1] / 'قوراللار'))
if __name__ == '__main__':
    import runpy as ئەپ_خادىم
    ئەپ_خادىم.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': 'ئۆلچەم_مەلۇمات', 'builtins': '내장연산', 'header': 'بېشى_قىممىتى', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'ئىجرا_قىلىش_بۇيرۇق', 'flags': '설정비트', 'path': 'يول', 'p': 'مەلۇمات_ئورۇنلاشتۇرۇش', 'cc': '시언어번역기', 'obj': 'نىشان_ھۆججەت', 'flag': 'تەڭشەك_قىممىتى', 'ld': '연결편집기', 'objects': 'نىشان_ھۆججەت_417c7a10', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': 'يىلتىز_ئادرېس', 'assets': '탑재자료', 'source': '원본자료', 'name': 'ئاتى', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
