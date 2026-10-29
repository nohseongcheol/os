#!/usr/bin/env python3
"""기존 ផ្លូវ 호환 ការបញ្ចូល_ចំនុច. ដែលពិត_ទិន្នន័យ 구현: ../ឧបករណ៍/អនុវត្ត_ឯកសារ.py"""
import importlib as 가져오기
import sys as ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ
from pathlib import Path as ផ្លូវ
ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ.path.insert(0, str(ផ្លូវ(__file__).resolve().parents[1] / 'ឧបករណ៍'))
if __name__ == '__main__':
    import runpy as កម្មវិធី_ថត_កម្មវិធី
    កម្មវិធី_ថត_កម្មវិធី.run_module('អនុវត្ត_ឯកសារ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('អនុវត្ត_ឯកសារ')
    대응 = {'timeout': '시간제한', 's': 'សំនុំអក្សរ_ទិន្នន័យ', 'i': '순번', 'match': '일치', 'files': 'ឯកសារ_បញ្ជី', 'program': 'កម្មវិធី', 'executable': '실행가능파일', 'args': 'អាគុយម៉ង់_អារេ', 'chunk': '조각', 'data': 'ទិន្នន័យ', 'proc': 'ដំណើរការ', 'send': 'ផ្ញើ', 'main': 'រត់', 'marker': '확인표시', 'command': 'ពាក្យ_បញ្ជា', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'អនុវត្ត_ពាក្យបញ្ជា', 'p': 'ទិន្នន័យ_កំណត់ទីតាំង', 'parser': 'មុខងារ_ញែក', 'options': 'ជំរើស', 'kind': 'ប្រភេទ_តំលៃ', 'selector': 'អ្នកជ្រើសរើស', 'upload_data': 'បង្ហោះ_ទិន្នន័យ', 'end': 'បញ្ចប់_ការបែង_ភាគ', 'n': '개수', 'd': 'ទិសដៅ_ទិន្នន័យ', 'key': '누름값', 'output': '출력결과', 'line': 'បន្ទាត់', 'name': 'ឈ្មោះ', 'upload_name': 'បង្ហោះ_ឈ្មោះ', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
