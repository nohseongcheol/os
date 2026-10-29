#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/되돌림시험서버.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('되돌림시험서버')
    대응 = {'data': 'iingcombolo', 'e': '보조항목', 'connection': 'uqhagamshelo_e05f319b', 'f': 'ifayile_ufako_nkcukacha', 'peer': 'untanga_ixabiso', 'self': '자신', 'udp': '전문제어', 't': '터미널항목', 'tcp': 'uqhagamshelo_isilawuli', 'EchoFixture': '되돌림시험서버', 'args': 'isiniki_myalelo_ULUHLU', 'chunk': '조각'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
