#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/বিল্ড_ব্যৱহাৰকৰ্তা_স্থান.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('বিল্ড_ব্যৱহাৰকৰ্তা_স্থান', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('বিল্ড_ব্যৱহাৰকৰ্তা_স্থান')
    대응 = {'mode': 'পদ্ধতি_মোড', 'header': 'শিৰো_মান', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'অভিলেখাগাৰ_সঁজুলি', 'posix': '포직스경로', 'payload': 'প্লেল_ড_ডাটা', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'ডাটা', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'টেক্সট', 'headers': 'শিৰো_সূচী', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'বিল্ড', 'build_users': 'ক্ৰিয়েট_ব্যৱহাৰকৰ্তা_স্থান', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'এপ্প্_শিৰো_অফছেট', 'offset': 'অফছেট_মান', 'text_address': 'আদেশ_ঠিকনা', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'নিষ্পাদন_আদেশ', 'path': 'পথ', 'p': 'ডাটা_স্থান_সলনি_কৰক', 'changed': '바뀐자료', 'n': '개수', 'flag': 'ছেটিংছ_মান', 'index': 'লুকআপ_ইনডেক্স', 'classes': 'শ্ৰেণী_পথ', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'ডাটা_ঠিকনা', 'symbol': 'প্ৰতীক_মান', 'root': 'ৰুট_ঠিকনা', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'নাম', 'value': 'মান', 'fmt': 'সজ্জা_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
