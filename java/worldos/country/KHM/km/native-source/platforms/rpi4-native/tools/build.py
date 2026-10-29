#!/usr/bin/env python3
"""기존 ផ្លូវ 호환 ការបញ្ចូល_ចំនុច. ដែលពិត_ទិន្នន័យ 구현: ../ឧបករណ៍/ចងក្រង_ប្រព័ន្ធ.py"""
import importlib as 가져오기
import sys as ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ
from pathlib import Path as ផ្លូវ
ប្រព័ន្ធប្រតិបត្តិការណ៏_តំលៃ.path.insert(0, str(ផ្លូវ(__file__).resolve().parents[1] / 'ឧបករណ៍'))
if __name__ == '__main__':
    import runpy as កម្មវិធី_ថត_កម្មវិធី
    កម្មវិធី_ថត_កម្មវិធី.run_module('ចងក្រង_ប្រព័ន្ធ', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ចងក្រង_ប្រព័ន្ធ')
    대응 = {'network': 'ណិតវឺក', 'BUILD': 'ចងក្រង_ផ្លូវ', 'ar': 'ប័ណ្ណសារ_ឧបករណ៏', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'ពុម្ពអក្សរ_ទិន្នន័យ', 'flags': 'ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ', 'a': '첫째값', 'cc': '시언어번역기', 'args': 'អាគុយម៉ង់_អារេ', 'source_flags': '원본설정', 'ld': '연결편집기', 'method': 'វិធីសាស្រ្ត_ការបញ្ចូល', 'main': 'រត់', 'objcopy': 'វត្ថុ_ឯកសារ_អង្គបំលែង', 'ROOT': 'បញ្ចាំង_ឬស', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': '번역기', 'build_users': 'បង្កើត_អ្នកប្រើ_លំហ', 'f': 'ឯកសារ_ការបញ្ចូល', 'extra': '추가영역', 'exports': 'នាំចេញ_តារាង', 'jobs': '빌드작업', 'run': 'អនុវត្ត_ពាក្យបញ្ជា', 'path': 'ផ្លូវ', 'REPO': 'ឃ្លាំង_ផ្ទុក_ឬស', 'tool': 'ឧបករណ៍', 'classes': 'ថ្នាក់_ផ្លូវ', 'output': '출력결과', 'samples': '예제들', 'symbol': 'និមិត្ត_សញ្ញា_តំលៃ', 'source': '원본자료', 'name': 'ឈ្មោះ', 'build_network': 'បង្កើត_ណិតវឺក', 'font_info': 'ពុម្ពអក្សរ_ព័ត៌មាន', 'manifest': '꾸러미명세', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
