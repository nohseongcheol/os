#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/testi_Java_VM.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('testi_Java_VM', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('testi_Java_VM')
    yhdistämismääritys_ARVO = {'message': '알림문', 's': 'merkkijono_data', 'actual': 'todellinen_KR', 'match': '일치', 'payload': 'tiedot_data', 'cases': 'testi_työ', 'fixture': 'testi_data', 'main': 'Suorita_2', 'ROOT': 'aloite_juuri', 'text': 'teksti', 'valid': 'kelvollinen', 'includes': '포함인수', 'include': 'sisältää', 'expected': '예상결과', 'sources': '원문목록', 'tmp': '임시경로', 'done': 'valmis_määrä', 'classes': 'Luokka_polku', 'output': 'tulos', 'result': 'TULOS', 'cmd': '명령인수', 'name': 'Nimi', 'jar': '자바꾸러미', 'report': 'vahvistus_raportti', 'tests': 'testi_luettelo'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
