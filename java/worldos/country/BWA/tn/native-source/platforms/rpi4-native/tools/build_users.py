#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/aga_modirisi_sebaka.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('aga_modirisi_sebaka', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('aga_modirisi_sebaka')
    대응 = {'mode': 'mokgwa_mokgwa', 'header': 'setlhogo_Boleng', 'i': '순번', 'build_ccompiler': '시언어번역기만들기', 'ar': 'boloka_sediriswa', 'posix': '포직스경로', 'payload': 'selekanyo_sa_tshedimosetso_tshedimosetso', 'flags': '설정비트', 'cases': '시험사례', 'cc': '시언어번역기', 'data': 'tshedimosetso', 'build_java_library': '자바라이브러리만들기', 'ld': '연결편집기', 'repo': '저장소경로', 'build_python': '파이썬만들기', 'inc': '포함경로', 'argument': '전달값', 'text': 'SMS', 'headers': 'setlhogo_lenaane', 'cxx': '시플플번역기', 'valid': '유효함', 'build': 'aga', 'build_users': 'tlhama_modirisi_sebaka', 'compiler': '번역기', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'Tiriso_setlhogo_Baya_ka_Tekatekanyo', 'offset': 'Baya_ka_Tekatekanyo_Boleng', 'text_address': 'Taelo_aterese', 'abi': '호출규약', 'assembly': '어셈블리자료', 'run': 'diragatsa_Taelo', 'path': 'tsela', 'p': '자료위치', 'changed': '바뀐자료', 'n': '개수', 'flag': 'Diseting_Boleng', 'index': '색인', 'classes': 'mofuta_tsela', 'output': '출력결과', 'loads': '적재구획', 'data_address': 'tshedimosetso_aterese', 'symbol': 'letshwao_Boleng', 'root': '뿌리주소', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'leina', 'value': 'Boleng', 'fmt': 'fomete', 'work': '작업경로'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
