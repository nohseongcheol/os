#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/예제빌드.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'فائل_فهرست', 'java': '자바실행', 'run': 'تعميل_ڪرڻ_حڪم', 'path': 'راههه', 'p': '자료위치', 'readme': 'پڙهو_فائل', 'build_java_library': '자바라이브러리만들기', 'code': 'هدايت_ترتيب', 'index': '색인', 'classes': 'درجو_راههه', 'repo': '저장소경로', 'root': '뿌리주소', 'content': 'مواد_قدر', 'source': '원본자료', 'name': 'نالو', 'target': 'هدف', 'manifest': '꾸러미명세', 'language': 'ٻولي'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
