#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/kääntää_PYTHON.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('kääntää_PYTHON', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('kääntää_PYTHON')
    yhdistämismääritys_ARVO = {'ld': 'linkitin_työkalu', 'archive': 'Arkisto', 'SHA256': 'vahvistus_hajautusarvo', 'build_python': 'Luo_PYTHON', 'root': 'juuri_OSOITE', 'source': '원본자료', 'name': 'Nimi', 'path': 'polku_2', 'VERSION': 'versio_ARVO_237a4c94', 'cc': 'C_kääntäjä', 'tar': '타르꾸러미', 'newlib': '뉴리브포함경로', 'member': 'jäsen'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
