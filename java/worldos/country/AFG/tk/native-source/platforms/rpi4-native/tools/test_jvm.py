#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/자바가상기계시험.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'setir_maglumat', 'actual': '실제결과', 'match': '일치', 'payload': 'ýük_gutujygy_maglumat', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Bitir', 'ROOT': '기준', 'text': 'Metin', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'klas_ýol', 'output': '출력결과', 'result': '결과', 'cmd': '명령인수', 'name': 'Ad', 'jar': '자바꾸러미', 'report': 'barlag_hasabat', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
