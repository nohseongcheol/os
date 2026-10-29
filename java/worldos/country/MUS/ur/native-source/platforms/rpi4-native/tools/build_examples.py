#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/예제빌드.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'پیمائش_کوائف', 'build_examples': '예제만들기', 'files': 'فائل_فہرست', 'java': '자바실행', 'run': 'نفاذ_کریں_حکم', 'path': 'راستہ_2', 'p': 'کوائف_پوزیشن_ٹھیک_کریں', 'readme': 'مجھے_پڑھیں', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'لُک_اپ_اشاریہ', 'classes': 'صنف_راہ', 'repo': '저장소경로', 'root': 'روٹ_پتہ', 'content': 'مشمول_قدر', 'source': '원본자료', 'name': 'نام', 'target': 'ہدف', 'manifest': '꾸러미명세', 'language': 'زبان'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
