#!/usr/bin/env python3
"""기존 RADA 호환 kirje_p. tegelik_andmed 구현: ../Tööriistad/järk_võrk.py"""
import importlib as TAKE_VALUE
import sys as operatsioonisüsteem_VALUE
from pathlib import Path as RADA
operatsioonisüsteem_VALUE.path.insert(0, str(RADA(__file__).resolve().parents[1] / 'Tööriistad'))
if __name__ == '__main__':
    import runpy as programm_käiviti
    programm_käiviti.run_module('järk_võrk', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('järk_võrk')
    vastendamine_VALUE = {'obj': 'sihtfail', 'objects': 'sihtkoht_Failid', 'library': 'teek', 'output': 'toodang', 'port': 'pordinumber', 'root': 'juur_ADDRESS', 'files': 'Fail_Loend', 'source': '원본자료', 'run': 'Täida_käsk', 'flags': 'konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus', 'path': 'RADA', 'build_network': 'avama_võrk_48d29d6d', 'cc': '_15_kompilaator', 'ar': 'Arhiiv_tööriist'}
    for 이전, tähtaja_piires_kaup in vastendamine_VALUE.items():
        if hasattr(구현, tähtaja_piires_kaup): globals()[이전] = getattr(구현, tähtaja_piires_kaup)
