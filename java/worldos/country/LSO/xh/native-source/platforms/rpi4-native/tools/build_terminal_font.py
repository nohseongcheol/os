#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/터미널글꼴빌드.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('터미널글꼴빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('터미널글꼴빌드')
    대응 = {'data': 'iingcombolo', 'img': 'umzobo_ixabiso', 'bits': '비트들', 'x': 'isilungelelanisi_x', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'indlela_uludwe', 'y': '세로좌표', 'main': 'Phumeza', 'src': '원본주소', 'fonts': 'ifonti_uludwe', 'ROOT': '기준', 'p': '자료위치', 'cp': 'ikharakhtha_ujiko_nkcukacha_zibe_ziikhowudi', 'target': 'ithagethi'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
