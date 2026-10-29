#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/셸시험.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('셸시험', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('셸시험')
    대응 = {'timeout': '시간제한', 'x': 'rëddu_iks_yi', 'msg': 'mbaal_bataaxal', 'i': '순번', 'reply': 'tontu', 'call': '호출', 'args': 'Tegtal_TABLO', 'chunk': '조각', 'data': 'mbir', 'proc': 'yokkute', 'long_text': '긴글', 'restored': '복원자료', 'send': 'Yónnee', 'file': 'bara_denc', 'main': 'daw', 'found': '찾은결과', 'ROOT': '기준', 'text': 'Tekst', 'marker': '확인표시', 'command': 'ndigel', 'expected': '예상결과', 'pixel': 'piksel', 'shell': 'Wëreef', 'poll': '준비살피미', 'transcript': '대화기록', 'end': 'jeexal_Randal', 'image': 'nataal', 'key': '누름값', 'y': '세로좌표', 'output': '출력결과', 'result': '결과', 'client': 'lëkkalekat', 'line': 'buum', 'stream': 'dawal_xëyma', 'name': 'tur_253d1510', 'value': 'xëyma', 'receive': '수신하기', 'report': 'wéral_tënk', 'work': '작업경로', 'qmp': '모의제어접속'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
