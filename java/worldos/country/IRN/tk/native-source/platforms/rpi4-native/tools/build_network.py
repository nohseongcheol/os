#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/düz_Tor_243da480.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('düz_Tor_243da480', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('düz_Tor_243da480')
    대응 = {'obj': 'çykyş_faýly', 'objects': 'barylmaly_ýer_Faýllar', 'library': 'Kitaphana', 'output': '출력결과', 'port': '접속번호', 'root': '뿌리주소', 'files': 'faýl_Sanaw', 'source': '원본자료', 'run': 'ýerine_ýetir_buýruk', 'flags': '설정비트', 'path': 'Ýol', 'build_network': 'döretmek_Tor', 'cc': '시언어번역기', 'ar': 'Arhiw_gural'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
