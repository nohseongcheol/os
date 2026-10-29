#!/usr/bin/env python3
"""기존 polku_2 호환 aloituskohta. todellinen_data toteutus: ../työkalut/silta_3de4fe3a.py"""
import importlib as OTA_ARVO
import sys as käyttöjärjestelmä_ARVO
from pathlib import Path as polku_2
käyttöjärjestelmä_ARVO.path.insert(0, str(polku_2(__file__).resolve().parents[1] / 'työkalut'))
if __name__ == '__main__':
    import runpy as ohjelma_sovellusvalikko
    ohjelma_sovellusvalikko.run_module('silta_3de4fe3a', run_name='__main__', alter_sys=True)
else:
    toteutus = OTA_ARVO.import_module('silta_3de4fe3a')
    yhdistämismääritys_ARVO = {'response': 'vastaus', 'parts': 'polku_osa', 's': 'merkkijono_data', 'i': '순번', 'close': 'Sulje', 'forward': '전달규칙', 'slip_input': 'SLIP_syöte', 'self': '자신', 'item': 'merkintä_ARVO_962f286b', 'flags': 'määritys_Background_Intelligent_Transfer_Service', 'ftp_port': 'tiedostonsiirto_portin_numero', 'args': 'argumentti_MATRIISI', 'server': 'palvelin_ARVO', 'data': 'data', 'ethernet_input': 'Ethernet_syöte', 'trace_packet': 'jälki_paketti', 'GATEWAY': 'yhdyskäytävä_laitteisto_OSOITE', 'rule': 'sääntö_ARVO', 'protocol': '통신규약', 'forwards': '전달규칙들', 'occupied': '사용중주소', 'host': 'isäntä', 'ack': '확인번호', 'serial_port': 'COM_portti_numero', 'readers': '읽기대상들', 'guest': 'vieras', 'destination': 'kohde_data_OSOITE', 'ethernet_port': 'Ethernet_portti', 'b': 'SEKUNNIT_ARVO', 'MAC': 'absoluuttinen_osoite', 'arp': 'OSOITE_tarkkuus_paketti', 'writable': 'kirjoitettava', 'direction': '방향', 'seq': 'tilata_numero', 'frame': 'suoritus_kuva', 'loop': 'kehä_ARVO', 'port': 'portin_numero', 'offset': 'SIIRTYMÄ_ARVO', 'readable': '읽을수있음', 'c': 'merkkikoodi', 'p': 'data_toimi', 'writers': '쓰기대상들', 'IP': 'Internet_osoite_ARVO', 'e': '보조항목', 'n': 'kohde_LASKE', 'packet': 'paketti_data', 'arguments': '전달인수', 'source': '원본자료', 'NetworkBridge': 'silta_3de4fe3a', 'window': 'Ikkuna', 'capture': 'siepata'}
    for Edellinen_kohde, nykyinen_kohde in yhdistämismääritys_ARVO.items():
        if hasattr(toteutus, nykyinen_kohde): globals()[Edellinen_kohde] = getattr(toteutus, nykyinen_kohde)
