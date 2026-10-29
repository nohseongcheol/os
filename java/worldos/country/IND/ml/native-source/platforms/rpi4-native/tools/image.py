#!/usr/bin/env python3
"""기존 വഴി 호환 എന്_ട്രി_പോയിന്_റ്. വാസ്തവമായ_ഡാറ്റാ 구현: ../ഉപകരണങ്ങൾ/സൃഷ്_ടിക്കുക_ഇമേജ്.py"""
import importlib as 가져오기
import sys as ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം
from pathlib import Path as വഴി
ഓപ്പറേറ്റിംഗ്_സിസ്റ്റം_മൂല്യം.path.insert(0, str(വഴി(__file__).resolve().parents[1] / 'ഉപകരണങ്ങൾ'))
if __name__ == '__main__':
    import runpy as പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ
    പ്രോഗ്രാം_ആപ്പ്_ഡ്രോയർ.run_module('സൃഷ്_ടിക്കുക_ഇമേജ്', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('സൃഷ്_ടിക്കുക_ഇമേജ്')
    대응 = {'total': '총량', 'start': 'നടപ്പിലാക്കുക', 'firmware': '기초제어프로그램', 'files': 'ഫയല്_ലിസ്റ്റ്', 'archive_base': '압축기준', 'partition': 'വിഭജനം_ഫയല്', 'archive': 'ശേഖരം', 'main': 'നടപ്പിലാക്കുക', 'block': 'ഡാറ്റാ_തടയുക', 'ROOT': 'പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം', 'boot': '부팅경로', 'stage': 'വേദി_മൂല്യം', 'out': 'അളവ്_ഡാറ്റാ', 'expected': '예상결과', 'f': 'ഫയല്_എന്_ട്രി', 'src': '원본주소', 'path': 'വഴി', 'p': 'ഡാറ്റാ_പദവി', 'extracted': '추출자료', 'member': 'അംഗം', 'mbr': '주부트기록', 'image': 'ഇമേജ്', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'ലൈസൻസ്', 'source': '원본자료', 'name': 'പേരു്', 'value': 'മൂല്യം', 'manifest': 'ബണ്ടിൽ_ആവിഷ്കാരം', 'dest': 'ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം_പദവി', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
