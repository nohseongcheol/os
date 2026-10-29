#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'Unhlokweni_inani', 'sources': '원문목록', 'i': '순번', 'info': 'I_msinfo32_exe', 'payload': 'ukulayisha_okukhokhelwayo_imininingwane', 'src': '원본주소', 'run': 'yenza_umyalo', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'uhlobo_umzila', 'dist': '배포경로', 'archive': 'londoloza', 'output': '출력결과', 'root': '뿌리주소', 'name': 'Igama', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
