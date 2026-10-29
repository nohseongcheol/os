#!/usr/bin/env python3
"""기존 tsela 호환 tsenyo_ntlha. tota_tshedimosetso 구현: ../Thuluse/diragatsa_faele.py"""
import importlib as 가져오기
import sys as Tsamaisotiriso_Boleng
from pathlib import Path as tsela
Tsamaisotiriso_Boleng.path.insert(0, str(tsela(__file__).resolve().parents[1] / 'Thuluse'))
if __name__ == '__main__':
    import runpy as Tiriso_llae_ya_sediriso
    Tiriso_llae_ya_sediriso.run_module('diragatsa_faele', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('diragatsa_faele')
    대응 = {'timeout': '시간제한', 's': 'dikwalwa_tshedimosetso', 'i': '순번', 'match': '일치', 'files': 'faele_lenaane', 'program': 'Tiriso', 'executable': '실행가능파일', 'args': 'Thulaganyo_setlhopha', 'chunk': '조각', 'data': 'tshedimosetso', 'proc': 'Thulaganyo', 'send': 'romela', 'main': 'dirisa', 'marker': '확인표시', 'command': 'Taelo', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'diragatsa_Taelo', 'p': '자료위치', 'parser': '인수해석기', 'options': 'Diitlhophelwa', 'kind': 'setlhopha_Boleng_4b6d6445', 'selector': 'setlhophi', 'upload_data': 'laisa_tshedimosetso', 'end': 'kgaola_Baya_ka_Tekatekanyo', 'n': '개수', 'd': 'bogorogelo_tshedimosetso', 'key': '누름값', 'output': '출력결과', 'line': 'Mola', 'name': 'leina', 'upload_name': 'laisa_leina', 'receive': '수신하기'}
    for 이전, ga_jaana_selwana in 대응.items():
        if hasattr(구현, ga_jaana_selwana): globals()[이전] = getattr(구현, ga_jaana_selwana)
