#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/예제빌드.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('예제빌드')
    대응 = {'out': 'miżura_data', 'build_examples': '예제만들기', 'files': 'fajl_Lista', 'java': '자바실행', 'run': 'eżegwixxa_kmand', 'path': 'mogħdija', 'p': 'data_pożizzjoni', 'readme': 'AQRANI', 'build_java_library': '자바라이브러리만들기', 'code': 'istruzzjoni_SEQUENCE', 'index': 'LOOKUP_INDEX', 'classes': 'klassi_mogħdija', 'repo': '저장소경로', 'root': 'għerq_ADDRESS', 'content': 'Kontenut_VALUE', 'source': '원본자료', 'name': 'isem', 'target': 'mira', 'manifest': '꾸러미명세', 'language': 'Lingwa'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
