#!/usr/bin/env python3
"""기존 yo_l 호환 kiritish_nuqta. real_ma_lumotlar 구현: ../Vositalar/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as operatsion_tizim_VALUE
from pathlib import Path as yo_l
operatsion_tizim_VALUE.path.insert(0, str(yo_l(__file__).resolve().parents[1] / 'Vositalar'))
if __name__ == '__main__':
    import runpy as ilova_ilovalar_paneli
    ilova_ilovalar_paneli.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'satr_ma_lumotlar', 'actual': 'real_o_lchov', 'match': '일치', 'payload': 'foydali_yuklanma_ma_lumotlar', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Bajarish', 'ROOT': 'Project_ildiz', 'text': 'Matn', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'Sinf_yo_l', 'output': '출력결과', 'result': 'o_lchov', 'cmd': '명령인수', 'name': 'Nomi', 'jar': '자바꾸러미', 'report': 'tasdiq_hisobot', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
