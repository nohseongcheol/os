#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/Luo_KUVA.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('Luo_KUVA', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('Luo_KUVA')
    yhdistämismääritys_ARVO = {'total': 'summa_kapasiteetti', 'start': 'Suorita_2', 'firmware': 'laiteohjelmisto_ARVO', 'files': 'tiedostoluettelo', 'archive_base': 'Arkisto_PERUS', 'partition': 'osio_Tiedosto', 'archive': 'Arkisto', 'main': 'Suorita_2', 'block': 'tietolohko', 'ROOT': 'aloite_juuri', 'boot': '부팅경로', 'stage': 'vaihe_ARVO', 'out': 'KR_data', 'expected': '예상결과', 'f': 'Tiedosto_merkintä', 'src': '원본주소', 'path': 'polku_2', 'p': 'data_toimi', 'extracted': '추출자료', 'member': 'jäsen', 'mbr': 'pääkäynnistystietue', 'image': 'KUVA', 'sector_count': '섹터개수', 'dist': 'jakelu_polku', 'sha': '해시계산', 'license_': 'lisenssi', 'source': '원본자료', 'name': 'Nimi', 'value': 'ARVO', 'manifest': 'nippu_kokoonpanotiedot', 'dest': 'kohde_ARVO_toimi', 'work': '작업경로'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
