#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/예제되돌림서버.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('예제되돌림서버', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('예제되돌림서버')
    yhdistämismääritys_ARVO = {'data': 'data', 'sock': 'vastake_ARVO', 'tcp_port': 'TCP_portti', 'chunk': '조각', 'received': '수신됨', 'self': '자신', 'UDP': 'datagrammi_kahva_pyyntö', 'thread': 'työntekijä', 'echo': 'päivitys_palvelin_merkintä', 'TCP': 'kahva_yhteys_pyyntö', 'EchoServers': 'päivitys_Palvelimet', 'parser': 'jäsennin', 'server': 'palvelin_ARVO', 'udp_port': 'UDP_portti', 'args': 'argumentti_MATRIISI'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
