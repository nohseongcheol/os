#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/yenza_ifayela.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('yenza_ifayela', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('yenza_ifayela')
    대응 = {'timeout': '시간제한', 's': 'uchunge_imininingwane', 'i': '순번', 'match': '일치', 'files': 'ifayela_Uhlu', 'program': 'i_app', 'executable': '실행가능파일', 'args': 'i_agumenti_AMALUNGU_AFANAYO', 'chunk': '조각', 'data': 'imininingwane', 'proc': 'Inqubo', 'send': 'Thumela', 'main': 'Sebenzisa', 'marker': '확인표시', 'command': 'Umlayelo', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'yenza_umyalo', 'p': '자료위치', 'parser': '인수해석기', 'options': 'Izinketho', 'kind': 'umunxa_inani', 'selector': 'isiqoki', 'upload_data': 'layisha_imininingwane', 'end': 'yekisa_I_ofisethi', 'n': '개수', 'd': 'isikhumulo_imininingwane', 'key': '누름값', 'output': '출력결과', 'line': 'umugqa', 'name': 'Igama', 'upload_name': 'layisha_igama', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
