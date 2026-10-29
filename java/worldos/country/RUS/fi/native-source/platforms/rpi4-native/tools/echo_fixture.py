#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/되돌림시험서버.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('되돌림시험서버', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('되돌림시험서버')
    yhdistämismääritys_ARVO = {'data': 'data', 'e': '보조항목', 'connection': 'yhteys_e05f319b', 'f': 'Tiedosto_merkintä', 'peer': 'vertaissolmu_ARVO', 'self': '자신', 'udp': 'datagrammi_ohjain', 't': 'Pääte_merkintä', 'tcp': 'yhteys_ohjain', 'EchoFixture': '되돌림시험서버', 'args': 'argumentti_MATRIISI', 'chunk': '조각'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
