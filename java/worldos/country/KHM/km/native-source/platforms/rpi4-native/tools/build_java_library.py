#!/usr/bin/env python3
"""기존 ផ្លូវ 호환 ការបញ្ចូល_ចំនុច. ដែលពិត_ទិន្នន័យ 구현: ../ឧបករណ៍/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ
from pathlib import Path as ផ្លូវ
ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ.path.insert(0, str(ផ្លូវ(__file__).resolve().parents[1] / 'ឧបករណ៍'))
if __name__ == '__main__':
    import runpy as កម្មវិធី_ថត_កម្មវិធី
    កម្មវិធី_ថត_កម្មវិធី.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'បឋមកថា_តំលៃ', 'sources': '원문목록', 'i': '순번', 'info': 'ប្រព័ន្ធព័ត៌មាន', 'payload': 'ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ', 'src': '원본주소', 'run': 'អនុវត្ត_ពាក្យបញ្ជា', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'ថ្នាក់_ផ្លូវ', 'dist': '배포경로', 'archive': 'ប័ណ្ណសារ', 'output': '출력결과', 'root': 'ឬស_អ៊ីម៉ែល', 'name': 'ឈ្មោះ', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
