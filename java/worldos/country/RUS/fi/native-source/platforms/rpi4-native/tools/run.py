#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/Suorita_komento.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('Suorita_komento', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('Suorita_komento')
    yhdistämismääritys_ARVO = {'supported': '지원목록', 'parser': 'jäsennin', 'qemu': '모의기계', 'run_desktop': 'suorittaa_työpöytä', 'main': 'Suorita_2', 'host': 'isäntä', 'status': 'Tila_ARVO', 'NetworkBridge': 'silta_3de4fe3a', 'ROOT': 'aloite_juuri', 'bridge': 'silta', 'loader': 'latausohjelma', 'base': 'Tausta_ARVO', 'options': 'Asetukset_7f769d16', 'binary': 'binaarinen', 'args': 'argumentti_MATRIISI', 'command': 'komento'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
