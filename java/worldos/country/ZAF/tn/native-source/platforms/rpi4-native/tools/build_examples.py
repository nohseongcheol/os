#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/예제빌드.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제빌드')
    대응 = {'out': '결과자료', 'build_examples': '예제만들기', 'files': 'faele_lenaane', 'java': '자바실행', 'run': 'diragatsa_Taelo', 'path': 'tsela', 'p': '자료위치', 'readme': 'MPUISE', 'build_java_library': '자바라이브러리만들기', 'code': 'taelo_TATELANO', 'index': '색인', 'classes': 'mofuta_tsela', 'repo': '저장소경로', 'root': '뿌리주소', 'content': 'Diteng_Boleng', 'source': '원본자료', 'name': 'leina', 'target': 'setotwa', 'manifest': '꾸러미명세', 'language': 'Puo'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
