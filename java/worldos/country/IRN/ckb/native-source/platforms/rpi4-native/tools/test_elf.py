#!/usr/bin/env python3
"""기존 گوزەر 호환 تێنووسین_خاڵ. ڕاستەکی_دەیتا 구현: ../ئامرازەکان/실행파일시험.py"""
import importlib as 가져오기
import sys as سیستەمی_کارپێکردن_نرخ
from pathlib import Path as گوزەر
سیستەمی_کارپێکردن_نرخ.path.insert(0, str(گوزەر(__file__).resolve().parents[1] / 'ئامرازەکان'))
if __name__ == '__main__':
    import runpy as بەرنامە_ئەندامی_ستاف
    بەرنامە_ئەندامی_ستاف.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': '결과자료', 'expected': '예상결과', 'phoff': 'بەرنامە_سەرپەڕ_ئۆفسێت', 'offset': 'ئۆفسێت_نرخ', 'invalid': 'بێبایەخ_دەیتا', 'path': 'گوزەر', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': '결과', 'format_': 'بیچم_b87fd068', 'main': 'ڕادان', 'content': 'ناوەرۆک_نرخ', 'source': '원본자료', 'name': 'ناو', 'reference': '비교기준', 'ROOT': '기준', 'value': 'نرخ', 'report': 'ڕەواکردن_ڕاپۆرت'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
