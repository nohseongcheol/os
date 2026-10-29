#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/testi_Windows.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('testi_Windows', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('testi_Windows')
    yhdistämismääritys_ARVO = {'wait': '기다리기', 'x': 'x_koordinaatti', 's': 'merkkijono_data', 'xy': 'koordinaattipari', 'sel': 'valitsin_a916db4e', 'seconds': '초단위', 'log': 'LOG_TIETUE', 'at': 'nykyinen_toimi', 'send': 'lähettää', 'main': 'Suorita_2', 'req': 'pyyntö_ARVO', 'hot': 'pikakuvake_ARVO', 'pump': 'kahva_tapahtuma', 'ROOT': 'aloite_juuri', 'marker': 'merkintä', 'b': 'SEKUNNIT_ARVO', 'command': 'komento', 'shell': 'liittymä', 'f': 'Tiedosto_merkintä', 'color': '색상', 'click': 'osoittaa_painike', 'k': '셋째순번', 'c': 'merkkikoodi', 'r': '반환값', 'p': 'data_toimi', 'done': 'valmis_määrä', 'end': 'lopettaa_puhelu_SIIRTYMÄ', 'command_mode': 'komento_tila', 'key': '누름값', 'y': 'Y_koordinaatti', 'pixels': '화소들', 'result': 'TULOS', 'report': 'vahvistus_raportti', 'dest': 'kohde_ARVO_toimi', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
