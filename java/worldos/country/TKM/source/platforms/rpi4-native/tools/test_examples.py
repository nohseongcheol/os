#!/usr/bin/env python3
"""기존 Ýol 호환 girizmeklik_utuk. hakyky_maglumat 구현: ../Gurallar/예제시험.py"""
import importlib as 가져오기
import sys as operasiýa_ulgamy_baha
from pathlib import Path as Ýol
operasiýa_ulgamy_baha.path.insert(0, str(Ýol(__file__).resolve().parents[1] / 'Gurallar'))
if __name__ == '__main__':
    import runpy as programma_programma_paneli
    programma_programma_paneli.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'maglumat', 'graphics_command': '그림명령', 'main': 'Bitir', 'row': '행위치', 'init': '초기값', 'target': 'niýet', 'ROOT': '기준', 'text': 'Metin', 'binary': 'ikilik', 'out': '결과자료', 'entry': 'girizmeklik_utuk', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'başlat_çyzgy', 'col': '열위치', 'begin': 'başlat_Süýşüriş', 'kind': 'kategoriýa_baha', 'selector': 'saýlaýjy', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'müşderi', 'line': 'setir', 'report': 'barlag_hasabat', 'language': 'Dil', 'x': 'x_koordinatasy', 'start': 'Bitir', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'iber_Sanaw', 'payload': 'ýük_gutujygy_maglumat', 'proc': 'Proses', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'at_tablisa', 'content': 'Mazmun_baha', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'faýl_girizmeklik_at', 'shell': 'gabyjak', 'color': '색상', 'transcript': '대화기록', 'offset': 'Süýşüriş_baha', 'h': '높이값', 'run': 'ýerine_ýetir_buýruk', 'c': 'nyşanyň_kody', 'path': 'Ýol', 'encoding': 'nyşanlaryň_toplumy', 'end': 'tamamla_Süýşüriş', 'ftp': 'faýl_geçir_birikme', 'pixels': '화소들', 'symbol': 'nyşan_baha', 'source': '원본자료', 'name': 'Ad', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
