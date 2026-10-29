#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/tekeleza_faili.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('tekeleza_faili', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('tekeleza_faili')
    대응 = {'timeout': '시간제한', 's': 'tungo_data', 'i': '순번', 'match': '일치', 'files': 'faili_Orodha', 'program': 'programu', 'executable': '실행가능파일', 'args': 'hoja_ARRAY', 'chunk': '조각', 'data': 'data', 'proc': 'Mchakato', 'send': 'tuma', 'main': 'endesha', 'marker': '확인표시', 'command': 'amri', 'include': '포함항목', 'dumped': '갈무리자료', 'run': 'tekeleza_amri', 'p': '자료위치', 'parser': 'kichanganuzi', 'options': 'chaguo', 'kind': 'kategoria_thamani', 'selector': 'kiteuzi', 'upload_data': 'pakia_data', 'end': 'tamatia_Chipua', 'n': '개수', 'd': 'fikio_data', 'key': '누름값', 'output': '출력결과', 'line': 'laini', 'name': 'Jina', 'upload_name': 'pakia_jina', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
