#!/usr/bin/env python3
"""기존 Indlela_2 호환 okufakwayo_iphoyinti. ulwazi_ngokwenzekile_imininingwane 구현: ../Amathuluzi/yenza_umyalo.py"""
import importlib as 가져오기
import sys as isistimu_yokusebenza_inani
from pathlib import Path as Indlela_2
isistimu_yokusebenza_inani.path.insert(0, str(Indlela_2(__file__).resolve().parents[1] / 'Amathuluzi'))
if __name__ == '__main__':
    import runpy as i_app_ikhabethe_le_app
    i_app_ikhabethe_le_app.run_module('yenza_umyalo', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('yenza_umyalo')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'sebenzisa_ideskithophu', 'main': 'Sebenzisa', 'host': 'singatha', 'status': 'isimo_inani', 'NetworkBridge': 'iNethiwekhi_ibhuloho', 'ROOT': '기준', 'bridge': 'ibhuloho', 'loader': '적재기', 'base': 'ngemuva_inani', 'options': 'Izinketho', 'binary': 'unambambili', 'args': 'i_agumenti_AMALUNGU_AFANAYO', 'command': 'Umlayelo'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
