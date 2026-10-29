#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': 'পৰিমাপ_ডাটা', 'builtins': '내장연산', 'header': 'শিৰো_মান', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'নিষ্পাদন_আদেশ', 'flags': '설정비트', 'path': 'পথ', 'p': 'ডাটা_স্থান_সলনি_কৰক', 'cc': '시언어번역기', 'obj': 'গন্তব্য_ফাইল', 'flag': 'ছেটিংছ_মান', 'ld': '연결편집기', 'objects': 'গন্তব্য_স্থান_ফাইলসমূহ', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': 'ৰুট_ঠিকনা', 'assets': '탑재자료', 'source': '원본자료', 'name': 'নাম', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
