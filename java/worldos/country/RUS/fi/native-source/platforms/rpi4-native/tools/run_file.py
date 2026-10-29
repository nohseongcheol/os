#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/Suorita_Tiedosto.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('Suorita_Tiedosto', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('Suorita_Tiedosto')
    yhdistämismääritys_ARVO = {'timeout': 'suoritus_AIKAKATKAISU', 's': 'merkkijono_data', 'i': '순번', 'match': '일치', 'files': 'tiedostoluettelo', 'program': 'ohjelma', 'executable': 'suoritettava_tiedosto_KUVA', 'args': 'argumentti_MATRIISI', 'chunk': '조각', 'data': 'data', 'proc': 'Prosessi', 'send': 'lähettää', 'main': 'Suorita_2', 'marker': 'merkintä', 'command': 'komento', 'include': 'sisältää', 'dumped': '갈무리자료', 'run': 'Suorita_komento', 'p': 'data_toimi', 'parser': 'jäsennin', 'options': 'Asetukset_7f769d16', 'kind': 'alue_ARVO', 'selector': 'valitsin', 'upload_data': 'Upload_data', 'end': 'lopettaa_puhelu_SIIRTYMÄ', 'n': 'kohde_LASKE', 'd': 'kohde_data', 'key': '누름값', 'output': 'tulos', 'line': 'syöterivi', 'name': 'Nimi', 'upload_name': 'Upload_nimi', 'receive': 'saada_sanoma'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
