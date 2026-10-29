#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/예제빌드.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'فایل_لیست', 'java': '자바실행', 'run': 'جێبەجێکردن_فەرمان', 'path': 'گوزەر', 'p': '자료위치', 'readme': 'رێخۆشکەر', 'build_java_library': '자바라이브러리만들기', 'code': 'ڕێنمایی_زنجیره', 'index': '색인', 'classes': 'کلاس_گوزەر', 'repo': '저장소경로', 'root': '뿌리주소', 'content': 'ناوەرۆک_نرخ', 'source': '원본자료', 'name': 'ناو', 'target': 'مەبەست', 'manifest': '꾸러미명세', 'language': 'زمان'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
