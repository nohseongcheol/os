#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/자바가상기계시험.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'ষ্ট্ৰিং_ডাটা', 'actual': 'প্ৰকৃত_পৰিমাপ', 'match': '일치', 'payload': 'প্লেল_ড_ডাটা', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'সঞ্চালন', 'ROOT': '기준', 'text': 'টেক্সট', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'শ্ৰেণী_পথ', 'output': '출력결과', 'result': 'পৰিমাপ', 'cmd': '명령인수', 'name': 'নাম', 'jar': '자바꾸러미', 'report': 'বৈধতা_ৰিপ_ৰ্ট', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
