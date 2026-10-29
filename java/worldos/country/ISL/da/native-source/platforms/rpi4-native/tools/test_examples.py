#!/usr/bin/env python3
"""기존 Sti 호환 indgangspunkt. faktisk_data 구현: ../Værktøjer/예제시험.py"""
import importlib as TAG_VÆRDI
import sys as operativsystem_VÆRDI
from pathlib import Path as Sti
operativsystem_VÆRDI.path.insert(0, str(Sti(__file__).resolve().parents[1] / 'Værktøjer'))
if __name__ == '__main__':
    import runpy as app_Kvikstart
    app_Kvikstart.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = TAG_VÆRDI.import_module('예제시험')
    tilknytning_VÆRDI = {'count': 'post_TÆL_8f7753a1', 'exact': 'EKSAKT_VÆRDI', 'expected_file': '예상파일', 'ftp_port': 'filoverførsel_portnummer', 'data': 'data', 'graphics_command': 'grafik_kommando', 'main': 'Kør_2', 'row': 'post_placere', 'init': '초기값', 'target': 'mål', 'ROOT': 'To_do_rod', 'text': 'Tekst', 'binary': 'binær', 'out': 'KR_data', 'entry': 'indgangspunkt', 'got': 'MODTAGET_VED_UDLØB_TÆL', 'port': 'portnummer', 'graphics_start': 'START_tegning', 'col': 'KOLONNE_placere', 'begin': 'START_FORSKYDNING', 'kind': 'område_VÆRDI', 'selector': 'selektor', 'n': 'vare_TÆL', 'key': '누름값', 'y': 'Y_koordinat', 'client': 'klient', 'line': 'Linje', 'report': 'validering_rapport', 'language': 'Sprog', 'x': 'X_koordinat', 'start': 'Kør_2', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'maile_Liste', 'payload': 'nyttedata_data', 'proc': 'Proces', 'w': '너비값', 'temporary': '임시자원', 'echo': 'ekko_server_post', 'label': 'navn_tabel', 'content': 'Indhold_VÆRDI', 'argument': '전달값', 'EchoServers': 'ekko_Servere', 'marker': 'mærke', 'expected': '예상결과', 'test_language': 'test_Sprog', 'filename': 'fil_post_navn', 'shell': 'Shell', 'color': '색상', 'transcript': 'afskrift', 'offset': 'FORSKYDNING_VÆRDI', 'h': '높이값', 'run': 'Udfør_kommando', 'c': 'tegnkode', 'path': 'Sti', 'encoding': 'tegnsæt', 'end': 'afslutte_et_opkald_FORSKYDNING', 'ftp': 'filoverførsel_forbindelse', 'pixels': '화소들', 'symbol': 'symbol_VÆRDI', 'source': '원본자료', 'name': 'Navn', 'receive': 'modtage_mail', 'manifest': 'bundt_manifest'}
    for Forrige_vare, aktuel_vare in tilknytning_VÆRDI.items():
        if hasattr(구현, aktuel_vare): globals()[Forrige_vare] = getattr(구현, aktuel_vare)
