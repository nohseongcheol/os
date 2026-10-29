#!/usr/bin/env python3
"""기존 ara 호환 tāurunga_ira. tūturu_raraunga 구현: ../Ngā_Utauta/자바가상기계시험.py"""
import importlib as TAKE_uara
import sys as pūnaha_mahi_uara
from pathlib import Path as ara
pūnaha_mahi_uara.path.insert(0, str(ara(__file__).resolve().parents[1] / 'Ngā_Utauta'))
if __name__ == '__main__':
    import runpy as kaupapa_pūwhiri_taupānga
    kaupapa_pūwhiri_taupānga.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_uara.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'aho_raraunga', 'actual': 'tūturu_mēhua', 'match': '일치', 'payload': 'tino_raraunga_raraunga', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'whakahaere', 'ROOT': 'whakaatu_pūtake', 'text': 'Ngā_kupu', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'tauaha_ara', 'output': '출력결과', 'result': 'mēhua', 'cmd': '명령인수', 'name': 'Ingoa', 'jar': '자바꾸러미', 'report': 'whakamana_pūrongo', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
