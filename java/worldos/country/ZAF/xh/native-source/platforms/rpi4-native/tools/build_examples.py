#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/예제빌드.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'ifayile_uludwe', 'java': '자바실행', 'run': 'ukwenza_umyalelo', 'path': 'INDLELA', 'p': '자료위치', 'readme': 'i_README', 'build_java_library': '자바라이브러리만들기', 'code': 'umyalelo_ULANDELELWANO', 'index': '색인', 'classes': 'iklasi_indlela', 'repo': '저장소경로', 'root': '뿌리주소', 'content': 'Isiqulatho_ixabiso', 'source': '원본자료', 'name': 'Igama', 'target': 'ithagethi', 'manifest': '꾸러미명세', 'language': 'Ulwimi'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
