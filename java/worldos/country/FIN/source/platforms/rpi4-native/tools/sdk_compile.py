#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/SDK_kääntää.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('SDK_kääntää', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('SDK_kääntää')
    yhdistämismääritys_ARVO = {'compiler': 'kääntäjä_työkalu', 'obj': 'kohdetiedosto', 'sdk': 'ohjelmankehityspaketti', 'output': 'tulos', 'main': 'Suorita_2', 'elf': 'suoritettava_tiedosto', 'is_c': 'tietojärjestelmät_C_Kieli', 'parser': 'jäsennin', 'language': 'Kieli', 'work': '작업경로', 'args': 'argumentti_MATRIISI'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
