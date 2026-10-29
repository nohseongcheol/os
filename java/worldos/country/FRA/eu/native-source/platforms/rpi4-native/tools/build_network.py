#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/eraiki_sare.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('eraiki_sare', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('eraiki_sare')
    대응 = {'obj': 'helburuko_fitxategi', 'objects': 'helburu_Fitxategiak', 'library': 'liburutegi', 'output': '출력결과', 'port': 'ataka_zenbaki', 'root': 'erro_helbide', 'files': 'fitxategi_Zerrenda', 'source': '원본자료', 'run': 'exekutatu_komando', 'flags': 'konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna', 'path': 'Bide_izena', 'build_network': 'sortu_sare', 'cc': '시언어번역기', 'ar': 'artxibo_tresna'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
