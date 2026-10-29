#!/usr/bin/env python3
"""기존 Cığır 호환 daxiletmə_p. faktiki_verilənlər 구현: ../Alətlər/자바가상기계시험.py"""
import importlib as TAKE_VALUE
import sys as əməliyyat_sistemi_VALUE
from pathlib import Path as Cığır
əməliyyat_sistemi_VALUE.path.insert(0, str(Cığır(__file__).resolve().parents[1] / 'Alətlər'))
if __name__ == '__main__':
    import runpy as proqram_işəsalma
    proqram_işəsalma.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'sətir_verilənlər', 'actual': 'faktiki_ölçü', 'match': '일치', 'payload': 'faydalı_yük_verilənlər', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'İcra_Et', 'ROOT': 'Project_kök', 'text': 'Mətn', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'Sinif_yol', 'output': '출력결과', 'result': 'ölçü', 'cmd': '명령인수', 'name': 'Ad', 'jar': '자바꾸러미', 'report': 'yoxlama_hesabat', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
