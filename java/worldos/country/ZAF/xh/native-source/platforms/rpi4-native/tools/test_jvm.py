#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/자바가상기계시험.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'uluhlu_lweekharektha_iingcombolo', 'actual': '실제결과', 'match': '일치', 'payload': 'umthwalo_wentlawulo_iingcombolo', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Phumeza', 'ROOT': '기준', 'text': 'Umbhalo', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'iklasi_indlela', 'output': '출력결과', 'result': '결과', 'cmd': '명령인수', 'name': 'Igama', 'jar': '자바꾸러미', 'report': 'uqinisekiso_ingxelo', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
