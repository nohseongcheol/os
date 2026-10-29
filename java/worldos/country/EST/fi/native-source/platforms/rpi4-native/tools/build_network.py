#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/kääntää_verkko.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('kääntää_verkko', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('kääntää_verkko')
    yhdistämismääritys_ARVO = {'obj': 'kohdetiedosto', 'objects': 'kohde_Files', 'library': 'kirjasto', 'output': 'tulos', 'port': 'portin_numero', 'root': 'juuri_OSOITE', 'files': 'tiedostoluettelo', 'source': '원본자료', 'run': 'Suorita_komento', 'flags': 'määritys_Background_Intelligent_Transfer_Service', 'path': 'polku_2', 'build_network': 'Luo_verkko', 'cc': 'C_kääntäjä', 'ar': 'Arkisto_työkalu'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
