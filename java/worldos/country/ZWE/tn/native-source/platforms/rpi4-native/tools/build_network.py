#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/aga_Neteweke.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('aga_Neteweke', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('aga_Neteweke')
    대응 = {'obj': 'Faele_ya_bogorogelo', 'objects': 'bogorogelo_Difaele', 'library': 'laeborari', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'faele_lenaane', 'source': '원본자료', 'run': 'diragatsa_Taelo', 'flags': '설정비트', 'path': 'tsela', 'build_network': 'tlhama_Neteweke', 'cc': '시언어번역기', 'ar': 'boloka_sediriswa'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
