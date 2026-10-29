#!/usr/bin/env python3
"""기존 راہ 호환 داخلہ_مقام. اصلی_کوائف 구현: ../اوزار/예제빌드.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راہ
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راہ(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ایپ_عملے_دا_رکن
    ایپ_عملے_دا_رکن.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'فائل_فرست', 'java': '자바실행', 'run': 'نفاذ_کرو_حکم', 'path': 'راہ', 'p': '자료위치', 'readme': 'فائل_مینوں_پڑھو', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': '색인', 'classes': 'درجہ_راہ', 'repo': '저장소경로', 'root': '뿌리주소', 'content': 'اجزاء_قدر', 'source': '원본자료', 'name': 'ناں', 'target': 'ہدف', 'manifest': '꾸러미명세', 'language': 'زبان'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
