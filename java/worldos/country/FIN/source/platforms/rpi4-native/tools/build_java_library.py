#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/자바라이브러리빌드.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('자바라이브러리빌드', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('자바라이브러리빌드')
    yhdistämismääritys_ARVO = {'header': 'otsikko_ARVO', 'sources': '원문목록', 'i': '순번', 'info': 'msinfo32_exe', 'payload': 'tiedot_data', 'src': '원본주소', 'run': 'Suorita_komento', 'build_java_library': '자바라이브러리만들기', 'relative': 'suhteellinen_polku', 'classes': 'Luokka_polku', 'dist': 'jakelu_polku', 'archive': 'Arkisto', 'output': 'tulos', 'root': 'juuri_OSOITE', 'name': 'Nimi', 'jar': '자바꾸러미', 'b': 'SEKUNNIT_ARVO', 'entries': '항목들'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
