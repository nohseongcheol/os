#!/usr/bin/env python3
"""기존 Yoonu_jëmale 호환 dugal_xabaar_Tomb. liteew_mbir 구현: ../Jumtukaay_yi/def_bara_denc.py"""
import importlib as 가져오기
import sys as doxalukaay_xëyma
from pathlib import Path as Yoonu_jëmale
doxalukaay_xëyma.path.insert(0, str(Yoonu_jëmale(__file__).resolve().parents[1] / 'Jumtukaay_yi'))
if __name__ == '__main__':
    import runpy as jëfekaay_armuwaaru_jëfekaay
    jëfekaay_armuwaaru_jëfekaay.run_module('def_bara_denc', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('def_bara_denc')
    대응 = {'timeout': '시간제한', 's': 'araf_yu_bennoo_mbir', 'i': '순번', 'match': '일치', 'files': 'bara_denc_lim', 'program': 'jëfekaay', 'executable': '실행가능파일', 'args': 'Tegtal_TABLO', 'chunk': '조각', 'data': 'mbir', 'proc': 'yokkute', 'send': 'Yónnee', 'main': 'daw', 'marker': '확인표시', 'command': 'ndigel', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'def_ndigel', 'p': '자료위치', 'parser': '인수해석기', 'options': 'tànneef', 'kind': 'ngiir_xëyma', 'selector': 'tànnkat', 'upload_data': 'toxalsi_mbir', 'end': 'jeexal_Randal', 'n': '개수', 'd': 'jëmmukaay_mbir', 'key': '누름값', 'output': '출력결과', 'line': 'buum', 'name': 'tur_253d1510', 'upload_name': 'toxalsi_tur', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
