#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/시언어번역기빌드.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('시언어번역기빌드')
    대응 = {'out': 'miżura_data', 'builtins': '내장연산', 'header': 'Intestazzjoni_VALUE', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'eżegwixxa_kmand', 'flags': '설정비트', 'path': 'mogħdija', 'p': 'data_pożizzjoni', 'cc': '시언어번역기', 'obj': 'fajl_tad_destinazzjoni', 'flag': 'Settings_VALUE', 'ld': '연결편집기', 'objects': 'destinazzjoni_Fajls', 'repo': '저장소경로', 'v': '임시값', 'upstream': '외부원문', 'root': 'għerq_ADDRESS', 'assets': '탑재자료', 'source': '원본자료', 'name': 'isem', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
