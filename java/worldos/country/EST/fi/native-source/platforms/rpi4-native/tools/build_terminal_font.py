#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/kääntää_Pääte_fontti.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('kääntää_Pääte_fontti', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('kääntää_Pääte_fontti')
    yhdistämismääritys_ARVO = {'data': 'data', 'img': 'piirustus_ARVO', 'bits': 'Background_Intelligent_Transfer_Service_luettelo', 'x': 'x_koordinaatti', 'draw': '화면그리기', 'licences': '이용허락목록', 'paths': 'polku_luettelo', 'y': 'Y_koordinaatti', 'main': 'Suorita_2', 'src': '원본주소', 'fonts': 'fontti_luettelo', 'ROOT': 'aloite_juuri', 'p': 'data_toimi', 'cp': 'merkkikoodaus', 'target': 'tavoite'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
