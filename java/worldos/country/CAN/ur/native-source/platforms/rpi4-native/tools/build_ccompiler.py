#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': 'پیمائش_کوائف', 'builtins': '내장연산', 'header': 'سرصفحہ_قدر', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'نفاذ_کریں_حکم', 'flags': '설정비트', 'path': 'راستہ_2', 'p': 'کوائف_پوزیشن_ٹھیک_کریں', 'cc': '시언어번역기', 'obj': 'مقصود_فائل', 'flag': 'سیٹنگز_قدر', 'ld': '연결편집기', 'objects': 'منزل_مقصود_فائلیں', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': 'روٹ_پتہ', 'assets': '탑재자료', 'source': '원본자료', 'name': 'نام', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
