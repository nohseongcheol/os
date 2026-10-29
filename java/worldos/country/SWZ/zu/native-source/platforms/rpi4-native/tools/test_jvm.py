#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/자바가상기계시험.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('자바가상기계시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바가상기계시험')
    대응 = {'message': '알림문', 's': 'uchunge_imininingwane', 'actual': '실제결과', 'match': '일치', 'payload': 'ukulayisha_okukhokhelwayo_imininingwane', 'cases': '시험사례', 'fixture': '시험자료', 'main': 'Sebenzisa', 'ROOT': '기준', 'text': 'Itekisi', 'valid': '유효함', 'includes': '포함인수', 'include': '포함항목', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': '완료량', 'classes': 'uhlobo_umzila', 'output': '출력결과', 'result': '결과', 'cmd': '명령인수', 'name': 'Igama', 'jar': '자바꾸러미', 'report': 'ukufakazisa_umbiko', 'tests': '시험목록'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
