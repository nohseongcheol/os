#!/usr/bin/env python3
"""기존 ផ្លូវ 호환 ការបញ្ចូល_ចំនុច. ដែលពិត_ទិន្នន័យ 구현: ../ឧបករណ៍/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ
from pathlib import Path as ផ្លូវ
ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ.path.insert(0, str(ផ្លូវ(__file__).resolve().parents[1] / 'ឧបករណ៍'))
if __name__ == '__main__':
    import runpy as កម្មវិធី_ថត_កម្មវិធី
    កម្មវិធី_ថត_កម្មវិធី.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': 'ការវាស់វែង_ទិន្នន័យ', 'builtins': '내장연산', 'header': 'បឋមកថា_តំលៃ', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'អនុវត្ត_ពាក្យបញ្ជា', 'flags': 'ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ', 'path': 'ផ្លូវ', 'p': 'ទិន្នន័យ_កំណត់ទីតាំង', 'cc': '시언어번역기', 'obj': 'ទិសដៅឯកសារ', 'flag': 'ការកំណត់_តំលៃ', 'ld': '연결편집기', 'objects': 'ទិសដៅ_ឯកសារ', 'repo': 'ឃ្លាំង_ផ្ទុក_ផ្លូវ', 'v': '임시값', 'upstream': 'ប្រច្រាស់ទិស', 'root': 'ឬស_អ៊ីម៉ែល', 'assets': '탑재자료', 'source': '원본자료', 'name': 'ឈ្មោះ', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
