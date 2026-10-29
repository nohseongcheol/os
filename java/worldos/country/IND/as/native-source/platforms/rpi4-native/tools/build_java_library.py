#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'শিৰো_মান', 'sources': '원문목록', 'i': '순번', 'info': 'ছিষ্টেম_তথ্য', 'payload': 'প্লেল_ড_ডাটা', 'src': '원본주소', 'run': 'নিষ্পাদন_আদেশ', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'শ্ৰেণী_পথ', 'dist': '배포경로', 'archive': 'অভিলেখাগাৰ', 'output': '출력결과', 'root': 'ৰুট_ঠিকনা', 'name': 'নাম', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
