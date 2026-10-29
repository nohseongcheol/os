#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/বিল্ড_টাৰ্মিনেল_ফ_ন্ট.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('বিল্ড_টাৰ্মিনেল_ফ_ন্ট', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('বিল্ড_টাৰ্মিনেল_ফ_ন্ট')
    대응 = {'data': 'ডাটা', 'img': 'অংকন_মান', 'bits': '비트들', 'x': 'x_ক_ৰ্ডিনেট', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'পথ_সূচী', 'y': '세로좌표', 'main': 'সঞ্চালন', 'src': '원본주소', 'fonts': 'ফ_ন্ট_সূচী', 'ROOT': '기준', 'p': 'ডাটা_স্থান_সলনি_কৰক', 'cp': 'বৰ্ণ_এনকোডিং', 'target': 'লক্ষ্য'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
