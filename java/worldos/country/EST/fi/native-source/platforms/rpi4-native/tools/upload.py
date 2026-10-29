#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/Upload_Files.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('Upload_Files', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('Upload_Files')
    yhdistämismääritys_ARVO = {'data': 'data', 'i': '순번', 'name': 'Nimi', 'c': 'merkkikoodi', 'p': 'data_toimi', 'args': 'argumentti_MATRIISI'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
