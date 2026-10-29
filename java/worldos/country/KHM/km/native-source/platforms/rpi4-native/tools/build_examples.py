#!/usr/bin/env python3
"""기존 ផ្លូវ 호환 ការបញ្ចូល_ចំនុច. ដែលពិត_ទិន្នន័យ 구현: ../ឧបករណ៍/예제빌드.py"""
import importlib as 가져오기
import sys as ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ
from pathlib import Path as ផ្លូវ
ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ.path.insert(0, str(ផ្លូវ(__file__).resolve().parents[1] / 'ឧបករណ៍'))
if __name__ == '__main__':
    import runpy as កម្មវិធី_ថត_កម្មវិធី
    កម្មវិធី_ថត_កម្មវិធី.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': 'ការវាស់វែង_ទិន្នន័យ', 'build_examples': '예제만들기', 'files': 'ឯកសារ_បញ្ជី', 'java': '자바실행', 'run': 'អនុវត្ត_ពាក្យបញ្ជា', 'path': 'ផ្លូវ', 'p': 'ទិន្នន័យ_កំណត់ទីតាំង', 'readme': 'អានខ្ញុំ', 'build_java_library': '자바라이브러리만들기', 'code': '명령열', 'index': 'រុករក_សន្ទស្សន៏', 'classes': 'ថ្នាក់_ផ្លូវ', 'repo': 'ឃ្លាំង_ផ្ទុក_ផ្លូវ', 'root': 'ឬស_អ៊ីម៉ែល', 'content': 'មាតិកា_តំលៃ', 'source': '원본자료', 'name': 'ឈ្មោះ', 'target': 'គោលដៅ', 'manifest': '꾸러미명세', 'language': 'ភាសា'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
