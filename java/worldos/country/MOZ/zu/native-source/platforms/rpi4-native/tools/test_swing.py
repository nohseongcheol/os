#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/화면요소시험.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('화면요소시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('화면요소시험')
    대응 = {'wait': '기다리기', 'x': 'okuxhumanisa_u_x', 's': 'uchunge_imininingwane', 'i': '순번', 'sel': 'isiqoki_a916db4e', 'seconds': '초단위', 'log': 'loga_umugqa', 'data': 'imininingwane', 'at': '현재위치', 'send': 'Thumela', 'main': 'Sebenzisa', 'req': '요청값', 'hot': 'ukunqamulela_inani', 'pump': 'isibambo_isigameko', 'ROOT': '기준', 'marker': '확인표시', 'b': '둘째값', 'command': 'Umlayelo', 'shell': 'isihumushi_miyalelo', 'f': 'ifayela_okufakwayo', 'click': 'qhafaza_inkinobho', 'k': '셋째순번', 'c': 'ikhodi_yohlamvu', 'r': '반환값', 'p': '자료위치', 'command_mode': 'umyalo_inqubo', 'end': 'yekisa_I_ofisethi', 'classes': 'uhlobo_umzila', 'key': '누름값', 'y': '세로좌표', 'result': '결과', 'report': 'ukufakazisa_umbiko', 'dest': '목적위치', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
