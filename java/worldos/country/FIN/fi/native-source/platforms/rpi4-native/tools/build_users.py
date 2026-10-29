#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/kääntää_käyttäjä_tila.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('kääntää_käyttäjä_tila', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('kääntää_käyttäjä_tila')
    yhdistämismääritys_ARVO = {'mode': 'menetelmä_tila', 'header': 'otsikko_ARVO', 'i': '순번', 'build_ccompiler': 'Luo_C_kääntäjä', 'ar': 'Arkisto_työkalu', 'posix': '포직스경로', 'payload': 'tiedot_data', 'flags': 'määritys_Background_Intelligent_Transfer_Service', 'cases': 'testi_työ', 'cc': 'C_kääntäjä', 'data': 'data', 'build_java_library': '자바라이브러리만들기', 'ld': 'linkitin_työkalu', 'repo': 'säilö_polku', 'build_python': 'Luo_PYTHON', 'inc': 'sisältää_polku', 'argument': '전달값', 'text': 'teksti', 'headers': 'otsikko_luettelo', 'cxx': '시플플번역기', 'valid': 'kelvollinen', 'build': 'kääntää', 'build_users': 'Luo_käyttäjä_tila', 'compiler': 'kääntäjä_työkalu', 'uzlib': '압축해제경로', 'extra': '추가영역', 'phoff': 'ohjelma_otsikko_SIIRTYMÄ', 'offset': 'SIIRTYMÄ_ARVO', 'text_address': 'komento_OSOITE', 'abi': '호출규약', 'assembly': 'kokoonpano', 'run': 'Suorita_komento', 'path': 'polku_2', 'p': 'data_toimi', 'changed': '바뀐자료', 'n': 'kohde_LASKE', 'flag': 'Asetukset_ARVO', 'index': 'HAKU_INDEKSI', 'classes': 'Luokka_polku', 'output': 'tulos', 'loads': '적재구획', 'data_address': 'data_OSOITE', 'symbol': 'symboli_ARVO', 'root': 'juuri_OSOITE', 'patches': '수정사항', 'source': '원본자료', 'sizes': '크기목록', 'blobs': '탑재덩이들', 'name': 'Nimi', 'value': 'ARVO', 'fmt': 'muoto_932e03c8', 'work': '작업경로'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
