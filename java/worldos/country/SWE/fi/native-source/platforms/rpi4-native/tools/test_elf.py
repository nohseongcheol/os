#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/실행파일시험.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('실행파일시험', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('실행파일시험')
    yhdistämismääritys_ARVO = {'out': 'KR_data', 'expected': '예상결과', 'phoff': 'ohjelma_otsikko_SIIRTYMÄ', 'offset': 'SIIRTYMÄ_ARVO', 'invalid': 'pätemätön_data', 'path': 'polku_2', 'executable': 'suoritettava_tiedosto_KUVA', 'rejected': '거부결과', 'linux_example': '리눅스예제', 'original': '원본', 'result': 'TULOS', 'format_': 'muoto_b87fd068', 'main': 'Suorita_2', 'content': 'Sisältö_ARVO', 'source': '원본자료', 'name': 'Nimi', 'reference': 'Vertailu_perus', 'ROOT': 'aloite_juuri', 'value': 'ARVO', 'report': 'vahvistus_raportti'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
