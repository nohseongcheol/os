#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/실행파일시험.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('실행파일시험')
    대응 = {'out': 'miżura_data', 'expected': '예상결과', 'phoff': 'programm_Intestazzjoni_OFFSET', 'offset': 'OFFSET_VALUE', 'invalid': 'invalidu_data', 'path': 'mogħdija', 'executable': '실행가능파일', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'miżura', 'format_': 'format_b87fd068', 'main': 'serje', 'content': 'Kontenut_VALUE', 'source': '원본자료', 'name': 'isem', 'reference': '비교기준', 'ROOT': 'pprojetta_għerq', 'value': 'VALUE', 'report': 'validazzjoni_rapport'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
