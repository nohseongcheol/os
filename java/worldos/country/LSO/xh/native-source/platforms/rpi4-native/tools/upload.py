#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/layisha_Iifayile.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('layisha_Iifayile', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('layisha_Iifayile')
    대응 = {'data': 'iingcombolo', 'i': '순번', 'name': 'Igama', 'c': 'ikhowudi_yekharakhtha', 'p': '자료위치', 'args': 'isiniki_myalelo_ULUHLU'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
