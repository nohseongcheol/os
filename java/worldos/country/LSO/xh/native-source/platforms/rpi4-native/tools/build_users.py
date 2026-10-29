#!/usr/bin/env python3
"""기존 INDLELA 호환 ufako_nkcukacha_inqaku. eyona_yenzekileyo_iingcombolo 구현: ../Izixhobo/yakha_umsebenzisi_isithuba.py"""
import importlib as 가져오기
import sys as Indlela_yokusebenza_ixabiso
from pathlib import Path as INDLELA
Indlela_yokusebenza_ixabiso.path.insert(0, str(INDLELA(__file__).resolve().parents[1] / 'Izixhobo'))
if __name__ == '__main__':
    import runpy as inkqubo_idrowa_yosetyenziso
    inkqubo_idrowa_yosetyenziso.run_module('yakha_umsebenzisi_isithuba', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('yakha_umsebenzisi_isithuba')
    대응 = {'mode': 'imethodi_imo', 'header': 'Iheda_ixabiso', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Uvimba_isixhobo_sokutayipha', 'posix': '포직스경로', 'payload': 'umthwalo_wentlawulo_iingcombolo', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'iingcombolo', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'Umbhalo', 'headers': 'Iheda_uludwe', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'yakha', 'build_users': 'yila_umsebenzisi_isithuba', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'inkqubo_Iheda_Ukulinganisa', 'offset': 'Ukulinganisa_ixabiso', 'text_address': 'umyalelo_idilesi', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'ukwenza_umyalelo', 'path': 'INDLELA', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'Iisetingi_ixabiso', 'index': '색인', 'classes': 'iklasi_indlela', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'iingcombolo_idilesi', 'symbol': 'isimboli_ixabiso', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Igama', 'value': 'ixabiso', 'fmt': 'ifomathi', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
