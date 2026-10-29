#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/원격한글시험.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('원격한글시험', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('원격한글시험')
    yhdistämismääritys_ARVO = {'wait': '기다리기', 'typing': '글자입력', 'start': 'Suorita_2', 'profile': 'Profiili', 'focused': 'Tärkeät', 'serial': '직렬입출력', 'keys': '누름열', 'server': 'palvelin_ARVO', 'log': 'LOG_TIETUE', 'args': 'argumentti_MATRIISI', 'deadline': 'määräaika_AIKA', 'data': 'data', 'candidate': '후보', 'logs': '기록들', 'kw': 'nimetty_argumentti', 'number': '수치', 'main': 'Suorita_2', 'ready': '준비완료', 'found': 'Hae_KR', 'guest': 'vieras', 'ROOT': 'aloite_juuri', 'marker': 'merkintä', 'text': 'teksti', 'out': 'KR_data', 'env': 'ympäristö', 'f': 'Tiedosto_merkintä', 'port': 'portin_numero', 'offset': 'SIIRTYMÄ_ARVO', 'version': 'versionumero', 'p': 'data_toimi', 'selector': 'valitsin', 'xvfb': 'virtuaalinen_näyttö', 'display': 'näyttö', 'n': 'kohde_LASKE', 'key': '누름값', 'processes': '실행과정들', 'rootfs': '뿌리파일계층', 'xdo': 'virtuaalinen_syöte_työkalu', 'name': 'Nimi', 'window': 'Ikkuna', 'report': 'vahvistus_raportti', 'work': '작업경로'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
