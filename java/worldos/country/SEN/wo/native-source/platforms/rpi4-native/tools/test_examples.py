#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/예제시험.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('예제시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('예제시험')
    대응 = {'count': '항목수', 'exact': '정확한값', 'expected_file': '예상파일', 'ftp_port': '파일전송접속번호', 'data': 'mbir', 'graphics_command': '그림명령', 'main': 'daw', 'row': '행위치', 'init': '초기값', 'target': 'luñu_name', 'ROOT': '기준', 'text': 'Tekst', 'binary': 'Seexalin_ci_kaw_0_et1', 'out': '결과자료', 'entry': 'dugal_xabaar_Tomb', 'got': '받은수', 'port': '접속번호', 'graphics_start': 'Door_deseñ', 'col': '열위치', 'begin': 'Door_Randal', 'kind': 'ngiir_xëyma', 'selector': 'tànnkat', 'n': '개수', 'key': '누름값', 'y': '세로좌표', 'client': 'lëkkalekat', 'line': 'buum', 'report': 'wéral_tënk', 'language': 'Làkk', 'x': 'rëddu_iks_yi', 'start': 'daw', 'rgb': '빛삼원색', 'down': '누르는중', 'listing': 'Yónnee_lim', 'payload': 'njoxe_yu_solowu_mbir', 'proc': 'yokkute', 'w': '너비값', 'temporary': '임시자원', 'echo': '되돌림서버항목', 'label': 'tur_àlluwa', 'content': 'Këmb_xëyma', 'argument': '전달값', 'EchoServers': '되돌림서버', 'marker': '확인표시', 'expected': '예상결과', 'test_language': 'test_언어', 'filename': 'bara_denc_dugal_xabaar_tur', 'shell': 'Wëreef', 'color': '색상', 'transcript': '대화기록', 'offset': 'Randal_xëyma', 'h': '높이값', 'run': 'def_ndigel', 'c': 'kotu_araf', 'path': 'Yoonu_jëmale', 'encoding': 'Mbindin', 'end': 'jeexal_Randal', 'ftp': 'bara_denc_toxal_jokkalóo', 'pixels': '화소들', 'symbol': 'sembóol_xëyma', 'source': '원본자료', 'name': 'tur_253d1510', 'receive': '수신하기', 'manifest': '꾸러미명세'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
