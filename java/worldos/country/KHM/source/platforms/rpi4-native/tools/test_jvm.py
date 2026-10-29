#!/usr/bin/env python3
"""기존 ផ្លូវ 호환 ការបញ្ចូល_ចំនុច. ដែលពិត_ទិន្នន័យ 구현: ../ឧបករណ៍/자바가상기계시험.py"""
import importlib as 가져오기
import sys as ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ
from pathlib import Path as ផ្លូវ
ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ.path.insert(0, str(ផ្លូវ(__file__).resolve().parents[1] / 'ឧបករណ៍'))
if __name__ == '__main__':
    import runpy as កម្មវិធី_ថត_កម្មវិធី
    កម្មវិធី_ថត_កម្មវិធី.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'សំនុំអក្សរ_ទិន្នន័យ', 'actual': 'ដែលពិត_ការវាស់វែង', 'match': '일치', 'payload': 'ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'រត់', 'ROOT': 'បញ្ចាំង_ឬស', 'text': 'អត្ថបទ', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'ថ្នាក់_ផ្លូវ', 'output': '출력결과', 'result': 'ការវាស់វែង', 'cmd': '명령인수', 'name': 'ឈ្មោះ', 'jar': '자바꾸러미', 'report': 'សុពលភាព_រាយការណ៍', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
