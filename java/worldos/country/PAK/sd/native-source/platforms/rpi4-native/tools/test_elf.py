#!/usr/bin/env python3
"""기존 راههه 호환 داخلا_هنڌ. اصلي_ڪوائف 구현: ../اوزار/실행파일시험.py"""
import importlib as 가져오기
import sys as آپريٽنگ_سسٽم_قدر
from pathlib import Path as راههه
آپريٽنگ_سسٽم_قدر.path.insert(0, str(راههه(__file__).resolve().parents[1] / 'اوزار'))
if __name__ == '__main__':
    import runpy as ائپ_ائپ_ڊرائر
    ائپ_ائپ_ڊرائر.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': '결과자료', 'expected': '예상결과', 'phoff': 'ائپ_هيڊر_آف_سيٽ', 'offset': 'آف_سيٽ_قدر', 'invalid': 'ناجائز_ڪوائف', 'path': 'راههه', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': '결과', 'format_': 'وضع_b87fd068', 'main': 'هلائڻ', 'content': 'مواد_قدر', 'source': '원본자료', 'name': 'نالو', 'reference': '비교기준', 'ROOT': '기준', 'value': 'قدر', 'report': 'ڪارگر_رپورٽ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
