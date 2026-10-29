#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/testi_swing.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('testi_swing', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('testi_swing')
    yhdistämismääritys_ARVO = {'wait': '기다리기', 'x': 'x_koordinaatti', 's': 'merkkijono_data', 'i': '순번', 'sel': 'valitsin_a916db4e', 'seconds': '초단위', 'log': 'LOG_TIETUE', 'data': 'data', 'at': 'nykyinen_toimi', 'send': 'lähettää', 'main': 'Suorita_2', 'req': 'pyyntö_ARVO', 'hot': 'pikakuvake_ARVO', 'pump': 'kahva_tapahtuma', 'ROOT': 'aloite_juuri', 'marker': 'merkintä', 'b': 'SEKUNNIT_ARVO', 'command': 'komento', 'shell': 'liittymä', 'f': 'Tiedosto_merkintä', 'click': 'osoittaa_painike', 'k': '셋째순번', 'c': 'merkkikoodi', 'r': '반환값', 'p': 'data_toimi', 'command_mode': 'komento_tila', 'end': 'lopettaa_puhelu_SIIRTYMÄ', 'classes': 'Luokka_polku', 'key': '누름값', 'y': 'Y_koordinaatti', 'result': 'TULOS', 'report': 'vahvistus_raportti', 'dest': 'kohde_ARVO_toimi', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
