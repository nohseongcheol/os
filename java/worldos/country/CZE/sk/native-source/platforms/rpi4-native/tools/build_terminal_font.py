#!/usr/bin/env python3
"""기존 Cesta 호환 položka_bod. skutočný_údaje 구현: ../Nástroje/zostava_Terminál_písmo.py"""
import importlib as TAKE_VALUE
import sys as operačný_systém_VALUE
from pathlib import Path as Cesta
operačný_systém_VALUE.path.insert(0, str(Cesta(__file__).resolve().parents[1] / 'Nástroje'))
if __name__ == '__main__':
    import runpy as program_spúšťač
    program_spúšťač.run_module('zostava_Terminál_písmo', run_name='__main__', alter_sys=True)
else:
    구현 = TAKE_VALUE.import_module('zostava_Terminál_písmo')
    mapovanie_VALUE = {'data': 'údaje', 'img': 'kresba_VALUE', 'bits': 'Background_Intelligent_Transfer_Service_Zoznam', 'x': 'X_súradnica', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'cesta_Zoznam', 'y': 'Y_súradnica', 'main': 'Spustiť_2', 'src': '원본주소', 'fonts': 'písmo_Zoznam', 'ROOT': 'akcia_koreň', 'p': 'údaje_pozícia', 'cp': 'kódovanie_znakov', 'target': 'cieľová_hodnota'}
    for 이전, v_termíne_splatnosti_položka in mapovanie_VALUE.items():
        if hasattr(구현, v_termíne_splatnosti_položka): globals()[이전] = getattr(구현, v_termíne_splatnosti_položka)
