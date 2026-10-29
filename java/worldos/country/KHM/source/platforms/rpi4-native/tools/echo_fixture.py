#!/usr/bin/env python3
"""기존 ផ្លូវ 호환 ការបញ្ចូល_ចំនុច. ដែលពិត_ទិន្នន័យ 구현: ../ឧបករណ៍/되돌림시험서버.py"""
import importlib as 가져오기
import sys as ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ
from pathlib import Path as ផ្លូវ
ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ.path.insert(0, str(ផ្លូវ(__file__).resolve().parents[1] / 'ឧបករណ៍'))
if __name__ == '__main__':
    import runpy as កម្មវិធី_ថត_កម្មវិធី
    កម្មវិធី_ថត_កម្មវិធី.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'ទិន្នន័យ', 'e': '보조항목', 'connection': 'ការភ្ជាប់_e05f319b', 'f': 'ឯកសារ_ការបញ្ចូល', 'peer': 'សិទ្ធស្មើ_តំលៃ', 'self': '자신', 'udp': '전문제어', 't': 'ធើមីណល_ការបញ្ចូល', 'tcp': 'ការភ្ជាប់_អង្គបញ្ជា', 'EchoFixture': '되돌림시험서버', 'args': 'អាគុយម៉ង់_អារេ', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
