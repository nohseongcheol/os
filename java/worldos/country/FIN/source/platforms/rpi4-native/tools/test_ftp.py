#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/testi_FTP.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('testi_FTP', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('testi_FTP')
    yhdistämismääritys_ARVO = {'timeout': 'suoritus_AIKAKATKAISU', 'payload': 'tiedot_data', 'broken': '손상자료', 'linux_example': '리눅스예제', 'chunk': '조각', 'data': 'data', 'proc': 'Prosessi', 'code': 'käsky_JONO', 'linux': '리눅스파일', 'archive': 'Arkisto', 'main': 'Suorita_2', 'net_source': 'NET_lähde', 'temporary': '임시자원', 'static_source': 'staattinen_lähde', 'java_source': '자바원문', 'echo': 'päivitys_palvelin_merkintä', 'ROOT': 'aloite_juuri', 'text': 'teksti', 'marker': 'merkintä', 'EchoFixture': '되돌림시험서버', 'command': 'komento', 'out': 'KR_data', 'expected': '예상결과', 'server_source': 'palvelin_lähde', 'shell': 'liittymä', 'upload': 'Upload_Files', 'transcript': 'transkriptio', 'port': 'portin_numero', 'native': 'alkuperäinen', 'elf': 'suoritettava_tiedosto', 'server_udp_port': 'palvelin_datagrammi_portti', 'packed': '묶인자료', 'bridge': 'silta', 'selector': 'valitsin', 'end': 'lopettaa_puhelu_SIIRTYMÄ', 'e': '보조항목', 'ftp': 'tiedostonsiirto_yhteys', 'key': '누름값', 'bytecode': '바이트코드', 'peer': 'vertaissolmu_ARVO', 'result': 'TULOS', 'unchanged': '보존자료', 'line': 'syöterivi', 'server_tcp_port': 'palvelin_virta_portti', 'source': '원본자료', 'NetworkBridge': 'silta_3de4fe3a', 'jar': '자바꾸러미', 'receive': 'saada_sanoma', 'report': 'vahvistus_raportti'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
