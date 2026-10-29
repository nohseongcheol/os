#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/avama_pilt.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('avama_pilt', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('avama_pilt')
    vastendamine_VALUE = {'total': 'kokku_võimsus', 'start': 'Käivita_2', 'firmware': 'püsivara_VALUE', 'files': 'Fail_Loend', 'archive_base': 'Arhiiv_BASE', 'partition': 'sektsioon_Fail', 'archive': 'Arhiiv', 'main': 'Käivita_2', 'block': 'andmeplokk', 'ROOT': 'Project_juur', 'boot': '부팅경로', 'stage': 'etapp_VALUE', 'out': 'näitaja_andmed', 'expected': '예상결과', 'f': 'Fail_kirje', 'src': '원본주소', 'path': 'RADA', 'p': 'andmed_ametikoht', 'extracted': '추출자료', 'member': 'liige', 'mbr': 'MBR', 'image': 'pilt', 'sector_count': '섹터개수', 'dist': 'turustus_tee', 'sha': '해시계산', 'license_': 'litsents', 'source': '원본자료', 'name': 'Nimi_2', 'value': 'VALUE', 'manifest': '꾸러미명세', 'dest': 'sihtkoht_VALUE_ametikoht', 'work': '작업경로'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
