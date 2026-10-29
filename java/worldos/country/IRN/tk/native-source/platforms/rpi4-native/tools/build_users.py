#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/düz_ulanyjy_ýer.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('düz_ulanyjy_ýer', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('düz_ulanyjy_ýer')
    대응 = {'mode': 'usul_reje', 'header': 'At_baha', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'Arhiw_gural', 'posix': '포직스경로', 'payload': 'ýük_gutujygy_maglumat', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'maglumat', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'Metin', 'headers': 'At_Sanaw', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'düz', 'build_users': 'döretmek_ulanyjy_ýer', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'programma_At_Süýşüriş', 'offset': 'Süýşüriş_baha', 'text_address': 'buýruk_salgy', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'ýerine_ýetir_buýruk', 'path': 'Ýol', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'Sazlamalar_baha', 'index': '색인', 'classes': 'klas_ýol', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'maglumat_salgy', 'symbol': 'nyşan_baha', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Ad', 'value': 'baha', 'fmt': 'format_932e03c8', 'work': '작업경로'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
