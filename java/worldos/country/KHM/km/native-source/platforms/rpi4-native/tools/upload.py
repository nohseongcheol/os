#!/usr/bin/env python3
"""기존 ផ្លូវ 호환 ការបញ្ចូល_ចំនុច. ដែលពិត_ទិន្នន័យ 구현: ../ឧបករណ៍/បង្ហោះ_ឯកសារ.py"""
import importlib as 가져오기
import sys as ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ
from pathlib import Path as ផ្លូវ
ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ.path.insert(0, str(ផ្លូវ(__file__).resolve().parents[1] / 'ឧបករណ៍'))
if __name__ == '__main__':
    import runpy as កម្មវិធី_ថត_កម្មវិធី
    កម្មវិធី_ថត_កម្មវិធី.run_module('បង្ហោះ_ឯកសារ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('បង្ហោះ_ឯកសារ')
    대응 = {'data': 'ទិន្នន័យ', 'i': '순번', 'name': 'ឈ្មោះ', 'c': 'កូដនៃតួអក្សរ', 'p': 'ទិន្នន័យ_កំណត់ទីតាំង', 'args': 'អាគុយម៉ង់_អារេ'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
