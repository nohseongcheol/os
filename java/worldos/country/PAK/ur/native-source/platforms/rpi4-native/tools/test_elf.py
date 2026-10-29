#!/usr/bin/env python3
"""기존 راستہ_2 호환 اندراج_نقطہ. اصل_کوائف 구현: ../ٹولز/실행파일시험.py"""
import importlib as 가져오기
import sys as آپریٹنگ_سسٹم_قدر
from pathlib import Path as راستہ_2
آپریٹنگ_سسٹم_قدر.path.insert(0, str(راستہ_2(__file__).resolve().parents[1] / 'ٹولز'))
if __name__ == '__main__':
    import runpy as ایپ_ایپ_دراز
    ایپ_ایپ_دراز.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'پیمائش_کوائف', 'expected': '예상결과', 'phoff': 'ایپ_سرصفحہ_آفسٹ', 'offset': 'آفسٹ_قدر', 'invalid': 'بے_جواز_کوائف', 'path': 'راستہ_2', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'پیمائش', 'format_': 'وضع_b87fd068', 'main': 'چلائیں', 'content': 'مشمول_قدر', 'source': '원본자료', 'name': 'نام', 'reference': '비교기준', 'ROOT': 'عکس_ڈالنا_روٹ', 'value': 'قدر', 'report': 'توثیق_رپورٹ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
