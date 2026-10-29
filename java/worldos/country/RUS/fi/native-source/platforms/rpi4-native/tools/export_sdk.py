#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/viedä_SDK.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('viedä_SDK', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('viedä_SDK')
    yhdistämismääritys_ARVO = {'out': 'KR_data', 'obj': 'kohdetiedosto', 'relative': 'suhteellinen_polku', 'compiler_archive': 'kääntäjä_Arkisto', 'sdk': 'ohjelmankehityspaketti', 'dist': 'jakelu_polku', 'archive': 'Arkisto', 'main': 'Suorita_2', 'posix': '포직스경로', 'files': 'tiedostoluettelo', 'source': '원본자료', 'name': 'Nimi', 'target': 'tavoite', 'ROOT': 'aloite_juuri', 'destination': 'kohde_data_OSOITE', 'manifest': 'nippu_kokoonpanotiedot', 'work': '작업경로'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
