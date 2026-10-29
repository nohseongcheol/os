#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/বিল্ড_ছিষ্টেম.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('বিল্ড_ছিষ্টেম', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('বিল্ড_ছিষ্টেম')
    대응 = {'network': 'নেটৱৰ্ক', 'BUILD': 'বিল্ড_পথ', 'ar': 'অভিলেখাগাৰ_সঁজুলি', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'ফ_ন্ট_ডাটা', 'flags': '설정비트', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'যুক্তি_শৃঙ্খলা', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'পদ্ধতি_প্রবিষ্ট', 'main': 'সঞ্চালন', 'objcopy': 'অবজেক্ট_ফাইল_কনভাৰ্টাৰ', 'ROOT': '기준', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'ক্ৰিয়েট_ব্যৱহাৰকৰ্তা_স্থান', 'f': 'ফাইল_প্রবিষ্ট', 'extra': '추가영역', 'exports': 'ৰপ্তানি_কৰক_তালিকা', 'jobs': '빌드작업', 'run': 'নিষ্পাদন_আদেশ', 'path': 'পথ', 'REPO': '저장소', 'tool': 'সঁজুলিসমূহ', 'classes': 'শ্ৰেণী_পথ', 'output': '출력결과', 'samples': '예제들', 'symbol': 'প্ৰতীক_মান', 'source': '원본자료', 'name': 'নাম', 'build_network': 'ক্ৰিয়েট_নেটৱৰ্ক', 'font_info': 'ফ_ন্ট_তথ্য', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
