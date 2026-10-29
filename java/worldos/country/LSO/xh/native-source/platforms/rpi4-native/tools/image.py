#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/yila_umfanekiso.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('yila_umfanekiso', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('yila_umfanekiso')
    대응 = {'total': '총량', 'start': 'Phumeza', 'firmware': '기초제어프로그램', 'files': 'ifayile_uludwe', 'archive_base': '압축기준', 'partition': 'ukwahlulwahlulwa_ifayile', 'archive': 'Uvimba', 'main': 'Phumeza', 'block': 'iingcombolo_thintela', 'ROOT': '기준', 'boot': '부팅경로', 'stage': 'umgangatho_ixabiso', 'out': '결과자료', 'expected': '예상결과', 'f': 'ifayile_ufako_nkcukacha', 'src': '원본주소', 'path': 'INDLELA', 'p': '자료위치', 'extracted': '추출자료', 'member': 'ilungu', 'mbr': '주부트기록', 'image': 'umfanekiso', 'sector_count': '섹터개수', 'dist': '배포경로', 'sha': '해시계산', 'license_': 'nikeza_ilayisensi', 'source': '원본자료', 'name': 'Igama', 'value': 'ixabiso', 'manifest': '꾸러미명세', 'dest': '목적위치', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
