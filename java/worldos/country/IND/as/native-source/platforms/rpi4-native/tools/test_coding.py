#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/코딩시험.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('코딩시험')
    대응 = {'out': 'পৰিমাপ_ডাটা', 'expected': '예상결과', 'sdk': '개발꾸러미', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'সঞ্চালন', 'elf': '실행파일', 'run': 'নিষ্পাদন_আদেশ', 'name': 'নাম', 'path': 'পথ', 'p': 'ডাটা_স্থান_সলনি_কৰক', 'ROOT': '기준', 'report': 'বৈধতা_ৰিপ_ৰ্ট', 'args': 'যুক্তি_শৃঙ্খলা'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
