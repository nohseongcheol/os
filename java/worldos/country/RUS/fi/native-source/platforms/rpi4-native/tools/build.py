#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/kääntää_Järjestelmä.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('kääntää_Järjestelmä', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('kääntää_Järjestelmä')
    yhdistämismääritys_ARVO = {'network': 'verkko', 'BUILD': 'kääntää_polku', 'ar': 'Arkisto_työkalu', 'build_examples': '예제만들기', 'posix': '포직스경로', 'font_data': 'fontti_data', 'flags': 'määritys_Background_Intelligent_Transfer_Service', 'a': '첫째값', 'cc': 'C_kääntäjä', 'args': 'argumentti_MATRIISI', 'source_flags': '원본설정', 'ld': 'linkitin_työkalu', 'method': 'menetelmä_merkintä', 'main': 'Suorita_2', 'objcopy': 'objekti_Tiedosto_muunnin', 'ROOT': 'aloite_juuri', 'cxx': '시플플번역기', 'includes': '포함인수', 'compiler': 'kääntäjä_työkalu', 'build_users': 'Luo_käyttäjä_tila', 'f': 'Tiedosto_merkintä', 'extra': '추가영역', 'exports': 'viedä_taulukko', 'jobs': '빌드작업', 'run': 'Suorita_komento', 'path': 'polku_2', 'REPO': 'säilö_juuri', 'tool': 'työkalut', 'classes': 'Luokka_polku', 'output': 'tulos', 'samples': '예제들', 'symbol': 'symboli_ARVO', 'source': '원본자료', 'name': 'Nimi', 'build_network': 'Luo_verkko', 'font_info': 'fontti_info', 'manifest': 'nippu_kokoonpanotiedot', 'work': '작업경로'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
