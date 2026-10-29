#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'Iheda_ixabiso', 'sources': '원문목록', 'i': '순번', 'info': 'i_msinfo32_exe', 'payload': 'umthwalo_wentlawulo_iingcombolo', 'src': '원본주소', 'run': 'ukwenza_umyalelo', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'iklasi_indlela', 'dist': '배포경로', 'archive': 'Uvimba', 'output': '출력결과', 'root': '뿌리주소', 'name': 'Igama', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
