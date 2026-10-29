#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/예제빌드.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('예제빌드', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('예제빌드')
    yhdistämismääritys_ARVO = {'out': 'KR_data', 'build_examples': '예제만들기', 'files': 'tiedostoluettelo', 'java': '자바실행', 'run': 'Suorita_komento', 'path': 'polku_2', 'p': 'data_toimi', 'readme': 'Lueminut', 'build_java_library': '자바라이브러리만들기', 'code': 'käsky_JONO', 'index': 'HAKU_INDEKSI', 'classes': 'Luokka_polku', 'repo': 'säilö_polku', 'root': 'juuri_OSOITE', 'content': 'Sisältö_ARVO', 'source': '원본자료', 'name': 'Nimi', 'target': 'tavoite', 'manifest': 'nippu_kokoonpanotiedot', 'language': 'Kieli'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
