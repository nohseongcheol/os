#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/বিল্ড_নেটৱৰ্ক.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('বিল্ড_নেটৱৰ্ক', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('বিল্ড_নেটৱৰ্ক')
    대응 = {'obj': 'গন্তব্য_ফাইল', 'objects': 'গন্তব্য_স্থান_ফাইলসমূহ', 'library': 'লাইব্ৰেৰী', 'output': '출력결과', 'port': '접속번호', 'root': 'ৰুট_ঠিকনা', 'files': 'ফাইল_সূচী', 'source': '원본자료', 'run': 'নিষ্পাদন_আদেশ', 'flags': '설정비트', 'path': 'পথ', 'build_network': 'ক্ৰিয়েট_নেটৱৰ্ক', 'cc': '시언어번역기', 'ar': 'অভিলেখাগাৰ_সঁজুলি'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
