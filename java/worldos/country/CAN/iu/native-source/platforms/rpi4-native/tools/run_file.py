#!/usr/bin/env python3
"""기존 aqqut 호환 Iliniku_puinti. taannallarik_titiqqat 구현: ../도구/파일실행.py"""
import importlib as 가져오기
import sys as qarasaujakkut_aulattijjut_atuutilik
from pathlib import Path as aqqut
qarasaujakkut_aulattijjut_atuutilik.path.insert(0, str(aqqut(__file__).resolve().parents[1] / '도구'))
if __name__ == '__main__':
    import runpy as 실행기
    실행기.run_module('파일실행', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('파일실행')
    대응 = {'timeout': '시간제한', 's': 'qimiaq_titiqqat', 'i': '순번', 'match': '일치', 'files': 'ini_Titiqpalliagaq', 'program': 'pilirijjut', 'executable': '실행가능파일', 'args': 'aturniqarnirainiq_array', 'chunk': '조각', 'data': 'titiqqat', 'proc': 'Pivallianiq', 'send': 'nassiutili', 'main': '시작', 'marker': '확인표시', 'command': 'piqujijjut', 'include': '포함항목', 'dumped': '갈무리자료', 'run': '실행', 'p': '자료위치', 'parser': '인수해석기', 'options': 'Qanuqtuurutit', 'kind': 'Ataqatigiivvik_atuutilik', 'selector': '준비선택기', 'upload_data': 'inimit_aullaaqtiriniq_titiqqat', 'end': '끝위치', 'n': '개수', 'd': 'namunngarvik_titiqqat', 'key': '누름값', 'output': '출력결과', 'line': 'titikutaak', 'name': 'atiq', 'upload_name': 'inimit_aullaaqtiriniq_atiq', 'receive': '수신하기'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
