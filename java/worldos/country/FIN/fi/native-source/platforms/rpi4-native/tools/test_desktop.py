#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/testi_työpöytä.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('testi_työpöytä', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('testi_työpöytä')
    yhdistämismääritys_ARVO = {'x': 'x_koordinaatti', 'typing': '글자입력', 'message': '알림문', 'start': 'Suorita_2', 'down': '누르는중', 'exact': 'VERTAA_ARVO', 'i': '순번', 'press': 'paina_Avain', 'rectangles': '사각형들', 'sym': 'symboli', 'j': '안쪽순번', 'deadline': 'määräaika_AIKA', 'proc': 'Prosessi', 'data': 'data', 'main': 'Suorita_2', 'w': '너비값', 'init': '초기값', 'block': 'tietolohko', 'ROOT': 'aloite_juuri', 'text': 'teksti', 'marker': 'merkintä', 'report': 'vahvistus_raportti', 'until': '까지', 'clipboard': 'leikepöytä_ARVO', 'dst': 'kohde_OSOITE_08bbd577', 'seen': '본항목들', 'poll': '준비살피미', 'transcript': 'transkriptio', 'port': 'portin_numero', 'offset': 'SIIRTYMÄ_ARVO', 'h': '높이값', 'src': '원본주소', 'event': 'Tapahtuma', 'encoding': 'merkistö', 'size': 'Koko', 'key': '누름값', 'pixels': '화소들', 'y': 'Y_koordinaatti', 'output': 'tulos', 'symbol': 'symboli_ARVO', 'client': 'asiakas', 'char': 'merkkitiedot', 'rgb': '빛삼원색'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
