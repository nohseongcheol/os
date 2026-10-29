#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/부팅시험.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('부팅시험', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('부팅시험')
    yhdistämismääritys_ARVO = {'timeout': 'suoritus_AIKAKATKAISU', 'response': 'vastaus', 'msg': 'verkko_sanoma', 'exact': 'VERTAA_ARVO', 'markers': '확인표시들', 'i': '순번', 'match': '일치', 'execute': 'Suorita', 'cancel': 'kumota_leikkaus', 'cmd_byte': 'komento_tavu', 'reply': 'palaute', 'points': '지점들', 'server': 'palvelin_ARVO', 'data': 'data', 'prompt': 'kehote', 'enter': 'anna', 'imported': '들여온파일', 'send': 'lähettää', 'main': 'Suorita_2', 'ROOT': 'aloite_juuri', 'text': 'teksti', 'first_gui': '첫화면', 'pixel': 'kuvapiste', 'java_class': '자바클래스', 'upload': 'Upload_Files', 'pixels_file': 'kuvapiste_Tiedosto', 'pixels_data': 'kuvapiste_data', 'edit': 'muutos_ARVO', 'receive_until': '표시까지받기', 'selector': 'valitsin', 'size': 'Koko', 'qmp_path': '모의제어경로', 'key': '누름값', 'second_gui': 'SEKUNNIT_GUI', 'y': 'Y_koordinaatti', 'result': 'TULOS', 'samples': '예제들', 'client': 'asiakas', 'line': 'syöterivi', 'report': 'vahvistus_raportti', 'work': '작업경로', 'x': 'x_koordinaatti', 'python_checks': '파이썬검사', 'download': 'ladata', 'greeting': '인사', 'dims': '치수', 'chunk': '조각', 'deadline': 'määräaika_AIKA', 'proc': 'Prosessi', 'content': 'Sisältö_ARVO', 'block': 'tietolohko', 'marker': 'merkintä', 'command': 'komento', 'expected': '예상결과', 'shell': 'liittymä', 'drawing': 'piirustus_polku', 'f': 'Tiedosto_merkintä', 'transcript': 'transkriptio', 'offset': 'SIIRTYMÄ_ARVO', 'path': 'polku_2', 'screenshot': 'näyttökuva', 'arguments': '전달인수', 'pixels': '화소들', 'viewer': '화면접속자', 'output': 'tulos', 'stream': 'virta_ARVO', 'cmd': '명령인수', 'name': 'Nimi', 'qmp': '모의제어접속'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
