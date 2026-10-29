#!/usr/bin/env python3
"""기존 Hanyar_shiga 호환 Mashigar_bayanai_maki. Na_hakika_Tarin_bayani 구현: ../Kaya/예제시험.py"""
import importlib as 가져오기
import sys as OS_Daraja
from pathlib import Path as Hanyar_shiga
OS_Daraja.path.insert(0, str(Hanyar_shiga(__file__).resolve().parents[1] / 'Kaya'))
if __name__ == '__main__':
    import runpy as Shiri_Mai_Fara_Ka_ida
    Shiri_Mai_Fara_Ka_ida.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': 'Fayil_Gusar_da_lambar_kafa', 'data': 'Tarin_bayani', 'graphics_command': '그림명령', 'main': 'Tafiyar_da', 'row': '행위치', 'init': '초기값', 'target': 'tageti', 'ROOT': '기준', 'text': 'SMS', 'binary': 'Mai_bangare_biyu', 'out': '결과자료', 'entry': 'Mashigar_bayanai_maki', 'got': '받은수', 'port': 'lambar_kafa', 'graphics_start': 'Fara_zane', 'col': '열위치', 'begin': 'Fara_Sassautawa', 'kind': 'ɓangare_Daraja', 'selector': 'mai_zabe', 'n': '개수', 'key': '누름값', 'y': 'Maɓallin_Y_Mai_tsarawa', 'client': 'abokin_hulda', 'line': 'Layi', 'report': 'amincewa_Rahoto', 'language': 'yare', 'x': 'gamayyar_x', 'start': 'Tafiyar_da', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'Aika_Jeri', 'payload': 'Kumshinbayanai_Tarin_bayani', 'proc': 'haryar_aikin_na_ura', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'Suna_tebur', 'content': 'kunshiya_Daraja', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'Fayil_Mashigar_bayanai_Suna', 'shell': 'Mai_fayyace_umani', 'color': '색상', 'transcript': '대화기록', 'offset': 'Sassautawa_Daraja', 'h': '높이값', 'run': 'gudanar_Umarni', 'c': 'Lambar_sirrin_harafi', 'path': 'Hanyar_shiga', 'encoding': 'Ƙunshin_alƙalumma', 'end': 'Ƙarshe_Sassautawa', 'ftp': 'Fayil_Gusar_da_haɗi', 'pixels': '화소들', 'symbol': 'alama_Daraja', 'source': '원본자료', 'name': 'Suna', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
