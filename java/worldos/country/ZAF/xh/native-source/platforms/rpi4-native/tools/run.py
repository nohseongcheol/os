#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/ukwenza_umyalelo.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('ukwenza_umyalelo', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('ukwenza_umyalelo')
    대응 = {'supported': '지원목록', 'parser': '인수해석기', 'qemu': '모의기계', 'run_desktop': 'i_run_idesktophu', 'main': 'Phumeza', 'host': 'umsingathi', 'status': 'imo_ixabiso', 'NetworkBridge': 'Inethiwekhi_ibhulorho', 'ROOT': '기준', 'bridge': 'ibhulorho', 'loader': '적재기', 'base': 'Ngasemva_ixabiso', 'options': 'uKhetho', 'binary': 'ibhayinari', 'args': 'isiniki_myalelo_ULUHLU', 'command': 'Umyalelo'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
