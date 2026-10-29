#!/usr/bin/env python3
"""기존 Bide_izena 호환 sarrera_p. benetako_datuak 구현: ../Tresnak/예제시험.py"""
import importlib as HARTU_balio
import sys as sistema_eragile_balio
from pathlib import Path as Bide_izena
sistema_eragile_balio.path.insert(0, str(Bide_izena(__file__).resolve().parents[1] / 'Tresnak'))
if __name__ == '__main__':
    import runpy as aplik_abiarazle
    aplik_abiarazle.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = HARTU_balio.import_module('예제시험')
    대응 = {'count': 'sarrera_ZENBATU', 'exact': 'BERDIN_balio', 'expected_file': '예상파일', 'ftp_port': 'fitxategi_transferitu_ataka_zenbaki', 'data': 'datuak', 'graphics_command': 'grafikoak_komando', 'main': 'Exekutatu_2', 'row': 'ERRENKADA_kargu', 'init': '초기값', 'target': 'helburu_balio', 'ROOT': 'Project_erro', 'text': 'Testua', 'binary': 'bitar', 'out': 'neurria_datuak', 'entry': 'sarrera_p', 'got': 'RECEIVED_ZENBATU', 'port': 'ataka_zenbaki', 'graphics_start': '그림시작', 'col': 'zutabe_kargu', 'begin': 'HASI_Geruzak', 'kind': 'Kategoria_balio', 'selector': '준비선택기', 'n': 'elementu_ZENBATU', 'key': '누름값', 'y': 'Y_koordenatu', 'client': 'bezero', 'line': 'Marra', 'report': 'balidazio_txosten', 'language': 'Hizkuntza', 'x': 'X_koordenatu', 'start': 'Exekutatu_2', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'bidali_Zerrenda', 'payload': 'karga_datuak', 'proc': 'Prozesua', 'w': '너비값', 'temporary': '임시자원', 'echo': 'atzeko_planoko_eguneratze_zerbitzari_sarrera', 'label': 'izen_taula', 'content': 'eduki_balio', 'argument': '전달값', 'EchoServers': 'atzeko_planoko_eguneratze_Zerbitzariak', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'fitxategi_sarrera_izen', 'shell': 'shell', 'color': '색상', 'transcript': '대화기록', 'offset': 'Geruzak_balio', 'h': '높이값', 'run': 'exekutatu_komando', 'c': 'karaktere_kode', 'path': 'Bide_izena', 'encoding': 'karaktere_joko', 'end': 'amaitu_Geruzak', 'ftp': 'fitxategi_transferitu_konexio', 'pixels': '화소들', 'symbol': 'ikur_balio', 'source': '원본자료', 'name': 'Izena', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
