#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/자바라이브러리빌드.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('자바라이브러리빌드')
    대응 = {'header': 'setlhogo_Boleng', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'selekanyo_sa_tshedimosetso_tshedimosetso', 'src': '원본주소', 'run': 'diragatsa_Taelo', 'build_java_library': '자바라이브러리만들기', 'relative': '상대경로', 'classes': 'mofuta_tsela', 'dist': '배포경로', 'archive': 'boloka', 'output': '출력결과', 'root': '뿌리주소', 'name': 'leina', 'jar': '자바꾸러미', 'b': '둘째값', 'entries': '항목들'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
