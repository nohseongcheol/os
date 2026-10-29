#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/নিষ্পাদন_আদেশ.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('নিষ্পাদন_আদেশ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('নিষ্পাদন_আদেশ')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'চলন_ডেস্কটপ', 'main': 'সঞ্চালন', 'host': 'হ_ষ্ট', 'status': 'অৱস্থা_মান', 'NetworkBridge': 'নেটৱৰ্ক_ব্ৰীজ', 'ROOT': '기준', 'bridge': 'ব্ৰীজ', 'loader': '적재기', 'base': 'পটভূমি_মান', 'options': 'বিকল্প', 'binary': 'বাইনেৰি', 'args': 'যুক্তি_শৃঙ্খলা', 'command': 'কমান্ড'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
