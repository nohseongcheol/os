#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/työpöytä_Näkymä.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('työpöytä_Näkymä', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('työpöytä_Näkymä')
    yhdistämismääritys_ARVO = {'count': 'merkintä_LASKE', 'special': '특수글쇠', 'error': 'VIRHE', 'exact': 'VERTAA_ARVO', 'network': 'verkko', 'closed': 'tietojärjestelmät_suljettu', 'length': 'kesto_ARVO', 'opened': '열림', 'ftp_port': 'tiedostonsiirto_portin_numero', 'server': 'palvelin_ARVO', 'resources': 'Resurssit', 'data': 'data', 'shift': 'VAIHTONÄPPÄIN', 'send': 'lähettää', 'run_desktop': 'suorittaa_työpöytä', 'protocol': '통신규약', 'forwards': '전달규칙들', 'host': 'isäntä', 'text': 'teksti', 'korean': '한글여부', 'port': 'portin_numero', 'signum': 'ilmoitus_numero', 'version': 'versionumero', 'parser': 'jäsennin', 'bridge': 'silta', 'kind': 'alue_ARVO', 'tail': '끝부분', 'size': 'Koko', 'previous_buttons': '이전단추', 'key': '누름값', 'y': 'Y_koordinaatti', 'prefix': '앞부분', 'client': 'asiakas', 'char': 'merkkitiedot', 'work': '작업경로', 'Keyboard': 'näppäimistö', 'x': 'x_koordinaatti', 'down': '누르는중', 'net': 'silta_merkintä', 'self': '자신', 'mode_changed': '입력방식알림', 'serial': '직렬입출력', 'args': 'argumentti_MATRIISI', 'Hangul': '한글조합', 'chunk': '조각', 'proc': 'Prosessi', 'Desktop': 'YHDISTÄ_työpöytä', 'buttons': '단추들', 'thread': 'työntekijä', 'pressed': '눌림', 'previous': 'Edellinen', 'toggle': 'MUUTA_tila', 'command': 'komento', 'sock': 'vastake_ARVO', 'frame': 'suoritus_kuva', 'ctrl': 'CTRL', 'path': 'polku_2', 'cp': 'merkkikoodaus', 'terminate': 'lopeta', 'security': 'suojaus', 'vnc_port': '원격화면접속번호', 'body': 'leipäteksti', 'index': 'HAKU_INDEKSI', 'exited': '종료됨', 'keysym': 'Avain_symboli', 'output': 'tulos', 'keyboard': 'näppäimistö_merkintä', 'interrupted': '가로채기됨', 'listener': 'saada_portti', 'reader': 'Lukija', 'NetworkBridge': 'silta_3de4fe3a', 'gui': '그림화면', 'worker': 'käsittely_tehtävä'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
