#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/kääntää_C_kääntäjä.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('kääntää_C_kääntäjä', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('kääntää_C_kääntäjä')
    yhdistämismääritys_ARVO = {'out': 'KR_data', 'builtins': '내장연산', 'header': 'otsikko_ARVO', 'sdk': 'ohjelmankehityspaketti', 'build_ccompiler': 'Luo_C_kääntäjä', 'i': '순번', 'elf': 'suoritettava_tiedosto', 'run': 'Suorita_komento', 'flags': 'määritys_Background_Intelligent_Transfer_Service', 'path': 'polku_2', 'p': 'data_toimi', 'cc': 'C_kääntäjä', 'obj': 'kohdetiedosto', 'flag': 'Asetukset_ARVO', 'ld': 'linkitin_työkalu', 'objects': 'kohde_Files', 'repo': 'säilö_polku', 'v': '임시값', 'upstream': 'yläpuolinen', 'root': 'juuri_OSOITE', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Nimi', 'includes': '포함인수'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
