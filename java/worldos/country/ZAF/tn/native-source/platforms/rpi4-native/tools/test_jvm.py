#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/자바가상기계시험.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'dikwalwa_tshedimosetso', 'actual': '실제결과', 'match': '일치', 'payload': 'selekanyo_sa_tshedimosetso_tshedimosetso', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'dirisa', 'ROOT': '기준', 'text': 'SMS', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'mofuta_tsela', 'output': '출력결과', 'result': '결과', 'cmd': '명령인수', 'name': 'leina', 'jar': '자바꾸러미', 'report': 'netefatso_pego', 'tests': '시험목록'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
