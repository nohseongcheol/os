#!/usr/bin/env python3
"""기존 ផ្លូវ 호환 ការបញ្ចូល_ចំនុច. ដែលពិត_ទិន្នន័យ 구현: ../ឧបករណ៍/បង្កើត_រូបថត.py"""
import importlib as 가져오기
import sys as ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ
from pathlib import Path as ផ្លូវ
ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ.path.insert(0, str(ផ្លូវ(__file__).resolve().parents[1] / 'ឧបករណ៍'))
if __name__ == '__main__':
    import runpy as កម្មវិធី_ថត_កម្មវិធី
    កម្មវិធី_ថត_កម្មវិធី.run_module('បង្កើត_រូបថត', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('បង្កើត_រូបថត')
    대응 = {'total': '총량', 'start': 'រត់', 'firmware': '기초제어프로그램', 'files': 'ឯកសារ_បញ្ជី', 'archive_base': '압축기준', 'partition': 'បំណែក_ឯកសារ', 'archive': 'ប័ណ្ណសារ', 'main': 'រត់', 'block': 'ទិន្នន័យ_ប្លុក', 'ROOT': 'បញ្ចាំង_ឬស', 'boot': '부팅경로', 'stage': 'ឆាក_តំលៃ', 'out': 'ការវាស់វែង_ទិន្នន័យ', 'expected': '예상결과', 'f': 'ឯកសារ_ការបញ្ចូល', 'src': '원본주소', 'path': 'ផ្លូវ', 'p': 'ទិន្នន័យ_កំណត់ទីតាំង', 'extracted': '추출자료', 'member': 'សមាជិក', 'mbr': '주부트기록', 'image': 'រូបថត', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'ផ្ដល់_អាជ្ញាបណ្ណ', 'source': '원본자료', 'name': 'ឈ្មោះ', 'value': 'តំលៃ', 'manifest': '꾸러미명세', 'dest': 'ទិសដៅ_តំលៃ_កំណត់ទីតាំង', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
