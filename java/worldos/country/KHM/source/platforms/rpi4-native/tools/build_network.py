#!/usr/bin/env python3
"""기존 ផ្លូវ 호환 ការបញ្ចូល_ចំនុច. ដែលពិត_ទិន្នន័យ 구현: ../ឧបករណ៍/ចងក្រង_ណិតវឺក.py"""
import importlib as 가져오기
import sys as ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ
from pathlib import Path as ផ្លូវ
ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ.path.insert(0, str(ផ្លូវ(__file__).resolve().parents[1] / 'ឧបករណ៍'))
if __name__ == '__main__':
    import runpy as កម្មវិធី_ថត_កម្មវិធី
    កម្មវិធី_ថត_កម្មវិធី.run_module('ចងក្រង_ណិតវឺក', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ចងក្រង_ណិតវឺក')
    대응 = {'obj': 'ទិសដៅឯកសារ', 'objects': 'ទិសដៅ_ឯកសារ', 'library': 'បណ្ណាល័យ', 'output': '출력결과', 'port': 'លេខរន្ធ', 'root': 'ឬស_អ៊ីម៉ែល', 'files': 'ឯកសារ_បញ្ជី', 'source': '원본자료', 'run': 'អនុវត្ត_ពាក្យបញ្ជា', 'flags': 'ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ', 'path': 'ផ្លូវ', 'build_network': 'បង្កើត_ណិតវឺក', 'cc': '시언어번역기', 'ar': 'ប័ណ្ណសារ_ឧបករណ៏'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
