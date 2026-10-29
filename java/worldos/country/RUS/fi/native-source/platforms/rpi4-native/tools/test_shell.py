#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/testi_liittymä.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('testi_liittymä', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('testi_liittymä')
    yhdistämismääritys_ARVO = {'timeout': 'suoritus_AIKAKATKAISU', 'x': 'x_koordinaatti', 'msg': 'verkko_sanoma', 'i': '순번', 'reply': 'palaute', 'call': '호출', 'args': 'argumentti_MATRIISI', 'chunk': '조각', 'data': 'data', 'proc': 'Prosessi', 'long_text': '긴글', 'restored': '복원자료', 'send': 'lähettää', 'file': 'tiedoston_nimi', 'main': 'Suorita_2', 'found': 'Hae_KR', 'ROOT': 'aloite_juuri', 'text': 'teksti', 'marker': 'merkintä', 'command': 'komento', 'expected': '예상결과', 'pixel': 'kuvapiste', 'shell': 'liittymä', 'poll': '준비살피미', 'transcript': 'transkriptio', 'end': 'lopettaa_puhelu_SIIRTYMÄ', 'image': 'KUVA', 'key': '누름값', 'y': 'Y_koordinaatti', 'output': 'tulos', 'result': 'TULOS', 'client': 'asiakas', 'line': 'syöterivi', 'stream': 'virta_ARVO', 'name': 'Nimi', 'value': 'ARVO', 'receive': 'saada_sanoma', 'report': 'vahvistus_raportti', 'work': '작업경로', 'qmp': '모의제어접속'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
