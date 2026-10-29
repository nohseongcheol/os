#!/usr/bin/env python3
"""기존 njia 호환 ingizo_pointi. halisi_data 구현: ../Zana/시언어번역기빌드.py"""
import importlib as 가져오기
import sys as mfumo_endeshi_thamani
from pathlib import Path as njia
mfumo_endeshi_thamani.path.insert(0, str(njia(__file__).resolve().parents[1] / 'Zana'))
if __name__ == '__main__':
    import runpy as programu_droo_ya_programu
    programu_droo_ya_programu.run_module('시언어번역기빌드', run_name='__main__', alter_sys=True)
else:
    구현 = 가져오기.import_module('시언어번역기빌드')
    대응 = {'out': '결과자료', 'builtins': '내장연산', 'header': 'kichwa_thamani', 'sdk': '개발꾸러미', 'build_ccompiler': '시언어번역기만들기', 'i': '순번', 'elf': '실행파일', 'run': 'tekeleza_amri', 'flags': 'usanidi_Huduma_ya_Uhamisho_wa_Ujasusi_wa_Mandharinyuma', 'path': 'njia', 'p': '자료위치', 'cc': '시언어번역기', 'obj': 'faili_fikio', 'flag': 'Mipangilio_thamani', 'ld': '연결편집기', 'objects': 'fikio_Faili', 'repo': 'uwekaji_njia', 'v': '임시값', 'upstream': 'mfululizo_wa_juu', 'root': '뿌리주소', 'assets': '탑재자료', 'source': '원본자료', 'name': 'Jina', 'includes': '포함인수'}
    for 이전, 현재 in 대응.items():
        if hasattr(구현, 현재): globals()[이전] = getattr(구현, 현재)
