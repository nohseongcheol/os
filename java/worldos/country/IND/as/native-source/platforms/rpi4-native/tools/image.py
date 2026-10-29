#!/usr/bin/env python3
"""기존 পথ 호환 প্রবিষ্ট_পইণ্ট. প্ৰকৃত_ডাটা 구현: ../সঁজুলিসমূহ/ক্ৰিয়েট_ছবি.py"""
import importlib as 가져오기
import sys as অপাৰেটিং_ছিষ্টেম_মান
from pathlib import Path as পথ
অপাৰেটিং_ছিষ্টেম_মান.path.insert(0, str(পথ(__file__).resolve().parents[1] / 'সঁজুলিসমূহ'))
if __name__ == '__main__':
    import runpy as এপ্প্_এপ্প্_ড্ৰৱাৰ
    এপ্প্_এপ্প্_ড্ৰৱাৰ.run_module('ক্ৰিয়েট_ছবি', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ক্ৰিয়েট_ছবি')
    대응 = {'total': '총량', 'start': 'সঞ্চালন', 'firmware': '기초제어프로그램', 'files': 'ফাইল_সূচী', 'archive_base': '압축기준', 'partition': 'বিভাজন_ফাইল', 'archive': 'অভিলেখাগাৰ', 'main': 'সঞ্চালন', 'block': 'ডাটা_অৱৰুদ্ধ_কৰক', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'ষ্টেজ_মান', 'out': 'পৰিমাপ_ডাটা', 'expected': '예상결과', 'f': 'ফাইল_প্রবিষ্ট', 'src': '원본주소', 'path': 'পথ', 'p': 'ডাটা_স্থান_সলনি_কৰক', 'extracted': '추출자료', 'member': 'সদস্য', 'mbr': '주부트기록', 'image': 'ছবি', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'লাইচেঞ্চ', 'source': '원본자료', 'name': 'নাম', 'value': 'মান', 'manifest': '꾸러미명세', 'dest': 'গন্তব্য_স্থান_মান_স্থান_সলনি_কৰক', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
