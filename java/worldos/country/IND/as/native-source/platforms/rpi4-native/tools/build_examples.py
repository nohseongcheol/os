#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/예제빌드.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'পৰিমাপ_ডাটা', 'build_examples': '예제만들기', 'files': 'ফাইল_সূচী', 'java': '자바실행', 'run': 'নিষ্পাদন_আদেশ', 'path': 'পথ', 'p': 'ডাটা_স্থান_সলনি_কৰক', 'readme': 'ৰিডমি_ফাইল', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'লুকআপ_ইনডেক্স', 'classes': 'শ্ৰেণী_পথ', 'repo': '저장소경로', 'root': 'ৰুট_ঠিকনা', 'content': 'সামগ্ৰী_মান', 'source': '원본자료', 'name': 'নাম', 'target': 'লক্ষ্য', 'manifest': '꾸러미명세', 'language': 'ভাষা'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
