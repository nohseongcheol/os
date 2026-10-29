#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/코딩시험.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('코딩시험', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('코딩시험')
    yhdistämismääritys_ARVO = {'out': 'KR_data', 'expected': '예상결과', 'sdk': 'ohjelmankehityspaketti', 'suffix': '뒷부분', 'arc': '압축묶음', 'main': 'Suorita_2', 'elf': 'suoritettava_tiedosto', 'run': 'Suorita_komento', 'name': 'Nimi', 'path': 'polku_2', 'p': 'data_toimi', 'ROOT': 'aloite_juuri', 'report': 'vahvistus_raportti', 'args': 'argumentti_MATRIISI'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
