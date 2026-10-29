#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/한글입력시험.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('한글입력시험', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('한글입력시험')
    yhdistämismääritys_ARVO = {'expected': '예상결과', 'Keyboard': 'näppäimistö', 'press': 'paina_Avain', 'self': '자신', 'test_modes_repeat_and_commit': 'test_전환반복확정', 'keys': '누름열', 'test_paste_and_unicode': 'testi_liitä_JA_UNICODE', 'data': 'data', 'key': '누름값', 'send': 'lähettää', 'test_words': 'test_낱말', 'InputTests': '한글입력시험', 'test_backspace': 'test_앞글자지우기', 'symbol': 'symboli_ARVO', 'char': 'merkkitiedot', 'type': 'TYYPPI_alue'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
