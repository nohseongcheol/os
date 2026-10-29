#!/usr/bin/env python3
"""기존 ọ̀nà 호환 ìgbéwọlé_kókó. gangan_détà 구현: ../Àwọn_irinṣẹ́/Ṣẹ̀dá_àwòrán.py"""
import importlib as 가져오기
import sys as OS_iye
from pathlib import Path as ọ̀nà
OS_iye.path.insert(0, str(ọ̀nà(__file__).resolve().parents[1] / 'Àwọn_irinṣẹ́'))
if __name__ == '__main__':
    import runpy as àtòjọ_ètò_aṣàfilọ́lẹ̀
    àtòjọ_ètò_aṣàfilọ́lẹ̀.run_module('Ṣẹ̀dá_àwòrán', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('Ṣẹ̀dá_àwòrán')
    대응 = {'total': '총량', 'start': 'Rọ́ọ̀nù', 'firmware': '기초제어프로그램', 'files': 'fáìlì_Àtòkọ', 'archive_base': '압축기준', 'partition': 'abala_àwo_àká_ọ̀rọ̀_fáìlì', 'archive': 'Ìpamọ_ọlọ́jọ́pípẹ́', 'main': 'Rọ́ọ̀nù', 'block': 'détà_sèdíwọ', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'ìpele_iye_29ee1bb7', 'out': '결과자료', 'expected': '예상결과', 'f': 'fáìlì_ìgbéwọlé', 'src': '원본주소', 'path': 'ọ̀nà', 'p': '자료위치', 'extracted': '추출자료', 'member': 'ọmọ_ẹgbẹ́', 'mbr': '주부트기록', 'image': 'àwòrán', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'ìgbaniláyè', 'source': '원본자료', 'name': 'Orúkọ', 'value': 'iye', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
