#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/yakha_isithombe.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('yakha_isithombe', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('yakha_isithombe')
    대응 = {'total': '총량', 'start': 'Sebenzisa', 'firmware': '기초제어프로그램', 'files': 'ifayela_Uhlu', 'archive_base': '압축기준', 'partition': 'ukwahlukanisa_ifayela', 'archive': 'londoloza', 'main': 'Sebenzisa', 'block': 'imininingwane_vimbela', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'isigaba_inani_29ee1bb7', 'out': '결과자료', 'expected': '예상결과', 'f': 'ifayela_okufakwayo', 'src': '원본주소', 'path': 'Indlela_2', 'p': '자료위치', 'extracted': '추출자료', 'member': 'ilungu', 'mbr': '주부트기록', 'image': 'isithombe', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'ilayisense', 'source': '원본자료', 'name': 'Igama', 'value': 'inani', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
