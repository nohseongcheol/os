#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/한글입력.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('한글입력', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('한글입력')
    yhdistämismääritys_ARVO = {'old': 'Edellinen_kohde', 'backspace': '앞글자지우기', 'committed': '확정글', 'KEYS': 'Avain_Asettelu', 'self': '자신', 'FINALS': '겹끝소리', 'VOWELS': '겹가운뎃소리', 'INITIAL': '첫소리목록', 'initial': '첫소리', 'commit': 'vahvistaa_muutokset_kokoonpano', 'feed': 'syöte_Avain', 'vowel': '가운뎃소리', 'Hangul': '한글조합', 'SPLIT': '끝소리가르기', 'final': '끝소리', 'key': '누름값', 'send': 'lähettää', 'left': '왼쪽', 'FINAL': '끝소리목록', 'history': 'Historia', 'pair': '한쌍', 'char': 'merkkitiedot', 'VOWEL': '가운뎃소리목록', 'right': 'OIKEA', 'value': 'ARVO', 'text': 'teksti'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
