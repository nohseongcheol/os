#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/실행파일시험.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('실행파일시험')
    대응 = {'out': 'পৰিমাপ_ডাটা', 'expected': '예상결과', 'phoff': 'এপ্প্_শিৰো_অফছেট', 'offset': 'অফছেট_মান', 'invalid': 'অবৈধ_ডাটা', 'path': 'পথ', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'পৰিমাপ', 'format_': 'সজ্জা_b87fd068', 'main': 'সঞ্চালন', 'content': 'সামগ্ৰী_মান', 'source': '원본자료', 'name': 'নাম', 'reference': 'তুলনা_আধাৰৰেখা', 'ROOT': '기준', 'value': 'মান', 'report': 'বৈধতা_ৰিপ_ৰ্ট'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
