#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'سرصفحہ_قدر', 'sources': '원문목록', 'i': '순번', 'info': 'نظام_کی_معلومات', 'payload': 'پے_لوڈ_کوائف', 'src': '원본주소', 'run': 'نفاذ_کریں_حکم', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'صنف_راہ', 'dist': '배포경로', 'archive': 'محفوظ', 'output': '출력결과', 'root': 'روٹ_پتہ', 'name': 'نام', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
