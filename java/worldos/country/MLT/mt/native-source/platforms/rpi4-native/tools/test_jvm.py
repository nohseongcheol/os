#!/usr/bin/env python3
"""기존 mogħdija 호환 entrata_punt. attwali_data 구현: ../Għodod/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as sistema_operattiva_VALUE
from pathlib import Path as mogħdija
sistema_operattiva_VALUE.path.insert(0, str(mogħdija(__file__).resolve().parents[1] / 'Għodod'))
if __name__ == '__main__':
    import runpy as programm_ġabra_ta_apps
    programm_ġabra_ta_apps.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'string_data', 'actual': 'attwali_miżura', 'match': '일치', 'payload': 'payload_data', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'serje', 'ROOT': 'pprojetta_għerq', 'text': 'SMS', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'klassi_mogħdija', 'output': '출력결과', 'result': 'miżura', 'cmd': '명령인수', 'name': 'isem', 'jar': '자바꾸러미', 'report': 'validazzjoni_rapport', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
